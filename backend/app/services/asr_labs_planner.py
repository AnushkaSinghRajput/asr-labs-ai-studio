"""
ASR LABS editorial planner.

Generates a research-led 14-day dual-slot calendar (08:00 + 20:00 IST)
for YouTube Shorts and Instagram Reels. Content is curated for accuracy
and brand fit; LLM enrichment can replace stubs later via agents/.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from uuid import uuid4

from app.models.content import (
    CalendarDay,
    ContentItem,
    ContentStatus,
    PlatformTarget,
    PublishingCalendar,
    Slot,
)

CHANNEL_ID = "asr-labs"
HASHTAGS = [
    "#ASRLABS",
    "#AI",
    "#Science",
    "#WomenInSTEM",
    "#EmergingTech",
    "#LearnOnReels",
    "#YouTubeShorts",
]


def _item(
    *,
    publish_date: date,
    slot: Slot,
    title: str,
    pillar: str,
    format_id: str,
    hook: str,
    script: str,
    caption_instagram: str,
    caption_youtube: str,
    visual_direction: str,
    sources_notes: str,
    duration_sec: int,
    cta: str = "Save this. Follow ASR LABS for ideas that shape tomorrow.",
) -> ContentItem:
    return ContentItem(
        id=f"asr-{publish_date.isoformat()}-{slot.value.replace(':', '')}-{uuid4().hex[:6]}",
        channel_id=CHANNEL_ID,
        title=title,
        pillar=pillar,
        format=format_id,
        slot=slot,
        publish_date=publish_date,
        platforms=[PlatformTarget.YOUTUBE_SHORTS, PlatformTarget.INSTAGRAM_REELS],
        status=ContentStatus.BRIEF_READY,
        hook=hook,
        script=script,
        caption_instagram=caption_instagram,
        caption_youtube=caption_youtube,
        hashtags=HASHTAGS,
        visual_direction=visual_direction,
        sources_notes=sources_notes,
        cta=cta,
        duration_sec=duration_sec,
    )


def _seed_plan(start: date) -> list[tuple[date, Slot, dict]]:
    """Editorial seed for 14 days × 2 slots. Morning = discovery; evening = story/depth."""
    # (day_offset, slot, payload) — day_offset 0..13
    specs: list[tuple[int, Slot, dict]] = [
        # Day 0 — Sat buffer / start
        (
            0,
            Slot.MORNING,
            dict(
                title="What is an AI agent — in 45 seconds",
                pillar="ai-decoded",
                format_id="explainer-60",
                hook="An AI chatbot answers. An AI agent acts.",
                script=(
                    "HOOK: An AI chatbot answers. An AI agent acts.\n"
                    "CONTEXT: Most people mix these up.\n"
                    "CORE: A chatbot predicts the next words. An agent can plan steps, "
                    "use tools, check results, and keep going until a goal is done — "
                    "like booking, researching, or updating a file.\n"
                    "MEANING: Agents need clear goals, guardrails, and human approval for risky actions.\n"
                    "CTA: Follow ASR LABS — we decode AI without the hype."
                ),
                caption_instagram=(
                    "Chatbot ≠ Agent.\n\n"
                    "One replies. The other can take steps toward a goal — with tools and checks.\n\n"
                    "Would you trust an agent with your calendar yet? Comment yes/no.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "What is an AI agent? Clear difference from a chatbot — ASR LABS.\n\n"
                    "Sources: general ML systems design; agent = LLM + tools + loop + goals.\n\n"
                    "{hashtags}"
                ),
                visual_direction=(
                    "Midnight ink background. Simple diagram: Chat bubble vs loop with "
                    "tools icons. Deep violet accents. Burned-in captions. Soft gold on key words."
                ),
                sources_notes="Conceptual explainer — no unverifiable stats. Keep definitions conservative.",
                duration_sec=45,
            ),
        ),
        (
            0,
            Slot.EVENING,
            dict(
                title="Zhenan Bao — the scientist teaching skin to sense",
                pillar="women-who-built-the-future",
                format_id="innovator-profile",
                hook="What if a robot hand could feel as gently as human skin?",
                script=(
                    "HOOK: What if a robot hand could feel as gently as human skin?\n"
                    "PERSON: Meet Zhenan Bao — Stanford chemical engineer working on electronic skin.\n"
                    "PROBLEM: Machines are strong, but touch and soft sensing are hard.\n"
                    "CONTRIBUTION: Her lab builds flexible, skin-like sensors for pressure, "
                    "temperature and more — toward better prosthetics and human-robot interaction.\n"
                    "WHY IT MATTERS: The future of AI isn't only in the cloud — it's also in materials that sense the world.\n"
                    "CTA: Women Who Built the Future — every week on ASR LABS."
                ),
                caption_instagram=(
                    "Zhenan Bao · Stanford\n\n"
                    "Building electronic skin so machines can sense more like we do.\n\n"
                    "AI needs better bodies — not just bigger models.\n\n"
                    "Who should we profile next?\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Zhenan Bao — Stanford scientist working on electronic skin and soft sensing. "
                    "Part of ASR LABS: Women Who Built the Future.\n\n"
                    "Verify latest lab work via Stanford profiles / peer-reviewed papers before final cut.\n\n"
                    "{hashtags}"
                ),
                visual_direction=(
                    "Lab / material close-ups (licensed or clearly illustrative + AI-labelled). "
                    "Name card: ZHENAN BAO — STANFORD. Editorial typography. No fake documentary stills."
                ),
                sources_notes=(
                    "Confirm bio details from Stanford ChemE / Bao Group site and recent papers. "
                    "Label illustrative AI imagery."
                ),
                duration_sec=60,
            ),
        ),
        # Day 1
        (
            1,
            Slot.MORNING,
            dict(
                title="Tokens: why AI 'reads' in chunks",
                pillar="ai-decoded",
                format_id="explainer-60",
                hook="AI doesn't read letters. It reads tokens.",
                script=(
                    "HOOK: AI doesn't read letters. It reads tokens.\n"
                    "CONTEXT: That's why long prompts cost more and hit limits.\n"
                    "CORE: Text is split into tokens — pieces of words. Models predict the next token. "
                    "Rough rule of thumb: English ≈ a few characters per token, but it varies by language and model.\n"
                    "MEANING: Shorter clear prompts often work better than long vague ones.\n"
                    "CTA: ASR LABS — practical AI, no fluff."
                ),
                caption_instagram=(
                    "Tokens = the units AI thinks in.\n\n"
                    "That's why length limits and pricing talk about tokens, not pages.\n\n"
                    "Save for your next prompt.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "What are tokens in AI? Quick explainer — ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Animated text splitting into token chips. Signal blue highlights. Clean grid.",
                sources_notes="Avoid exact token prices — they change. Keep conceptual.",
                duration_sec=40,
            ),
        ),
        (
            1,
            Slot.EVENING,
            dict(
                title="Ada Lovelace — the first programmer wasn't waiting for computers",
                pillar="women-who-built-the-future",
                format_id="innovator-profile",
                hook="In the 1840s, she saw a machine that could create — not just calculate.",
                script=(
                    "HOOK: In the 1840s, she saw a machine that could create — not just calculate.\n"
                    "PERSON: Ada Lovelace wrote notes on Babbage's Analytical Engine.\n"
                    "CONTRIBUTION: She described how the engine could manipulate symbols — "
                    "an early vision of general computing, not only arithmetic.\n"
                    "WHY IT MATTERS: Programming started as imagination about what machines could mean.\n"
                    "CTA: History that built today's AI — ASR LABS."
                ),
                caption_instagram=(
                    "Ada Lovelace · 1800s\n\n"
                    "She imagined computing beyond numbers — toward creation.\n\n"
                    "The first programmer energy was visionary.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Ada Lovelace and the Analytical Engine — why she's called the first computer programmer. ASR LABS.\n\n"
                    "Primary context: Lovelace's Notes on the Analytical Engine (historical).\n\n{hashtags}"
                ),
                visual_direction=(
                    "Historical document aesthetic with number/year motif (e.g. 1843 era cues). "
                    "Soft gold editorial emphasis. Label period art as historical/illustrative."
                ),
                sources_notes="Use established historical consensus; avoid myth inflation.",
                duration_sec=55,
            ),
        ),
        # Day 2
        (
            2,
            Slot.MORNING,
            dict(
                title="Myth: AI understands you like a person",
                pillar="ai-decoded",
                format_id="myth-vs-fact",
                hook="Myth: ChatGPT understands you. Fact: it predicts patterns.",
                script=(
                    "HOOK: Myth — AI understands you like a friend.\n"
                    "FACT: Large language models predict likely next tokens from patterns in data.\n"
                    "NUANCE: That can look like understanding — and still fail on truth, time, and your private context.\n"
                    "QUESTION: Where do you still want a human in the loop?\n"
                    "CTA: Myth vs Fact — ASR LABS."
                ),
                caption_instagram=(
                    "Myth vs Fact\n\n"
                    "AI can sound wise and still be guessing the next words.\n\n"
                    "Use it. Don't worship it.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Myth: AI understands you. Fact: pattern prediction. ASR LABS Myth vs Fact.\n\n{hashtags}"
                ),
                visual_direction="Split screen MYTH / FACT. Deep violet vs cloud white panels. High-contrast captions.",
                sources_notes="Align with public ML literacy (no invented 'understanding scores').",
                duration_sec=40,
            ),
        ),
        (
            2,
            Slot.EVENING,
            dict(
                title="AI in hospitals: help with eyes, not replace doctors",
                pillar="ai-for-humanity",
                format_id="tech-in-real-life",
                hook="The best medical AI doesn't replace judgment — it sharpens it.",
                script=(
                    "HOOK: The best medical AI doesn't replace judgment — it sharpens it.\n"
                    "PROBLEM: Radiologists face huge image volumes; misses cost lives.\n"
                    "TECH: Computer vision models flag possible findings for human review.\n"
                    "LIMITS: Bias, rare cases, and liability mean clinicians stay accountable.\n"
                    "IMPACT: Faster triage + second look — when deployed carefully.\n"
                    "CTA: AI for Humanity — ASR LABS."
                ),
                caption_instagram=(
                    "AI for Humanity\n\n"
                    "In imaging, AI is often a second set of eyes — not the final word.\n\n"
                    "Would you want AI review on your scan? Why / why not?\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "How AI assists medical imaging — benefits and limits. ASR LABS.\n\n"
                    "Keep claims general; cite a specific peer-reviewed deployment only after research pass.\n\n{hashtags}"
                ),
                visual_direction="Clean diagram: scan → model flag → clinician. Signal blue data cues. No fake patient photos.",
                sources_notes="Research pass required before naming a hospital or study.",
                duration_sec=55,
            ),
        ),
        # Day 3
        (
            3,
            Slot.MORNING,
            dict(
                title="One prompt trick: ask for the audience",
                pillar="ai-decoded",
                format_id="tool-demo",
                hook="Stop prompting for 'a good explanation.' Prompt for who it's for.",
                script=(
                    "HOOK: Stop asking for 'a good explanation.' Name the audience.\n"
                    "STEPS: 1) Role: 'Explain like I'm a curious 16-year-old.' "
                    "2) Goal: 'one analogy + one example.' 3) Constraint: 'no jargon without a definition.'\n"
                    "OUTCOME: Clearer answers in one shot.\n"
                    "CAVEAT: Still verify facts.\n"
                    "CTA: Practical workflows — ASR LABS."
                ),
                caption_instagram=(
                    "Prompt tip\n\n"
                    "Audience + goal + constraint beats 'write something good.'\n\n"
                    "Try it today.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Better AI prompts: specify audience, goal, constraints. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="UI mock of prompt box filling in 3 fields. Electric lavender highlights.",
                sources_notes="Workflow tip — no product endorsement required.",
                duration_sec=35,
            ),
        ),
        (
            3,
            Slot.EVENING,
            dict(
                title="Quantum computing: not a faster laptop",
                pillar="beyond-tomorrow",
                format_id="explainer-60",
                hook="Quantum computers won't replace your Mac. They attack different problems.",
                script=(
                    "HOOK: Quantum computers won't replace your Mac.\n"
                    "CONTEXT: Classical bits are 0 or 1. Qubits can be in superposition — "
                    "useful for specific maths like certain chemistry and optimisation problems.\n"
                    "CORE: They're fragile, error-prone, and still early for most business apps.\n"
                    "MEANING: Hype says 'soon everything.' Reality says 'narrow breakthroughs first.'\n"
                    "CTA: Beyond Tomorrow — ASR LABS."
                ),
                caption_instagram=(
                    "Beyond Tomorrow\n\n"
                    "Quantum ≠ faster laptop.\n"
                    "It's a different kind of machine for hard scientific problems.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Quantum computing explained simply — what it is and isn't. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Orbital/circuit motif restrained. Qubit vs bit comparison graphic.",
                sources_notes="Keep non-sensational; no fake timeline promises.",
                duration_sec=50,
            ),
        ),
        # Day 4
        (
            4,
            Slot.MORNING,
            dict(
                title="Hallucinations: why models invent facts",
                pillar="ai-decoded",
                format_id="explainer-60",
                hook="AI can sound 100% sure — and still be wrong.",
                script=(
                    "HOOK: AI can sound certain and still invent a citation.\n"
                    "WHY: Models optimise for plausible language, not a live truth database.\n"
                    "FIX: Ask for sources, check primary docs, use tools that retrieve real pages.\n"
                    "RULE: If a claim matters, verify before you share.\n"
                    "CTA: Research-led AI literacy — ASR LABS."
                ),
                caption_instagram=(
                    "If it matters, verify.\n\n"
                    "Fluent ≠ true.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Why AI hallucinates — and how to reduce risk. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Confident caption overlay then red 'CHECK SOURCE' stamp. Soft gold for rule line.",
                sources_notes="Standard LLM limitation literacy.",
                duration_sec=40,
            ),
        ),
        (
            4,
            Slot.EVENING,
            dict(
                title="Fei-Fei Li — teaching machines to see",
                pillar="women-who-built-the-future",
                format_id="innovator-profile",
                hook="Modern computer vision stands on a dataset she helped champion: ImageNet.",
                script=(
                    "HOOK: Modern computer vision stands on ImageNet — and Fei-Fei Li helped drive that vision.\n"
                    "CONTEXT: To learn recognition, models needed massive labelled images.\n"
                    "CONTRIBUTION: ImageNet fuelled breakthroughs in deep learning for vision.\n"
                    "WHY IT MATTERS: Seeing systems power medicine, cars, accessibility — and need ethical care.\n"
                    "CTA: Women Who Built the Future — ASR LABS."
                ),
                caption_instagram=(
                    "Fei-Fei Li\n\n"
                    "Helped push ImageNet — a foundation for how machines learn to see.\n\n"
                    "Vision AI started with ambitious data + science.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Fei-Fei Li and ImageNet — why computer vision leapt forward. ASR LABS.\n\n"
                    "Confirm details via Stanford / HAI materials in research pass.\n\n{hashtags}"
                ),
                visual_direction="Grid of abstract image tiles → model label. Name plate. Editorial, not celebrity tabloid.",
                sources_notes="Research pass for exact roles/years before publish.",
                duration_sec=55,
            ),
        ),
        # Day 5
        (
            5,
            Slot.MORNING,
            dict(
                title="RAG in plain English",
                pillar="ai-decoded",
                format_id="explainer-60",
                hook="Want fewer made-up answers? Give the model documents to look at.",
                script=(
                    "HOOK: Want fewer made-up answers? Retrieve first, then generate.\n"
                    "CORE: RAG = Retrieval-Augmented Generation. Find relevant docs → stuff them into context → answer with citations.\n"
                    "EXAMPLE: Company policy bot that searches your handbook before replying.\n"
                    "LIMIT: Bad retrieval still yields bad answers.\n"
                    "CTA: AI Decoded — ASR LABS."
                ),
                caption_instagram=(
                    "RAG = search, then answer.\n\n"
                    "Not magic. Better plumbing.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "RAG explained in plain English. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="3-step pipeline graphic: Docs → Retrieve → Generate. Signal blue arrows.",
                sources_notes="Conceptual; no vendor lock-in.",
                duration_sec=45,
            ),
        ),
        (
            5,
            Slot.EVENING,
            dict(
                title="Climate models meet machine learning",
                pillar="ai-for-humanity",
                format_id="research-brief",
                hook="AI isn't only chatbots — it's helping scientists read the planet faster.",
                script=(
                    "HOOK: AI isn't only chatbots — it's helping scientists read the planet faster.\n"
                    "WHAT: ML assists with satellite imagery, extreme-event patterns, and speeding parts of simulation workflows.\n"
                    "UNKNOWN: Climate systems are complex; models need careful validation.\n"
                    "WHY CARE: Better forecasts and monitoring can guide adaptation — if we stay rigorous.\n"
                    "CTA: AI for Humanity — ASR LABS."
                ),
                caption_instagram=(
                    "AI for the planet\n\n"
                    "From satellites to simulations — ML is a tool for climate science, not a silver bullet.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "How machine learning supports climate and Earth observation — carefully. ASR LABS.\n\n"
                    "Attach 1–2 primary papers/org links after research pass.\n\n{hashtags}"
                ),
                visual_direction="Earth / grid data aesthetic restrained. No disaster porn. Soft gold for 'validate' line.",
                sources_notes="Must attach real sources before APPROVED.",
                duration_sec=55,
            ),
        ),
        # Day 6
        (
            6,
            Slot.MORNING,
            dict(
                title="Temperature in AI: creativity dial",
                pillar="ai-decoded",
                format_id="explainer-60",
                hook="Same model. Different 'temperature.' Totally different vibe.",
                script=(
                    "HOOK: Same model. Twist the temperature. Different vibe.\n"
                    "CORE: Lower temperature → more focused, repetitive-safe answers. "
                    "Higher → more varied, riskier wording.\n"
                    "USE: Drafts & brainstorming higher; facts & code often lower.\n"
                    "CTA: Tiny settings, big difference — ASR LABS."
                ),
                caption_instagram=(
                    "Temperature = creativity dial.\n\n"
                    "Facts? Turn it down. Brainstorm? Turn it up.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "What is temperature in AI models? ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Dial UI animation. Deep violet knob. Captions burned in.",
                sources_notes="Provider UIs differ; keep conceptual.",
                duration_sec=35,
            ),
        ),
        (
            6,
            Slot.EVENING,
            dict(
                title="Founder Journal: why ASR LABS publishes twice a day",
                pillar="founder-journal",
                format_id="quiet-story",
                hook="Consistency builds trust. Research earns it.",
                script=(
                    "HOOK: Consistency builds habit. Research earns trust.\n"
                    "STORY: ASR LABS is building an operating system for educational media — "
                    "two original shorts a day, with human approval before anything goes public.\n"
                    "LESSON: Cadence without quality is noise. Quality without cadence is a hobby.\n"
                    "CTA: Follow the build in public — ASR LABS."
                ),
                caption_instagram=(
                    "Founder Journal\n\n"
                    "Two useful videos a day — not two videos to fill a schedule.\n\n"
                    "We're building the machine that makes that possible.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Why ASR LABS publishes at 08:00 and 20:00 IST — Founder Journal.\n\n{hashtags}"
                ),
                visual_direction=(
                    "Branded founder desk / soft nebula background matching IG. "
                    "Logo end card. Honest, not corporate stock."
                ),
                sources_notes="First-party brand story — no external claims needed.",
                duration_sec=45,
            ),
        ),
        # Day 7
        (
            7,
            Slot.MORNING,
            dict(
                title="Open source vs closed AI models",
                pillar="ai-decoded",
                format_id="myth-vs-fact",
                hook="Open weights aren't the same as open everything.",
                script=(
                    "HOOK: 'Open source AI' is a spectrum.\n"
                    "FACT: Some projects release weights you can run locally. Data, training code, and licenses still vary.\n"
                    "TRADEOFF: Open → more control & audit potential. Closed APIs → often stronger hosted performance & safety tooling.\n"
                    "CTA: Choose based on your risk and use case — ASR LABS."
                ),
                caption_instagram=(
                    "Open weights ≠ automatically safe or free forever.\n\n"
                    "Read the license. Know your risk.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Open vs closed AI models — a clear spectrum. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Spectrum bar graphic. Avoid dunking on vendors by name.",
                sources_notes="Keep vendor-neutral.",
                duration_sec=45,
            ),
        ),
        (
            7,
            Slot.EVENING,
            dict(
                title="Chips: why GPUs unlocked modern AI",
                pillar="beyond-tomorrow",
                format_id="explainer-60",
                hook="AI didn't suddenly get smart. Hardware caught up to the maths.",
                script=(
                    "HOOK: AI didn't suddenly get smart. Hardware caught up.\n"
                    "CORE: Training neural nets is massive matrix math. GPUs do that in parallel.\n"
                    "MEANING: Progress is model design + data + compute — not magic.\n"
                    "CTA: Beyond Tomorrow — ASR LABS."
                ),
                caption_instagram=(
                    "GPUs made deep learning practical at scale.\n\n"
                    "Software + silicon together.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Why GPUs matter for AI — short explainer. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Simple parallel cores animation. Technical lines, no product placement.",
                sources_notes="High-level hardware literacy.",
                duration_sec=40,
            ),
        ),
        # Day 8
        (
            8,
            Slot.MORNING,
            dict(
                title="Accessibility: AI that reads the world aloud",
                pillar="ai-for-humanity",
                format_id="tech-in-real-life",
                hook="The most important AI feature might be the one that describes a street for someone who can't see it.",
                script=(
                    "HOOK: AI that describes the world can expand independence.\n"
                    "TECH: On-device and cloud vision models power scene description and text reading.\n"
                    "LIMITS: Errors can mislead — design for confirmation and humility.\n"
                    "IMPACT: Accessibility is innovation, not a niche.\n"
                    "CTA: AI for Humanity — ASR LABS."
                ),
                caption_instagram=(
                    "AI for accessibility\n\n"
                    "Describe. Read. Navigate — with humans in the loop.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "How AI supports accessibility — benefits and limits. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Inclusive, calm visuals. No pity framing. High-contrast captions.",
                sources_notes="Prefer citing established a11y AI features after research pass.",
                duration_sec=50,
            ),
        ),
        (
            8,
            Slot.EVENING,
            dict(
                title="Grace Hopper — the compiler that spoke human",
                pillar="women-who-built-the-future",
                format_id="innovator-profile",
                hook="She believed humans shouldn't speak machine code forever.",
                script=(
                    "HOOK: She believed humans shouldn't speak machine code forever.\n"
                    "PERSON: Grace Hopper pioneered compilers — translating human-readable instructions into machine code.\n"
                    "WHY IT MATTERS: Modern software — and the AI stacks on top — sit on that idea: make machines meet people halfway.\n"
                    "CTA: Women Who Built the Future — ASR LABS."
                ),
                caption_instagram=(
                    "Grace Hopper\n\n"
                    "Compilers made programming human.\n\n"
                    "We still build on her idea.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Grace Hopper and the compiler revolution — ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Retro computing motifs + modern editorial overlay. Soft gold name plate.",
                sources_notes="Historical consensus; avoid apocryphal quotes unless sourced.",
                duration_sec=50,
            ),
        ),
        # Day 9
        (
            9,
            Slot.MORNING,
            dict(
                title="Embeddings: how AI finds 'similar meaning'",
                pillar="ai-decoded",
                format_id="explainer-60",
                hook="Search used to match words. Now it can match meaning.",
                script=(
                    "HOOK: Search used to match words. Now it can match meaning.\n"
                    "CORE: Embeddings turn text into vectors — lists of numbers — so 'car' and 'automobile' land nearby.\n"
                    "USE: Semantic search, recommendations, RAG retrieval.\n"
                    "CTA: AI Decoded — ASR LABS."
                ),
                caption_instagram=(
                    "Embeddings = meaning as maths.\n\n"
                    "That's how semantic search works.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "What are embeddings? Meaning as vectors. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="2D cluster dots for related words. Clean animation.",
                sources_notes="Conceptual.",
                duration_sec=40,
            ),
        ),
        (
            9,
            Slot.EVENING,
            dict(
                title="Robots in warehouses: AI that moves boxes",
                pillar="beyond-tomorrow",
                format_id="tech-in-real-life",
                hook="The quiet AI revolution is happening in logistics aisles.",
                script=(
                    "HOOK: The quiet AI revolution is in logistics aisles.\n"
                    "TECH: Vision + planning help robots navigate and pick in structured spaces.\n"
                    "LIMITS: Open-world homes are harder than warehouses.\n"
                    "MEANING: Robotics progress is uneven — and that's okay to say out loud.\n"
                    "CTA: Beyond Tomorrow — ASR LABS."
                ),
                caption_instagram=(
                    "Warehouse robots ≠ home robots (yet).\n\n"
                    "Structure makes autonomy easier.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Why warehouse robots advanced faster than home robots. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Abstract aisle grid + robot icon. No unverified company claims.",
                sources_notes="Keep general unless citing a specific public system.",
                duration_sec=45,
            ),
        ),
        # Day 10
        (
            10,
            Slot.MORNING,
            dict(
                title="System prompts: the invisible instructions",
                pillar="ai-decoded",
                format_id="tool-demo",
                hook="The most powerful prompt is often the one you never see.",
                script=(
                    "HOOK: The most powerful prompt is often invisible: the system prompt.\n"
                    "CORE: Apps wrap your message with rules — tone, safety, tools, format.\n"
                    "TIP: When building products, put durable rules in the system layer; keep user prompts for the task.\n"
                    "CTA: Practical AI — ASR LABS."
                ),
                caption_instagram=(
                    "System prompt = the app's rulebook.\n\n"
                    "User prompt = today's task.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "What is a system prompt? ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Layers graphic: System / Developer / User. Midnight ink.",
                sources_notes="Product-building literacy.",
                duration_sec=40,
            ),
        ),
        (
            10,
            Slot.EVENING,
            dict(
                title="AI tutors: promise, proof, and pitfalls",
                pillar="ai-for-humanity",
                format_id="research-brief",
                hook="A tutor that never sleeps sounds perfect — until it teaches a wrong step confidently.",
                script=(
                    "HOOK: An always-on tutor sounds perfect — until it teaches a wrong step confidently.\n"
                    "PROMISE: Personalised practice at scale.\n"
                    "PROOF NEEDED: Learning gains must be measured, not assumed.\n"
                    "PITFALLS: Hallucinations, cheating shortcuts, equity of access.\n"
                    "CTA: Hold the optimism and the evidence — ASR LABS."
                ),
                caption_instagram=(
                    "AI tutors\n\n"
                    "Promising. Not automatically proven.\n\n"
                    "Demand evidence.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "AI tutors — promise, proof, pitfalls. ASR LABS.\n\n"
                    "Add citations after research pass.\n\n{hashtags}"
                ),
                visual_direction="Classroom-neutral abstract. Soft gold on 'evidence' word.",
                sources_notes="Attach ed-tech studies before APPROVED.",
                duration_sec=55,
            ),
        ),
        # Day 11
        (
            11,
            Slot.MORNING,
            dict(
                title="Fine-tuning vs prompting",
                pillar="ai-decoded",
                format_id="explainer-60",
                hook="Don't fine-tune what a good prompt + examples can fix.",
                script=(
                    "HOOK: Don't fine-tune what prompting can fix.\n"
                    "PROMPTING: Fast, cheap, flexible — great for style and structure.\n"
                    "FINE-TUNING: Teaches narrower behaviour from many examples — costlier, slower to change.\n"
                    "RULE: Start with prompts and retrieval; fine-tune when you must.\n"
                    "CTA: AI Decoded — ASR LABS."
                ),
                caption_instagram=(
                    "Prompt first.\n"
                    "Retrieve second.\n"
                    "Fine-tune when you must.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Fine-tuning vs prompting — when to use which. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Decision tree graphic. Electric lavender path for 'prompt first'.",
                sources_notes="Engineering best-practice framing.",
                duration_sec=45,
            ),
        ),
        (
            11,
            Slot.EVENING,
            dict(
                title="Katie Bouman and the black hole image moment",
                pillar="women-who-built-the-future",
                format_id="innovator-profile",
                hook="A planet-sized telescope. An algorithm. A first look at a black hole's shadow.",
                script=(
                    "HOOK: A planet-sized telescope. Algorithms. A first look at a black hole's shadow.\n"
                    "CONTEXT: The Event Horizon Telescope combined data from observatories worldwide.\n"
                    "PERSON: Katie Bouman was part of the imaging effort that helped reconstruct the famous image — "
                    "science is team sport; credit the collaboration.\n"
                    "WHY IT MATTERS: Computation turns impossible data into human understanding.\n"
                    "CTA: Women Who Built the Future — ASR LABS."
                ),
                caption_instagram=(
                    "Black hole imaging was a team win.\n\n"
                    "Algorithms + astronomy + collaboration.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Katie Bouman and EHT imaging — credit the science and the team. ASR LABS.\n\n"
                    "Use EHT collaboration materials; avoid single-hero myths.\n\n{hashtags}"
                ),
                visual_direction="Abstract ring/shadow motif (not claiming real EHT plate without rights). Soft gold collaboration line.",
                sources_notes="Emphasise collaboration; verify role wording from EHT/MIT materials.",
                duration_sec=60,
            ),
        ),
        # Day 12
        (
            12,
            Slot.MORNING,
            dict(
                title="Latency vs intelligence: why 'smart' can feel slow",
                pillar="ai-decoded",
                format_id="explainer-60",
                hook="The smartest model isn't always the one you should ship.",
                script=(
                    "HOOK: The smartest model isn't always the one you should ship.\n"
                    "CORE: Bigger models can be slower and costlier. Product UX often needs small/fast models for drafts + big models for hard steps.\n"
                    "PATTERN: Route easy tasks cheaply; escalate hard ones.\n"
                    "CTA: Build like an engineer — ASR LABS."
                ),
                caption_instagram=(
                    "Route easy tasks to fast models.\n"
                    "Escalate the hard ones.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Latency vs intelligence in AI products. ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Router diagram. Signal blue paths.",
                sources_notes="Architecture literacy.",
                duration_sec=40,
            ),
        ),
        (
            12,
            Slot.EVENING,
            dict(
                title="Materials that heal: self-healing tech frontier",
                pillar="beyond-tomorrow",
                format_id="research-brief",
                hook="What if the devices we wear could repair tiny damage — like skin?",
                script=(
                    "HOOK: What if devices could repair tiny damage — like skin?\n"
                    "FIELD: Self-healing polymers and soft materials are an active research frontier "
                    "(including work adjacent to electronic skin and wearable labs).\n"
                    "UNKNOWN: Lab demos ≠ mass-market durability yet.\n"
                    "WHY CARE: Longevity and sustainability need better materials, not only smarter software.\n"
                    "CTA: Beyond Tomorrow — ASR LABS."
                ),
                caption_instagram=(
                    "Self-healing materials\n\n"
                    "Early. Exciting. Not magic yet.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "Self-healing materials — research frontier overview. ASR LABS.\n\n"
                    "Cite specific papers in research pass.\n\n{hashtags}"
                ),
                visual_direction="Macro material texture + crack-heal animation (illustrative, labelled).",
                sources_notes="Must attach papers before APPROVED.",
                duration_sec=50,
            ),
        ),
        # Day 13
        (
            13,
            Slot.MORNING,
            dict(
                title="Eval: how teams know if an AI feature works",
                pillar="ai-decoded",
                format_id="explainer-60",
                hook="If you can't measure it, you can't improve an AI feature.",
                script=(
                    "HOOK: If you can't measure it, you can't improve it.\n"
                    "CORE: Evals = test sets + scoring (exact match, rubrics, human ratings, safety checks).\n"
                    "PRACTICE: Ship a baseline, measure regressions, then change prompts or models.\n"
                    "CTA: Build with evidence — ASR LABS."
                ),
                caption_instagram=(
                    "No evals = vibes-driven AI.\n\n"
                    "Measure. Then ship.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "What are AI evals? ASR LABS.\n\n{hashtags}"
                ),
                visual_direction="Checklist / scorecard UI. Soft gold pass marks.",
                sources_notes="Engineering practice.",
                duration_sec=40,
            ),
        ),
        (
            13,
            Slot.EVENING,
            dict(
                title="Week ahead: what ASR LABS will teach next",
                pillar="founder-journal",
                format_id="quiet-story",
                hook="Next week: sharper explainers, deeper innovator stories, tighter sources.",
                script=(
                    "HOOK: Next week we raise the bar — sharper explainers, deeper stories, tighter sources.\n"
                    "PLAN: Keep 08:00 for learning. Keep 20:00 for meaning. Keep founder approval on every public cut.\n"
                    "ASK: Tell us what confuses you about AI — we'll make a video for it.\n"
                    "CTA: Comment your topic. ASR LABS."
                ),
                caption_instagram=(
                    "Founder Journal\n\n"
                    "What should we explain next?\n"
                    "Drop a topic below.\n\n"
                    "{hashtags}"
                ),
                caption_youtube=(
                    "What's next on ASR LABS — and how to request a topic.\n\n{hashtags}"
                ),
                visual_direction="Calendar + brand end card. Invite comment CTA on screen.",
                sources_notes="First-party.",
                duration_sec=40,
            ),
        ),
    ]

    out: list[tuple[date, Slot, dict]] = []
    for offset, slot, payload in specs:
        out.append((start + timedelta(days=offset), slot, payload))
    return out


def generate_asr_labs_calendar(start: date | None = None) -> PublishingCalendar:
    """Build 14 days × 2 slots for ASR LABS (YouTube Shorts + Instagram Reels)."""
    if start is None:
        start = date.today()

    by_day: dict[date, CalendarDay] = {}
    tag_str = " ".join(HASHTAGS)

    for publish_date, slot, payload in _seed_plan(start):
        captions = {
            "caption_instagram": payload["caption_instagram"].format(hashtags=tag_str),
            "caption_youtube": payload["caption_youtube"].format(hashtags=tag_str),
        }
        item = _item(
            publish_date=publish_date,
            slot=slot,
            title=payload["title"],
            pillar=payload["pillar"],
            format_id=payload["format_id"],
            hook=payload["hook"],
            script=payload["script"],
            caption_instagram=captions["caption_instagram"],
            caption_youtube=captions["caption_youtube"],
            visual_direction=payload["visual_direction"],
            sources_notes=payload["sources_notes"],
            duration_sec=payload["duration_sec"],
        )
        day = by_day.get(publish_date)
        if day is None:
            day = CalendarDay(
                date=publish_date,
                weekday=publish_date.strftime("%A"),
            )
            by_day[publish_date] = day
        if slot == Slot.MORNING:
            day.morning = item
        else:
            day.evening = item

    days = [by_day[d] for d in sorted(by_day)]
    return PublishingCalendar(
        channel_id=CHANNEL_ID,
        timezone="Asia/Kolkata",
        generated_at=datetime.now(timezone.utc),
        days=days,
        notes=[
            "Post the SAME vertical cut on Instagram Reels and YouTube Shorts each slot (adapt caption per platform).",
            "08:00 IST = discovery/learning. 20:00 IST = story/depth.",
            "Do not publish until founder approves the exact final file + captions.",
            "Research-pass items that name living people or papers before APPROVED.",
            "Create YouTube channel ASAP; Instagram @asrlabs.co is already live.",
        ],
    )


def calendar_to_markdown(calendar: PublishingCalendar) -> str:
    lines = [
        f"# ASR LABS — {len(calendar.days)}-day publishing calendar",
        "",
        f"Timezone: **{calendar.timezone}** · Channel: `{calendar.channel_id}`",
        f"Generated: {calendar.generated_at.isoformat()}",
        "",
        "## How to use",
        "",
        "Each day has **two** posts. Publish the same 9:16 video to **Instagram Reels** and **YouTube Shorts**, with platform-specific captions below.",
        "",
    ]
    for note in calendar.notes:
        lines.append(f"- {note}")
    lines.append("")

    for day in calendar.days:
        lines.append(f"## {day.weekday} {day.date.isoformat()}")
        lines.append("")
        for label, item in (("08:00 IST", day.morning), ("20:00 IST", day.evening)):
            if item is None:
                continue
            lines.extend(
                [
                    f"### {label} — {item.title}",
                    "",
                    f"- **Pillar:** `{item.pillar}` · **Format:** `{item.format}` · **~{item.duration_sec}s**",
                    f"- **Hook:** {item.hook}",
                    f"- **Status:** `{item.status.value}`",
                    "",
                    "**Script**",
                    "",
                    "```",
                    item.script,
                    "```",
                    "",
                    "**Visual direction**",
                    "",
                    item.visual_direction,
                    "",
                    "**Instagram caption**",
                    "",
                    item.caption_instagram,
                    "",
                    "**YouTube Shorts caption**",
                    "",
                    item.caption_youtube,
                    "",
                    f"*Sources / QA notes:* {item.sources_notes}",
                    "",
                    "---",
                    "",
                ]
            )
    return "\n".join(lines)
