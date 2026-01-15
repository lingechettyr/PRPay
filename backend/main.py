from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
from database import get_db
from data_models import PRReviewWithDetails
from schemas import ClaimPRRequest, ClaimPRResponse, StatsResponse
from enums import ReviewStatus

from config import get_settings
from routers import webhooks_router, reviews_router

app = FastAPI(title="PRPay API", version="1.0.0")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhooks_router)
app.include_router(reviews_router)


@app.get("/")
def root():
    return {
        "message": "PRPay API",
        "version": "1.0.0",
        "endpoints": {
            "GET /getPRs": "Get PR reviews for a user",
            "POST /claimPR": "Claim a PR review",
            "GET /getStats": "Get analytics statistics (admin)"
        }
    }


@app.get(
    "/getPRs",
    response_model=List[PRReviewWithDetails],
    summary="Get PR reviews for a user",
    description="Retrieve PR reviews for a specific user, optionally filtered by status"
)
def get_prs(
    user_id: str = Query(..., description="GitHub user ID of the reviewer"),
    status: Optional[ReviewStatus] = Query(None, description="Filter by review status")
):
    """
    Get all PR reviews for a specific user, with optional status filter.

    Args:
        user_id: GitHub user ID
        status: Optional status filter (requested, claimable, claimed, ineligible, done)

    Returns:
        List of PR reviews with full PR details
    """
    try:
        db = get_db()

        # Build query to join user_pr_reviews with pull_requests
        query = db.table("user_pr_reviews") \
            .select(
                "id, user_id, pr_id, status, payout, timestamp, "
                "pull_requests(id, title, body, url, created_at)"
            ) \
            .eq("user_id", user_id)

        # Add status filter if provided
        if status:
            query = query.eq("status", status.value)

        # Execute query
        response = query.execute()

        # Transform the data to match our response model
        results = []
        for item in response.data:
            pr_data = item.get("pull_requests")
            if pr_data:
                results.append({
                    "pr_id": pr_data["id"],
                    "pr_title": pr_data["title"],
                    "pr_body": pr_data["body"],
                    "pr_url": pr_data["url"],
                    "pr_created_at": pr_data["created_at"],
                    "review_id": item["id"],
                    "user_id": item["user_id"],
                    "status": item["status"],
                    "payout": float(item["payout"]),
                    "review_timestamp": item["timestamp"]
                })

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch PR reviews: {str(e)}"
        )


@app.post(
"/claimPR",
response_model=ClaimPRResponse,
summary="Claim a PR review",
description="Claim a PR review by updating its status from 'claimable' to 'claimed'"
)
def claim_pr(request: ClaimPRRequest):
    """
        Claim a PR review. Only works if the review status is 'claimable'.

        Args:
            request: ClaimPRRequest with user_id and pr_id

        Returns:
            ClaimPRResponse with success status and updated review details
    """
    try:
        db = get_db()

        # First, fetch the current review to check its status
        review_response = db.table("user_pr_reviews") \
            .select("id, status") \
            .eq("user_id", request.user_id) \
            .eq("pr_id", request.pr_id) \
            .execute()

        if not review_response.data:
            raise HTTPException(
                status_code=404,
                detail=f"No review found for user_id={request.user_id} and pr_id={request.pr_id}"
            )

        review = review_response.data[0]
        current_status = review["status"]

        # Check if status is 'claimable'
        if current_status != ReviewStatus.CLAIMABLE.value:
            return ClaimPRResponse(
                success=False,
                message=f"Cannot claim PR. Current status is '{current_status}', must be 'claimable'",
                review_id=review["id"],
                status=ReviewStatus(current_status)
            )

        # Update status to 'claimed'
        update_response = db.table("user_pr_reviews") \
            .update({"status": ReviewStatus.CLAIMED.value}) \
            .eq("user_id", request.user_id) \
            .eq("pr_id", request.pr_id) \
            .execute()

        if update_response.data:
            return ClaimPRResponse(
                success=True,
                message="PR successfully claimed",
                review_id=review["id"],
                status=ReviewStatus.CLAIMED
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to update review status"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to claim PR: {str(e)}"
        )


@app.get(
    "/getStats",
    response_model=StatsResponse,
    summary="Get analytics statistics",
    description="Get PR review statistics including claimable, claimed, and reviewed counts within a time range. Optionally filter by user_id."
)
def get_stats(
    start_time: str = Query(..., description="Start time in ISO format (YYYY-MM-DDTHH:MM:SS)"),
    end_time: str = Query(..., description="End time in ISO format (YYYY-MM-DDTHH:MM:SS)"),
    user_id: Optional[str] = Query(None, description="Optional: GitHub user ID to get stats for a specific user")
):
    """
    Get analytics statistics for PR reviews within a specified time range.
    If user_id is provided, returns stats for that user only. Otherwise, returns totals across all users.

    Args:
        start_time: Start timestamp in ISO format
        end_time: End timestamp in ISO format
        user_id: Optional GitHub user ID to filter by specific user

    Returns:
        StatsResponse with aggregated statistics
    """
    try:
        db = get_db()

        # Validate datetime strings
        try:
            datetime.fromisoformat(start_time)
            datetime.fromisoformat(end_time)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid datetime format: {str(e)}. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
            )

        # Build query with time range filters
        query = db.table("user_pr_reviews") \
            .select("status, payout") \
            .gte("timestamp", start_time) \
            .lte("timestamp", end_time)

        # Add user_id filter if provided
        if user_id:
            query = query.eq("user_id", user_id)

        # Execute query
        response = query.execute()

        # Initialize statistics
        claimable_total = 0.0
        claimable_count = 0
        claimed_total = 0.0
        claimed_count = 0
        reviewed_count = 0

        # Aggregate statistics
        for review in response.data:
            status = review.get("status")
            payout = float(review.get("payout", 0))

            if status == ReviewStatus.CLAIMABLE.value:
                claimable_total += payout
                claimable_count += 1
            elif status == ReviewStatus.CLAIMED.value:
                claimed_total += payout
                claimed_count += 1
            elif status == ReviewStatus.DONE.value:
                reviewed_count += 1

        return StatsResponse(
            claimable_total_value=claimable_total,
            claimable_pr_count=claimable_count,
            claimed_total_value=claimed_total,
            claimed_pr_count=claimed_count,
            total_prs_reviewed=reviewed_count,
            start_time=start_time,
            end_time=end_time
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch statistics: {str(e)}"
        )
