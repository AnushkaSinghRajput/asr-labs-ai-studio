"""Load independent channel brand configs from YAML."""

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from app.config import get_settings


def _channels_dir() -> Path:
    return Path(get_settings().channels_dir)


@lru_cache
def list_channel_ids() -> tuple[str, ...]:
    directory = _channels_dir()
    if not directory.exists():
        return ()
    return tuple(sorted(p.stem for p in directory.glob("*.yaml")))


@lru_cache
def load_channel(channel_id: str) -> dict[str, Any]:
    path = _channels_dir() / f"{channel_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Channel config not found: {channel_id}")
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if data.get("id") != channel_id:
        data["id"] = channel_id
    return data


def load_all_channels() -> list[dict[str, Any]]:
    return [load_channel(channel_id) for channel_id in list_channel_ids()]
