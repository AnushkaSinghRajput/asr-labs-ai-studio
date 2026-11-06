"""Content job models and state machine for ASR LABS."""

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ContentStatus(str, Enum):
    IDEA = "IDEA"
    RESEARCH = "RESEARCH"
    RESEARCH_APPROVED = "RESEARCH_APPROVED"
    BRIEF_READY = "BRIEF_READY"
    IN_PRODUCTION = "IN_PRODUCTION"
    QA_REVIEW = "QA_REVIEW"
    REVISION_REQUIRED = "REVISION_REQUIRED"
    AWAITING_FOUNDER = "AWAITING_FOUNDER"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"


ALLOWED_TRANSITIONS: dict[ContentStatus, set[ContentStatus]] = {
    ContentStatus.IDEA: {ContentStatus.RESEARCH, ContentStatus.FAILED},
    ContentStatus.RESEARCH: {
        ContentStatus.RESEARCH_APPROVED,
        ContentStatus.REVISION_REQUIRED,
        ContentStatus.FAILED,
    },
    ContentStatus.RESEARCH_APPROVED: {ContentStatus.BRIEF_READY, ContentStatus.FAILED},
    ContentStatus.BRIEF_READY: {ContentStatus.IN_PRODUCTION, ContentStatus.FAILED},
    ContentStatus.IN_PRODUCTION: {ContentStatus.QA_REVIEW, ContentStatus.FAILED},
    ContentStatus.QA_REVIEW: {
        ContentStatus.AWAITING_FOUNDER,
        ContentStatus.REVISION_REQUIRED,
        ContentStatus.FAILED,
    },
    ContentStatus.REVISION_REQUIRED: {
        ContentStatus.RESEARCH,
        ContentStatus.IN_PRODUCTION,
        ContentStatus.FAILED,
    },
    ContentStatus.AWAITING_FOUNDER: {
        ContentStatus.APPROVED,
        ContentStatus.REVISION_REQUIRED,
        ContentStatus.FAILED,
    },
    ContentStatus.APPROVED: {ContentStatus.SCHEDULED, ContentStatus.FAILED},
    ContentStatus.SCHEDULED: {ContentStatus.PUBLISHED, ContentStatus.FAILED},
    ContentStatus.PUBLISHED: set(),
    ContentStatus.FAILED: {ContentStatus.IDEA, ContentStatus.RESEARCH},
}


class PlatformTarget(str, Enum):
    YOUTUBE_SHORTS = "youtube_shorts"
    INSTAGRAM_REELS = "instagram_reels"


class Slot(str, Enum):
    MORNING = "08:00"
    EVENING = "20:00"


class ContentItem(BaseModel):
    id: str
    channel_id: str = "asr-labs"
    title: str
    pillar: str
    format: str
    slot: Slot
    publish_date: date
    platforms: list[PlatformTarget] = Field(
        default_factory=lambda: [
            PlatformTarget.YOUTUBE_SHORTS,
            PlatformTarget.INSTAGRAM_REELS,
        ]
    )
    status: ContentStatus = ContentStatus.BRIEF_READY
    hook: str
    script: str
    caption_instagram: str
    caption_youtube: str
    hashtags: list[str] = Field(default_factory=list)
    visual_direction: str
    sources_notes: str = ""
    cta: str = "Follow ASR LABS for ideas that shape tomorrow."
    duration_sec: int = 45
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)


class CalendarDay(BaseModel):
    date: date
    weekday: str
    morning: ContentItem | None = None
    evening: ContentItem | None = None


class PublishingCalendar(BaseModel):
    channel_id: str = "asr-labs"
    timezone: str = "Asia/Kolkata"
    generated_at: datetime
    days: list[CalendarDay]
    notes: list[str] = Field(default_factory=list)
