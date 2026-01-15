import logging
from typing import Any, cast

from supabase import Client

from models.enums import ReviewStatus
from models.webhook import PullRequestWebhookPayload, GitHubUser

logger = logging.getLogger(__name__)


def upsert_user(db: Client, user: GitHubUser) -> None:
    db.table("users").upsert(
        {"github_user_id": str(user.id), "username": user.login},
        on_conflict="github_user_id",
    ).execute()


def upsert_pull_request(db: Client, payload: PullRequestWebhookPayload) -> int:
    pr = payload.pull_request
    result = db.table("pull_requests").upsert(
        {"title": pr.title, "body": pr.body, "url": pr.html_url},
        on_conflict="url",
    ).execute()

    data = cast(list[dict[str, Any]], result.data or [])
    if data:
        return int(data[0]["id"])

    fetch_result = db.table("pull_requests").select("id").eq("url", pr.html_url).execute()
    fetch_data = cast(list[dict[str, Any]], fetch_result.data or [])
    return int(fetch_data[0]["id"])


def handle_pr_opened(db: Client, payload: PullRequestWebhookPayload) -> None:
    pr = payload.pull_request
    upsert_user(db, pr.user)
    upsert_pull_request(db, payload)
    logger.info("PR #%d opened by %s", pr.number, pr.user.login)


def handle_pr_closed(db: Client, payload: PullRequestWebhookPayload) -> None:
    pr = payload.pull_request

    pr_result = db.table("pull_requests").select("id").eq("url", pr.html_url).execute()
    pr_data = cast(list[dict[str, Any]], pr_result.data or [])
    if not pr_data:
        logger.warning("PR not found: %s", pr.html_url)
        return

    pr_id = pr_data[0]["id"]
    new_status = ReviewStatus.CLAIMABLE if pr.merged else ReviewStatus.INELIGIBLE

    (
        db.table("user_pr_reviews")
        .update({"status": new_status.value})
        .eq("pr_id", pr_id)
        .eq("status", ReviewStatus.REQUESTED.value)
        .execute()
    )

    logger.info("PR #%d %s", pr.number, "merged" if pr.merged else "closed")


def handle_review_requested(db: Client, payload: PullRequestWebhookPayload) -> None:
    pr = payload.pull_request
    reviewer = payload.requested_reviewer

    if not reviewer:
        logger.warning("No reviewer in review_requested for PR #%d", pr.number)
        return

    upsert_user(db, reviewer)
    pr_id = upsert_pull_request(db, payload)

    db.table("user_pr_reviews").upsert(
        {
            "user_id": str(reviewer.id),
            "pr_id": pr_id,
            "status": ReviewStatus.REQUESTED.value,
            "payout": 0.00,
        },
        on_conflict="user_id,pr_id",
    ).execute()

    logger.info("Review requested: %s for PR #%d", reviewer.login, pr.number)
