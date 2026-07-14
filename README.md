# Course 3 — Marketing Agent Team

Workshop code for Algen Academy's advanced course on multi-agent systems.

You build a small marketing team of agents: a Planner breaks a campaign brief into tasks, then a Copywriter, Editor, and SEO agent do the work. A human approves before anything goes out. Everything is traced with Traccia.

Full course page: https://algen.ai/multi-agent-systems-workshop

This repo also has the **1-hour demo** version of the same project. If you're running the live session, read `DEMO.md`.

---

## What you're building

One agent can write a blog post. That's fine for a toy demo.

In production, work usually splits across roles — someone plans, someone writes, someone edits, someone checks SEO, and a human signs off before publish. That's what this repo models.

By the end you have:

- A Planner that turns a brief into blog / social / SEO subtasks
- Specialist agents for each step
- Two ways to run them: one after another, or in parallel
- A human review step before publish
- Traces across every agent call (via Traccia)
- A Streamlit app that runs the whole thing from one screen

---

## Get it running

### 1. Set up the environment

```bash
cd workshop-multi
python3 -m venv .venv --without-pip
.venv/bin/python -c "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')"
.venv/bin/python get-pip.py && rm get-pip.py
source .venv/bin/activate
pip install -r requirements.txt
```

If `python3 -m venv .venv` works on your machine without the `--without-pip` workaround, use that instead.

### 2. Add your API key

```bash
cp .env.example .env
```

Open `.env` and paste your Gemini key from https://aistudio.google.com/apikey

### 3. Run it

Chapter by chapter (recommended for learning):

```bash
python chapters/01_overview.py      # no API key needed
python chapters/02_planner.py
python chapters/03_specialists.py
python chapters/04_hitl.py
python chapters/05_parallel.py
python chapters/06_observability.py
python chapters/07_integration.py
```

Full campaign from the command line:

```bash
python run_campaign.py
python run_campaign.py --mode sequential
python run_campaign.py --no-approval
```

Web UI:

```bash
streamlit run app.py
```

To deploy: push to GitHub, connect on [Streamlit Cloud](https://share.streamlit.io), pick `app.py`, and add `GEMINI_API_KEY` in secrets.

---

## What's in the repo

```
marketing_team/
  agents.py          Planner, Copywriter, Editor, SEO, and a Manager that calls them as tools
  orchestration.py   Sequential, parallel, and human review logic
  models.py          Structured outputs (Pydantic)
  config.py          Gemini + Traccia setup

chapters/            Seven scripts, one per course chapter
app.py               Streamlit UI
run_campaign.py      CLI entry point
DEMO.md              Speaking notes for the 1-hour live demo
```

---

## Tools used

- **Agents:** OpenAI Agents SDK
- **Model:** Gemini (free tier) through an OpenAI-compatible endpoint
- **Tracing:** Traccia — one `init()` call, auto-instruments the Agents SDK
- **UI:** Streamlit

If you've done Course 1 or 2, the setup will feel familiar. Course 3 is where you move from one agent to a team.

---

## Before you teach or demo

Read `DEMO.md`. It has the speaking flow, what to show on screen, and what to do when something breaks.

You should run through chapters 02–04 at least once before going live.

---

## Who this is for

Course 2 or similar experience: comfortable with the Agents SDK, tools, APIs, and basic Python async.

---

## A note on Traccia

Don't open with "here's our product." Let people hit the pain first — four agents, something fails, terminal logs aren't enough. Then introduce tracing the way you'd introduce any debugging tool: "this category of tool exists, today we're using Traccia because it's free and plugs into the SDK we're already using." The ideas transfer to Datadog, Jaeger, or whatever your team uses.
