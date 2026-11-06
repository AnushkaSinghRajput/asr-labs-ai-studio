# Channel strategy — ASR LABS + MANTHAN

Two independent education brands, one operating system.

| | **ASR LABS** | **MANTHAN** |
| --- | --- | --- |
| Purpose | AI, science, emerging tech, women innovators | Dharma, karma, आत्मबोध — contemplative life education |
| Language | English | Hindi-first |
| Visuals | Midnight ink + violet editorial / tech | Terracotta + Warli line art |
| Instagram | Live — `@asrlabs.co` | Live — MANTHAN (early) |
| YouTube | Create from scratch | Create from scratch |
| Cadence (target) | 2 shorts/day (08:00 & 20:00 IST) | 1 reflection/day (19:00 IST) until buffer exists |
| Config | `config/channels/asr-labs.yaml` | `config/channels/manthan.yaml` |

Brand reference screenshots: `docs/brand/`. Full ASR LABS ops doc: `docs/ASR_LABS_Professional_Operating_Blueprint_v2.pdf`.

## Shared operating rules

1. Human approval before any public post.
2. Exact asset + script + metadata version must be approved; edits reset approval.
3. Credentials only on the backend.
4. Official YouTube Data API + Instagram Graph API only.
5. Label AI-illustrative imagery when it could be mistaken for documentary fact.
6. Agents share one orchestrator and one content record per item — not five chat windows.

## Platform setup checklist (manual — founder)

### YouTube (both brands)

- [ ] Create/verify Google account for each brand (or Brand Account under one login)
- [ ] Create YouTube channel with correct name, handle, banner, avatar
- [ ] Upload channel trailer / about text aligned to config bio
- [ ] Enable YouTube Data API in Google Cloud; OAuth consent for upload/schedule
- [ ] Store OAuth refresh tokens in backend secrets (never frontend)
- [ ] First uploads as **private/unlisted** until the pipeline is trusted

### Instagram (both brands)

- [ ] Confirm Professional / Creator or Business account
- [ ] Link Meta Business / Facebook Page as required for Graph API
- [ ] Confirm exact `@` handles and save into channel YAML
- [ ] Complete Graph API app review / permissions for Reels publishing when ready
- [ ] Keep music rights-cleared (no random trending audio without rights for API-published video)

## First content buffers

**ASR LABS (Week 1 goal):** 1 end-to-end video through the OS → then a 7-video buffer before daily dual slots.

**MANTHAN (Week 1 goal):** 3–5 reflection Reels matching Warli look + Hindi voice, then steady 1/day.

Do not scale cadence until QA and approval feel calm.
