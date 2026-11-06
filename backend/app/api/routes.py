"""Founder-facing API routes."""

from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.services.asr_labs_planner import (
    calendar_to_markdown,
    generate_asr_labs_calendar,
)
from app.services.calendar_store import load_calendar, save_calendar
from app.services.channels import list_channel_ids, load_all_channels, load_channel

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "asr-labs-ai-studio"}


@router.get("/channels")
def get_channels() -> dict:
    return {"channels": load_all_channels()}


@router.get("/channels/{channel_id}")
def get_channel(channel_id: str) -> dict:
    try:
        return load_channel(channel_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/channels/asr-labs/calendar/generate")
def generate_calendar(
    start: date | None = Query(
        default=None,
        description="First publish date (YYYY-MM-DD). Defaults to today.",
    ),
) -> dict:
    if "asr-labs" not in list_channel_ids():
        raise HTTPException(status_code=404, detail="asr-labs channel config missing")
    calendar = generate_asr_labs_calendar(start=start)
    path = save_calendar(calendar)
    md = calendar_to_markdown(calendar)
    md_path = path.with_suffix(".md")
    md_path.write_text(md, encoding="utf-8")
    return {
        "saved_json": str(path),
        "saved_markdown": str(md_path),
        "calendar": calendar.model_dump(mode="json"),
    }


@router.get("/channels/asr-labs/calendar")
def get_calendar() -> dict:
    calendar = load_calendar()
    if calendar is None:
        raise HTTPException(
            status_code=404,
            detail="No calendar yet. POST /channels/asr-labs/calendar/generate first.",
        )
    return calendar.model_dump(mode="json")


@router.get("/channels/asr-labs/calendar/markdown")
def get_calendar_markdown() -> dict:
    calendar = load_calendar()
    if calendar is None:
        raise HTTPException(status_code=404, detail="No calendar yet.")
    return {"markdown": calendar_to_markdown(calendar)}
