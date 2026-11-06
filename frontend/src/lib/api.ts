const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type ContentItem = {
  id: string;
  title: string;
  pillar: string;
  format: string;
  slot: string;
  publish_date: string;
  hook: string;
  script: string;
  caption_instagram: string;
  caption_youtube: string;
  visual_direction: string;
  sources_notes: string;
  duration_sec: number;
  status: string;
};

export type CalendarDay = {
  date: string;
  weekday: string;
  morning: ContentItem | null;
  evening: ContentItem | null;
};

export type PublishingCalendar = {
  channel_id: string;
  timezone: string;
  generated_at: string;
  days: CalendarDay[];
  notes: string[];
};

export async function fetchCalendar(): Promise<PublishingCalendar> {
  const res = await fetch(`${API_BASE}/api/channels/asr-labs/calendar`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Calendar unavailable (${res.status}). Generate it from the API first.`);
  }
  return res.json();
}
