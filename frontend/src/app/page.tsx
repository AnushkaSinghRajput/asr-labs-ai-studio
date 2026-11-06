import { fetchCalendar, type ContentItem } from "@/lib/api";

export const dynamic = "force-dynamic";

function SlotCard({ label, item }: { label: string; item: ContentItem | null }) {
  if (!item) {
    return (
      <article className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 opacity-50">
        <p className="text-xs uppercase tracking-[0.2em] text-[var(--soft-gold)]">{label}</p>
        <p className="mt-3 text-sm text-white/60">No item scheduled</p>
      </article>
    );
  }

  return (
    <article className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 shadow-[0_0_0_1px_rgba(109,74,255,0.12)]">
      <div className="flex items-start justify-between gap-3">
        <p className="text-xs uppercase tracking-[0.2em] text-[var(--soft-gold)]">{label}</p>
        <span className="rounded-full bg-[var(--deep-violet)]/25 px-2.5 py-1 text-[10px] uppercase tracking-wide text-[var(--electric-lavender)]">
          {item.status}
        </span>
      </div>
      <h3 className="mt-3 font-[family-name:var(--font-display)] text-lg leading-snug text-white">
        {item.title}
      </h3>
      <p className="mt-2 text-sm text-white/70">{item.hook}</p>
      <dl className="mt-4 grid grid-cols-2 gap-2 text-xs text-white/55">
        <div>
          <dt className="uppercase tracking-wider text-white/35">Pillar</dt>
          <dd className="mt-1 text-white/80">{item.pillar}</dd>
        </div>
        <div>
          <dt className="uppercase tracking-wider text-white/35">Length</dt>
          <dd className="mt-1 text-white/80">~{item.duration_sec}s</dd>
        </div>
      </dl>
      <div className="mt-4 space-y-3 border-t border-white/10 pt-4 text-sm">
        <div>
          <p className="text-[11px] uppercase tracking-wider text-[var(--signal-blue)]">Instagram</p>
          <p className="mt-1 whitespace-pre-wrap text-white/75">{item.caption_instagram}</p>
        </div>
        <div>
          <p className="text-[11px] uppercase tracking-wider text-[var(--signal-blue)]">YouTube Shorts</p>
          <p className="mt-1 whitespace-pre-wrap text-white/75">{item.caption_youtube}</p>
        </div>
      </div>
    </article>
  );
}

export default async function HomePage() {
  let calendar = null;
  let error: string | null = null;

  try {
    calendar = await fetchCalendar();
  } catch (err) {
    error = err instanceof Error ? err.message : "Failed to load calendar";
  }

  return (
    <main className="relative min-h-screen overflow-hidden">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_rgba(109,74,255,0.22),_transparent_55%),radial-gradient(ellipse_at_bottom_right,_rgba(76,141,255,0.12),_transparent_40%)]"
      />
      <div className="relative mx-auto max-w-6xl px-6 pb-20 pt-12">
        <header className="max-w-3xl">
          <p className="text-xs uppercase tracking-[0.35em] text-[var(--electric-lavender)]">
            Founder OS
          </p>
          <h1 className="mt-3 font-[family-name:var(--font-display)] text-4xl font-semibold tracking-tight text-white md:text-5xl">
            ASR LABS
          </h1>
          <p className="mt-4 max-w-xl text-base text-white/70 md:text-lg">
            Ideas that shape tomorrow — daily educational Shorts for Instagram and YouTube.
            Review scripts, captions, and slots before you approve anything public.
          </p>
        </header>

        {error ? (
          <div className="mt-10 rounded-2xl border border-amber-400/30 bg-amber-400/10 p-6 text-amber-100">
            <p className="font-medium">Calendar not loaded</p>
            <p className="mt-2 text-sm opacity-90">{error}</p>
            <p className="mt-3 text-sm opacity-80">
              Start the API, then{" "}
              <code className="rounded bg-black/30 px-1.5 py-0.5">
                POST /api/channels/asr-labs/calendar/generate
              </code>
            </p>
          </div>
        ) : null}

        {calendar ? (
          <>
            <section className="mt-10 flex flex-wrap items-center gap-3 text-sm text-white/60">
              <span className="rounded-full border border-white/15 px-3 py-1">
                {calendar.timezone}
              </span>
              <span className="rounded-full border border-white/15 px-3 py-1">
                {calendar.days.length} days · dual slots
              </span>
              <span className="rounded-full border border-white/15 px-3 py-1">
                IG Reels + YT Shorts
              </span>
            </section>

            <section className="mt-6 space-y-2 text-sm text-white/55">
              {calendar.notes.map((note) => (
                <p key={note}>• {note}</p>
              ))}
            </section>

            <section className="mt-12 space-y-10">
              {calendar.days.map((day) => (
                <div key={day.date}>
                  <h2 className="font-[family-name:var(--font-display)] text-xl text-white">
                    {day.weekday}{" "}
                    <span className="text-white/45">{day.date}</span>
                  </h2>
                  <div className="mt-4 grid gap-4 md:grid-cols-2">
                    <SlotCard label="08:00 IST · Discovery" item={day.morning} />
                    <SlotCard label="20:00 IST · Story" item={day.evening} />
                  </div>
                </div>
              ))}
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}
