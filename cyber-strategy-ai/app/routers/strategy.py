from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
from app.core.config import get_settings
from app.models.schemas import (
    StrategyRunRequest,
    ClarifyRequest,
)
from app.services.strategy_analysis_service import run_strategy_analysis
from app.services.result_store import get_all_results, get_result
from app.services.report_service import generate_html_report
from app.services.powerpoint_service import (
    generate_initiative_slides_ppt_from_result,
)

router = APIRouter(prefix="/strategy", tags=["Strategy"])


@router.post("/run", summary="Run AI cyber strategy analysis")
def run_analysis(request: StrategyRunRequest):
    result = run_strategy_analysis(
        analysis_name=request.analysis_name,
        business_context=request.business_context,
        focus_areas=request.focus_areas,
        top_k=request.top_k,
    )
    return result


@router.get("/results", summary="List all strategy results")
def list_results():
    return get_all_results()


@router.get("/results/{result_id}", summary="Get a specific strategy result")
def get_result_by_id(result_id: str):
    result = get_result(result_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Result '{result_id}' not found.")
    return result


@router.get(
    "/results/{result_id}/report",
    response_class=HTMLResponse,
    summary="Render a board-ready HTML report for a strategy result",
)
def get_html_report(result_id: str):
    result = get_result(result_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Result '{result_id}' not found.")
    return HTMLResponse(content=generate_html_report(result))


@router.get(
    "/results/{result_id}/powerpoint/initiative-slide",
    summary="Generate initiative slide PowerPoint from a saved strategy result",
)
def create_initiative_slide_from_result(result_id: str):
    result = get_result(result_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Result '{result_id}' not found.")

    try:
        ppt_bytes, file_name = generate_initiative_slides_ppt_from_result(result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return StreamingResponse(
        iter([ppt_bytes]),
        media_type=(
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        ),
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


@router.post("/clarify", summary="Submit clarification answers and re-run analysis")
def clarify(request: ClarifyRequest):
    """
    Incorporate human-provided clarification answers by appending them to the
    business context and re-running the analysis pipeline.
    """
    # Build enriched context from Q&A pairs
    qa_text = "\n".join(
        f"Q: {a.question}\nA: {a.answer}" for a in request.answers
    )
    enriched_context = f"[Clarification Answers]\n{qa_text}"

    settings = get_settings()
    result = run_strategy_analysis(
        analysis_name=request.analysis_name,
        business_context=enriched_context,
        focus_areas=[],
        top_k=settings.default_top_k,
    )
    return result
