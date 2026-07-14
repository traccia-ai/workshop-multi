# 1-Hour Demo — Speaking Notes

This is the short version of Course 3. You're showing people what they'll actually build, then walking them through how it works.

**You:** Neha (content + code)  
**Audience:** Small group, 4–5 people  
**Length:** ~60 minutes  
**Course page:** https://algen.ai/multi-agent-systems-workshop

---

## Before you go live (15 min prep)

1. Clone the repo, install deps, add your Gemini key to `.env`
2. Run these once to make sure nothing surprises you:
   - `python chapters/01_overview.py`
   - `python chapters/02_planner.py`
   - `streamlit run app.py`
3. Keep three things open: a terminal for chapter scripts, the Streamlit tab, and console output from Traccia
4. Optional but useful: deploy Streamlit once so you have a URL to share

You don't need a polished script. Run through it once out loud — mirror, recording, whatever works. Fifty minutes of live demo is enough.

---

## How to open (first 2 minutes)

Start with the finished thing, not the code.

Open the Streamlit app (or a saved campaign package) and scroll through Drafts → Edited → SEO → Review. Let them see the output first.

Something like:

> "In the next hour you'll see a marketing team of agents — not one chatbot. A planner breaks a brief into tasks, specialists draft and edit the content, SEO optimizes it, and nothing publishes until a human says yes. Every step is traced. This is what Course 3 builds."

That two-minute preview is your trailer. It answers "what will I learn?" before you explain anything.

---

## The flow

### Part 1 — Why a team, not one agent (2–8 min)

One agent doing everything sounds simple until you try it. Planning, writing, editing, and SEO are different jobs. Splitting them into specialists is the same pattern you'd use for research, execution, or review in any other domain.

Run `python chapters/01_overview.py` and walk through the diagram: brief → planner → specialists → human review → publish.

Mention the three orchestration ideas you'll use today:
- **Sequential** — one step at a time, easy to follow
- **Parallel** — independent tasks at once, faster but messier on cost
- **Delegation** — a manager agent calls specialists as tools

If a senior engineer is in the room, note that these are the same patterns used in production multi-agent systems — planner/worker, handoffs, human gates.

---

### Part 2 — The Planner (8–18 min)

The first real agent. You give it a campaign brief, it returns a structured plan: campaign name, audience, goal, and three subtasks (blog, social, SEO).

Run `python chapters/02_planner.py`

Show the JSON output. Point out that it's not free text — it's a typed schema (`CampaignPlan` in `models.py`). In a real project you'd version and test that schema.

Sample brief if you need one:

> Launch a campaign for Algen Academy Course 3. Audience: senior engineers. Goal: waitlist signups. Tone: practical, not salesy.

---

### Part 3 — Specialists and delegation (18–28 min)

Now the Copywriter, Editor, and SEO agents. Each has one job and a narrow prompt.

Run `python chapters/03_specialists.py`

This uses the "agents as tools" pattern — a manager agent calls specialists without handing over the whole conversation. Show the tool calls in the console.

Worth a quick contrast: **agents as tools** (manager stays in control) vs **handoffs** (specialist takes over). Both are valid. This workshop uses tools because the manager needs to combine outputs.

---

### Part 4 — Human in the loop (28–38 min)

Agents draft. Humans publish. That's the rule.

Run `python chapters/04_hitl.py` and approve or reject something live. Or use the Approve / Request changes buttons in Streamlit — cleaner for a small audience.

The point isn't the button. It's the idea: in production, you gate irreversible actions — sending email, charging a card, publishing content. Same pattern here.

---

### Part 5 — Sequential vs parallel (38–48 min)

Same campaign, two ways to run it.

Run `python chapters/05_parallel.py` and compare the timing output.

Sequential is slower but easier to debug. Parallel is faster wall-clock but hits more API calls at once. Ask the room: when would you *not* parallelize? (Rate limits, dependent tasks, tight budget.)

---

### Part 6 — Observability (48–55 min)

Don't lead with the tool. Lead with the problem.

> "You've got four agents. Something fails. Print statements won't scale. You need to see which agent, which call, how many tokens."

Then:

> "There's a whole category of tools for this — tracing, same idea as Datadog or Jaeger for distributed systems. Today we're using Traccia because it's free and auto-instruments the Agents SDK. The concepts work with any tracer."

Run `python chapters/06_observability.py`. Show spans in the console: agent name, latency, tokens.

Don't say "Traccia is the best." Say "this is what we use today."

---

### Part 7 — Wrap up (55–60 min)

1. Open the Streamlit app one more time: `streamlit run app.py`
2. Or run the full pipeline: `python chapters/07_integration.py`
3. Close with the learning path:

> "This hour was the trailer. The full Course 3 is six hours — architecture patterns, orchestration, human review, performance, observability, and a deployed team you can show to your team. Details at algen.ai/multi-agent-systems-workshop."

Ask for questions. Share the repo link.

---

## Quick reminders (glance at these if you blank)

| When | Say something like |
|------|-------------------|
| Opening | "You'll leave with a marketing agent team, not one chatbot." |
| Planner | "Brief in, structured plan out." |
| Specialists | "Narrow jobs, not one giant prompt." |
| HITL | "Agents draft. Humans publish." |
| Parallel | "Faster, but watch cost and trace noise." |
| Traccia | "Same tracing ideas as any production system." |
| Closing | "This hour is the trailer. Course 3 is the full build." |

---

## When things go wrong

**Missing API key** — check `.env`, key should not say `your_gemini_api_key_here`

**Gemini returns 400** — already handled in `config.py` (Chat Completions model, OpenAI tracing disabled). Restart and retry.

**Streamlit hangs** — restart it; fall back to chapter CLI scripts

**Parallel run is slow** — shorten the brief, or demo sequential instead

**No traces showing** — confirm `traccia` is installed and `init_observability()` runs at the top of the script

---

## After the session

- Record yourself once, even 20 minutes — trailer through HITL is enough
- Deploy Streamlit and save the URL
- Rehearse the approve/reject moment; it's the most memorable part
- The full 6-hour timing is in the table below when you're ready to expand

---

## How this maps to the full course

| Chapter | Full workshop | This demo |
|---------|--------------|-----------|
| 01 — Overview | 30 min | ~6 min |
| 02 — Planner | 45 min | ~10 min |
| 03 — Specialists | 45 min | ~10 min |
| 04 — Human review | 30 min | ~10 min |
| 05 — Scaling | 45 min | ~10 min |
| 06 — Observability | 45 min | ~7 min |
| 07 — Integration | 30 min | ~5 min |
