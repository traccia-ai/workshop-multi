# Course 3 — Marketing Agent Team

Workshop code for Algen Academy’s advanced course: **Designing Multi-Agent AI Systems**.

You build a small marketing team of agents. A Planner breaks a campaign brief into tasks. A Copywriter, Editor, and SEO agent do the work. A human approves before anything goes out. Every step can be traced.

Course page: https://algen.ai/multi-agent-systems-workshop

---

## What this repo is

This is the hands-on project for Course 3.

One agent can write a blog post. That’s fine for a quick demo. Real work usually splits across roles — plan, write, edit, optimize, approve. This repo models that pattern with agents.

By the end you have:

- A Planner that turns a brief into blog, social, and SEO subtasks
- Specialist agents for each step
- Sequential and parallel ways to run them
- A human review step before publish
- Tracing across agent calls (Traccia)
- A Streamlit app for the full pipeline on one screen

---

## Quick start

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

Open `.env` and paste your Groq key from https://console.groq.com/keys

### 3. Run it

**Chapter by chapter** (best for learning):

```bash
python chapters/01_overview.py      # no API key needed
python chapters/02_planner.py
python chapters/03_specialists.py
python chapters/04_hitl.py
python chapters/05_parallel.py
python chapters/06_observability.py
python chapters/07_integration.py
```

**Full campaign from the terminal:**

```bash
python run_campaign.py
python run_campaign.py --mode sequential
python run_campaign.py --no-approval
```

**Web UI:**

```bash
streamlit run app.py
```

To deploy: push to GitHub, connect on [Streamlit Cloud](https://share.streamlit.io), pick `app.py`, and add `GROQ_API_KEY` in secrets.

---

## What’s in the repo

```
marketing_team/
  agents.py           Planner, Copywriter, Editor, SEO, Manager
  orchestration.py    Sequential, parallel, human review
  models.py           Structured outputs (Pydantic)
  config.py           Groq + Traccia setup
  pipeline.py         Step-by-step flow for the UI

chapters/             One script per course chapter (01–07)
app.py                Streamlit UI
run_campaign.py       CLI entry point

SPEAKING_NOTES_1HR.md Two-host script for the 1-hour live session
demo/
  DEMO_PRESENTATION.pptx   Session slides
  presentation.html        Browser backup slides
  build_presentation.py    Rebuild the PPT
```

---

## 1-hour live session

If you’re teaching or demoing the short trailer session (not the full 6-hour course), use these:

| File | Use for |
|------|---------|
| `SPEAKING_NOTES_1HR.md` | What each host says, minute by minute |
| `demo/DEMO_PRESENTATION.pptx` | Slides (Presenter View) |
| `demo/presentation.html` | Backup if PPT doesn’t open |

Session shape:

1. **0–15 min** — Context and story  
2. **15–25 min** — Projects and experience  
3. **25–50 min** — Hands-on (Planner → Specialists → Human approval)  
4. **50–60 min** — Takeaways, prerequisites, Q&A  

For the live block, run at least:

```bash
python chapters/02_planner.py
python chapters/03_specialists.py
python chapters/04_hitl.py
```

Practice those three once before you go live.

---

## Tools used

| Piece | What we use |
|-------|-------------|
| Agents | OpenAI Agents SDK |
| Model | Groq (OpenAI-compatible endpoint) |
| Tracing | Traccia — `init()` auto-instruments the Agents SDK |
| UI | Streamlit |

If you’ve done Course 1 or 2, the setup will feel familiar. Course 3 is where you move from one agent to a team.

---

## Who this is for

Best if you already have Course 2–level comfort: Agents SDK basics, tools, APIs, and some Python.

You don’t need to be an ML researcher. You do need curiosity about how agents coordinate in a real workflow.

---

## A note on Traccia

Don’t open with “here’s our product.”

Let people feel the pain first — four agents running, something fails, terminal logs aren’t enough. Then introduce tracing the way you’d introduce any debugging tool: this category of tool exists; today we use Traccia because it’s free and plugs into the SDK you’re already using.

The ideas transfer to Datadog, Jaeger, or whatever your team uses later.
