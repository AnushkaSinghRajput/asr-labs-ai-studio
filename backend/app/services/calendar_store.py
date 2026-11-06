"""Persist and load publishing calendars as JSON under storage/."""

import json
from pathlib import Path

from app.config import get_settings
from app.models.content import PublishingCalendar


def calendar_path() -> Path:
    return Path(get_settings().calendar_path)


def save_calendar(calendar: PublishingCalendar) -> Path:
    path = calendar_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        calendar.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return path


def load_calendar() -> PublishingCalendar | None:
    path = calendar_path()
    if not path.exists():
        return None
    return PublishingCalendar.model_validate_json(path.read_text(encoding="utf-8"))
