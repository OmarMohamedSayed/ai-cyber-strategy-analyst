from app.repositories.json_repository import JsonRepository
from app.core.config import get_settings


def _repo() -> JsonRepository:
    settings = get_settings()
    return JsonRepository(f"{settings.data_dir}/strategy_results.json")


def save_result(result: dict) -> dict:
    return _repo().insert(result)


def get_all_results() -> list[dict]:
    return _repo().all()


def get_result(result_id: str) -> dict | None:
    return _repo().get("result_id", result_id)


def update_result(result_id: str, updates: dict) -> dict | None:
    return _repo().update("result_id", result_id, updates)
