from fastapi import APIRouter
from app.models.schemas import ReviewRequest
from app.services.review_service import apply_review

router = APIRouter(prefix="/strategy", tags=["Review"])


@router.post(
    "/results/{result_id}/review",
    summary="Submit human review for a strategy result",
)
def review_result(result_id: str, request: ReviewRequest):
    updated = apply_review(
        result_id=result_id,
        reviewer_name=request.reviewer_name,
        status=request.status,
        comments=request.comments or "",
    )
    return {
        "message": f"Result '{result_id}' updated to '{request.status}'.",
        "result": updated,
    }
