# 🚀 Autonomous AI Content Pipeline

> End-to-end automated social media content engine: **Research ➔ Copywriting ➔ Headless Visual Carousel Rendering ➔ Buffer MCP Auto-Publishing**.

Built by **Ridwan Triafandi** ([@nusantaraai00001](https://www.instagram.com/nusantaraai00001) / [LinkedIn](https://www.linkedin.com/in/ridwan-triafandi-639a453b5)).

---

## ⚡ Overview

Producing high-signal technical content on LinkedIn and Instagram usually requires hours of manual work: scouring feeds for news, drafting scripts, designing graphics in Figma/Canva, and copying captions into schedulers.

This repository packages an **autonomous multi-agent pipeline** that executes the entire lifecycle on a headless Linux server:

1. **Stage 1 (Research):** Scrapes trending AI breakthroughs, benchmarks, and model updates in the past 24 hours.
2. **Stage 2 (Editorial):** Transforms raw technical data into high-engagement carousel scripts (4-6 slides) + platform-tailored captions.
3. **Stage 3 (Visual Engine):** Renders crisp 1080x1350 px (4:5 aspect ratio) carousel slides using pure Python Pillow without browser overhead.
4. **Stage 4 (Distribution):** Direct payload dispatch and scheduling to LinkedIn & Instagram via Buffer MCP / API.

---

## 📂 Project Structure

```
├── SKILL.md                         # Standard Hermes / AI Agent Skill specification
├── README.md                        # Documentation & setup guide
├── scripts/
│   ├── render_carousel.py           # Headless 1080x1350 Pillow slide renderer
│   └── buffer_publisher.py          # Buffer MCP / API multi-channel dispatcher
├── templates/
│   └── carousel_example.json        # Schema template for slide deck configuration
└── references/
    └── prompts.md                   # Editorial prompts for research, hooks, and copywriting
```

---

## 🛠️ Quickstart

### 1. Requirements
- Python 3.10+
- Pillow & Requests

```bash
pip install pillow requests
```

### 2. Render Carousel Slides
Create or modify `templates/carousel_example.json` and run:

```bash
python3 scripts/render_carousel.py \
  --input templates/carousel_example.json \
  --out-dir ./output_slides
```

Output: 4-6 high-definition `.png` slides ready for carousel upload.

### 3. Publish via Buffer
Set your Buffer channel ID and run:

```bash
python3 scripts/buffer_publisher.py \
  --channel linkedin \
  --text-file ./sample_caption.txt \
  --images ./output_slides/*.png \
  --mode draft
```

---

## 🤖 Using as an AI Agent Skill (Hermes)

This repository includes a native `SKILL.md`. To import it into your Hermes Agent instance:

```bash
# Clone to your Hermes skills directory:
git clone https://github.com/Dandidcee/autonomous-content-pipeline.git ~/.hermes/skills/autonomous-content-pipeline
```

The agent will automatically recognize the skill and autonomously execute content batches on demand.

---

## 📄 License
MIT License. Free to use, adapt, and build upon.
