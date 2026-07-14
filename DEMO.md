# Course 3 — 1-Hour Demo Script (v1)

**Product shown:** Marketing Agent Team (Planner + Copywriter + Editor + SEO)  
**Audience:** 4–5 people (internal / early demo)  
**Hosts:** Neha (content + code) · Co-host optional  
**Goal of this hour:** Show the *end product* people get from Course 3, then walk them through how the team of agents actually works — enough that they want the full 6-hour workshop.

> Trailer promise (first 1–2 minutes):  
> “This is what you will leave with — a coordinated marketing agent team that plans, drafts, edits, optimizes, waits for human approval, and is fully traced.”

Reference: https://algen.ai/multi-agent-systems-workshop

---

## Setup (before the call — 15 min)

1. Clone this repo, create venv, `pip install -r requirements.txt`
2. Copy `.env.example` → `.env`, paste Gemini key from https://aistudio.google.com/apikey
3. Smoke-test:
   - `python chapters/01_overview.py`
   - `python chapters/02_planner.py` (needs key)
   - `streamlit run app.py`
4. Keep one terminal for CLI chapters, one browser tab for Streamlit, one for Traccia console output
5. Optional: deploy Streamlit Cloud once so you have a public URL to share

Practice once out loud (mirror / recording). Speaking for ~50 minutes with live runs is enough; you do not need a perfect monologue.

---

## Minute-by-minute flow

### 0–2 min — Trailer (end product first)

**You say:**  
Welcome. In this hour you will see — and then run — a **marketing team of agents**. Not one chatbot. A Planner that breaks a campaign brief into work, specialists that draft / edit / SEO, a human approval gate, and traces across every agent.

**You show:** Streamlit app with a finished package (or a pre-saved `outputs/campaign_package.json`). Scroll Drafts → Edited → SEO → Review.

**Depth trigger:** “Same OpenAI Agents SDK used in production agent deployments. Course 3 is about orchestration, not prompts.”

---

### 2–8 min — Why multi-agent? (whiteboard / slide)

**You say:**  
One agent can only do so much. Marketing is a natural team: plan, write, edit, optimize. Same patterns as planner / researcher / executor / reviewer in any domain.

Draw or open `chapters/01_overview.py` output:

- Sequential vs parallel vs delegation
- Human-in-the-loop before publish
- Observability across agents

Run: `python chapters/01_overview.py`

---

### 8–18 min — Planner agent (structured plan)

**You say:**  
First agent: Planner. Brief in → structured plan out (Pydantic / `output_type`).

Run: `python chapters/02_planner.py`  
Show JSON: campaign name, audience, 3 subtasks (blog / social / seo).

**Depth trigger:** Show `CampaignPlan` in `marketing_team/models.py`. “In production these schemas are versioned and tested.”

---

### 18–28 min — Specialists + delegation

**You say:**  
Copywriter, Editor, SEO — each with a narrow job. Manager can call them as **tools** (`Agent.as_tool`). That is the delegation pattern.

Run: `python chapters/03_specialists.py`  
Point at tool calls in the console.

**Depth trigger:** Contrast agents-as-tools (manager stays in control) vs handoffs (specialist takes over).

---

### 28–38 min — Human-in-the-loop

**You say:**  
Agents draft. Humans publish. We pause for approval — same idea as production spend / delete / send gates.

Run: `python chapters/04_hitl.py`  
Approve or reject live. Show what “published” means in the package.

Or do the same buttons in Streamlit (cleaner for a small audience).

---

### 38–48 min — Parallel vs sequential + cost/latency

**You say:**  
Same work, two strategies. Sequential is simple. Parallel is faster wall-clock — and noisier on cost and traces.

Run: `python chapters/05_parallel.py`  
Compare totals. Ask: “When would you *not* parallelize?”

**Depth trigger:** Peak concurrency, rate limits, attribution of tokens per agent.

---

### 48–55 min — Observability (Traccia, naturally)

**Narrative (do not pitch):**  
With 4 agents, `print` does not scale. Same category of tools as Datadog/Jaeger — we use Traccia because it is free and auto-instruments the Agents SDK.

Run: `python chapters/06_observability.py`  
Show spans: which agent, latency, tokens.

Language: “Concepts apply to any tracer. Today we use Traccia.”

---

### 55–60 min — Deploy + wrap + Course 3 CTA

1. Show Streamlit URL (local or Cloud): `streamlit run app.py`
2. Full path: `python chapters/07_integration.py` or `python run_campaign.py`
3. Close:

> Today’s demo → full Course 3 (6 hours): architecture patterns, orchestration, HITL, performance, observability, final integration.  
> Link: https://algen.ai/multi-agent-systems-workshop

Ask for questions. Offer to share repo + brief they can re-run tonight.

---

## Talking points cheat sheet

| Moment | One line |
|--------|----------|
| Trailer | “You leave with a coordinated marketing agent team.” |
| Planner | “Brief → structured subtasks.” |
| Specialists | “Narrow jobs beat one mega-prompt.” |
| HITL | “Agents draft; humans publish.” |
| Parallel | “Speed vs cost vs trace clarity.” |
| Traccia | “Free, auto-instruments Agents SDK; concepts are universal.” |
| CTA | “This hour is the trailer; Course 3 is the film.” |

---

## If something breaks

| Symptom | Fix |
|---------|-----|
| Missing API key | Check `.env` / `GEMINI_API_KEY` |
| Gemini 400 / metadata | Confirm `OpenAIChatCompletionsModel` + tracing disabled for OpenAI backend (already in `config.py`) |
| Streamlit asyncio issues | Restart app; use chapter CLIs as backup |
| Slow parallel run | Use shorter brief; switch to sequential for the live path |
| No traces | `pip install traccia` + `init_observability()` |

---

## After the demo (your homework tonight)

- [ ] Record yourself once (even 20 min) covering trailer → planner → specialists → HITL
- [ ] Deploy Streamlit once (Cloud or Render) and save the URL
- [ ] Push this repo; keep `outputs/` out of git if it has demo content you do not want public
- [ ] Expand later into full 6-hour chapter timing (outline already matches algen.ai Course 3)

---

## Mapping to full 6-hour Course 3

| Chapter | Full course | This 1-hour demo |
|---------|-------------|------------------|
| 01 Overview | 30 min | 2–8 min |
| 02 Planner | 45 min | 8–18 min |
| 03 Specialists | 45 min | 18–28 min |
| 04 HITL | 30 min | 28–38 min |
| 05 Scaling | 45 min | 38–48 min |
| 06 Observability | 45 min | 48–55 min |
| 07 Integration | 30 min | 55–60 min |
