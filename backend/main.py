import logging

from fastapi import FastAPI

from models.webhook import PRAction, PullRequestWebhookPayload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/webhooks/github/pull-request")
async def handle_github_pr_webhook(payload: PullRequestWebhookPayload):
    try:
        action = PRAction(payload.action)
    except ValueError:
        logger.debug("Ignoring action: %s", payload.action)
        return {"status": "ignored", "action": payload.action}

    pr = payload.pull_request

    match action:
        case PRAction.OPENED:
            logger.info(
                "PR #%d opened: %s by %s — %s",
                pr.number,
                pr.title,
                pr.user.login,
                pr.html_url,
            )

        case PRAction.CLOSED:
            if pr.merged:
                logger.info(
                    "PR #%d merged at %s — %s",
                    pr.number,
                    pr.merged_at,
                    pr.html_url,
                )
            else:
                logger.info(
                    "PR #%d closed at %s — %s",
                    pr.number,
                    pr.closed_at,
                    pr.html_url,
                )

        case PRAction.REVIEW_REQUESTED:
            reviewer = payload.requested_reviewer
            logger.info(
                "PR #%d review requested from %s (id: %s) — %s",
                pr.number,
                reviewer.login if reviewer else "unknown",
                reviewer.id if reviewer else "unknown",
                pr.html_url,
            )

    return {"status": "processed", "action": action, "pr_number": pr.number}
