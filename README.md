# Course 3: Marketing Agent Team

**Algen Academy · Advanced · 6-hour workshop** (this repo also powers the **1-hour demo trailer**)

Orchestrate a **Planner + Copywriter + Editor + SEO** marketing team with human review, parallel scaling, and end-to-end observability via [Traccia](https://traccia.ai).

Workshop page: https://algen.ai/multi-agent-systems-workshop

---

## What you build

A coordinated system that:

1. Turns a **campaign brief** into structured subtasks (Planner)
2. Delegates to **Copywriter → Editor → SEO** specialists
3. Runs work **sequentially or in parallel**
4. Pauses for **human approval** before publish
5. Traces every agent / LLM call with **Traccia**
6. Exposes the team behind a single **Streamlit** interface

---

## Quick start

```bash
python3 -m venv .venv --without-pip
.venv/bin/python -c "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')"
.venv/bin/python get-pip.py && rm get-pip.py
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # paste GEMINI_API_KEY from https://aistudio.google.com/apikey
```

If `python3 -m venv .venv` works on your machine, you can use that instead of `--without-pip`.

### Run chapters

```bash
python chapters/01_overview.py
python chapters/02_planner.py
python chapters/03_specialists.py
python chapters/04_hitl.py
python chapters/05_parallel.py
python chapters/06_observability.py
python chapters/07_integration.py
```

### Run full campaign (CLI)

```bash
python run_campaign.py
python run_campaign.py --mode sequential
python run_campaign.py --no-approval
```

### Streamlit UI

```bash
streamlit run app.py
```

Deploy: push to GitHub → [Streamlit Community Cloud](https://share.streamlit.io) → select `app.py`. Add `GEMINI_API_KEY` in secrets.

---

## Repo layout

```
marketing_team/          # reusable package
  agents.py              # Planner, Copywriter, Editor, SEO, Manager-as-tools
  orchestration.py       # sequential / parallel / HITL
  models.py              # structured outputs (Pydantic)
  config.py              # Gemini + Traccia setup
chapters/                # 7 progressive scripts (matches course outline)
app.py                   # Streamlit interface
run_campaign.py          # CLI entrypoint
DEMO.md                  # 1-hour demo speaking script (instructor)
```

---

## Stack

| Piece | Choice |
|-------|--------|
| Agents | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) |
| Model | Gemini (free) via OpenAI-compatible API |
| Observability | [Traccia](https://traccia.ai) (`traccia.init()`, auto Agents SDK) |
| UI | Streamlit |

Same foundation as Courses 1–2; Course 3 adds **multi-agent orchestration**.

---

## Instructor: 1-hour demo

See **[DEMO.md](./DEMO.md)** for the minute-by-minute script, talking points, and failure checklist.

Target for tomorrow: this code + first pass of that demo script rehearsed once.

---

## Prerequisites

Course 2 or equivalent: Agents SDK, tools, basic APIs, comfort with Python async.

---

## License / use

Workshop material for Algen Academy demos and cohorts. Do not present as a product pitch for Traccia — introduce observability as the natural fix after multi-agent complexity shows up (see DEMO.md language guidelines).
