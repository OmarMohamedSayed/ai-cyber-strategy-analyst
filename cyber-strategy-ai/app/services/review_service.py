from fastapi import HTTPException
from app.services.result_store import get_result, update_result

VALID_STATUSES = {"approved", "rejected", "needs_review"}


def apply_review(result_id: str, reviewer_name: str, status: str, comments: str) -> dict:
    if status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{status}'. Must be one of: {VALID_STATUSES}",
        )

    result = get_result(result_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Result '{result_id}' not found.")

    updates = {
        "status": status,
        "review": {
            "reviewer_name": reviewer_name,
            "status": status,
            "comments": comments,
        },
    }
    updated = update_result(result_id, updates)
    return updated
