from pydantic import BaseModel, Field

from models.enums import ReviewStatus


class ClaimPRRequest(BaseModel):
    user_id: str = Field(..., description="GitHub user ID of the reviewer")
    pr_id: int = Field(..., description="ID of the pull request to claim")


class ClaimPRResponse(BaseModel):
    success: bool
    message: str
    review_id: int | None = None
    status: ReviewStatus | None = None


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None


class StatsResponse(BaseModel):
    """Response model for analytics statistics"""
    claimable_total_value: float = Field(..., description="Total dollar value of claimable PRs")
    claimable_pr_count: int = Field(..., description="Number of claimable PRs")
    claimed_total_value: float = Field(..., description="Total dollar value of claimed PRs")
    claimed_pr_count: int = Field(..., description="Number of claimed PRs")
    total_prs_reviewed: int = Field(..., description="Total number of PRs reviewed (done status)")
    start_time: str = Field(..., description="Start time of the query period")
    end_time: str = Field(..., description="End time of the query period")
