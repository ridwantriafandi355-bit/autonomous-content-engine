# 📖 Technical Documentation & Workflow Guide

Detailed guide for operating, configuring, and extending the **Autonomous Content Engine**.

---

## 🏗️ Architectural Overview

The engine operates as a sequential 4-stage pipeline designed for autonomous operation on Linux servers:

```
┌─────────────────────────┐
│  Stage 1: Intelligence  │ ➔ Daily Web Scraping, News Synthesis, Breakthrough Filtering
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│  Stage 2: Editorial     │ ➔ Hook generation, 4-6 slide breakdown, LinkedIn/IG copy
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│  Stage 3: Visual Engine │ ➔ Headless Pillow rendering: 1080x1350px 4:5 vertical slides
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│  Stage 4: Distribution  │ ➔ CDN asset upload & multi-channel Buffer MCP publishing
└─────────────────────────┘
```

---

## 🛠️ Step-by-Step Execution Guide

### 1. Intelligence Gathering (Stage 1)
Collects raw updates from tech sources, product launches, and model releases over the last 24 hours.

**Key Focus Areas:**
- Model releases & architectural benchmarks (LLMs, vision models, agent harnesses).
- Automation ecosystems (n8n, LangChain, crewAI, MCP developments).
- Developer productivity & open-source breakthroughs.

Outputs structured JSON containing:
```json
{
  "timestamp": "2026-09-23T09:00:00Z",
  "category": "AI Automation",
  "headline": "Example Headline",
  "summary": "Key technical takeaway...",
  "source_url": "https://..."
}
```

---

### 2. Editorial & Carousel Scripting (Stage 2)

Turn raw technical facts into an engaging narrative following high-conversion social frameworks:

1. **Slide 1 (The Hook):** State a counterintuitive fact or acute pain point.
2. **Slide 2 (The Breakdown):** Explain why conventional setups fail.
3. **Slide 3 (The Mechanism):** Step-by-step diagram or structural solution.
4. **Slide 4 (The Code / Implementation):** Exact tool stack, code snippet, or n8n workflow.
5. **Slide 5 (The Action / CTA):** Key summary takeaway and engagement invitation.

Refer to `references/prompts.md` for battle-tested prompt templates.

---

### 3. Visual Engine (Stage 3)

The renderer (`scripts/render_carousel.py`) compiles the JSON deck into crisp, platform-optimized slides:

- **Dimensions:** `1080 x 1350 px` (standard 4:5 portrait ratio).
- **Layout Math:**
  - Dynamic line wrapping based on bounding box measurement (`getbbox`).
  - Container heights adapt to text length to prevent overflow.
  - Accent indicators and badge pills render with anti-aliased corner radiuses.

```bash
python3 scripts/render_carousel.py \
  --input templates/carousel_example.json \
  --out-dir ./output_slides
```

---

### 4. Buffer MCP Distribution (Stage 4)

Buffer requires media files to be publicly reachable via HTTP/HTTPS URLs.

1. **Asset Staging:** Local `.png` images are uploaded to CDN storage.
2. **Payload Construction:** Post metadata and media links are mapped to channel profiles.
3. **Queue / Draft Scheduling:** Dispatched directly via Buffer MCP API.

```bash
python3 scripts/buffer_publisher.py \
  --channel linkedin \
  --text-file sample_caption.txt \
  --images output_slides/slide_1.png output_slides/slide_2.png \
  --mode draft
```

---

## ⚙️ Environment Variables

Configure these variables in your deployment environment or `.env` file:

| Variable | Description | Default |
|---|---|---|
| `BUFFER_API_KEY` | Buffer profile authentication token / MCP key | Required for Stage 4 |
| `BUFFER_MCP_URL` | Buffer MCP Server endpoint | `https://mcp.buffer.com/mcp` |
| `DEFAULT_BRAND_HANDLE` | Default footer watermark on slides | `@nusantaraai00001` |

---

## 🛡️ Reliability & Production Best Practices

- **Font Fallbacks:** The renderer automatically checks system font paths (`LiberationSans`, `DejaVuSans`, `Helvetica`).
- **Aspect Ratio:** Keep images in 4:5 ratio (`1080x1350`) for maximum visual screen real estate on mobile devices.
- **Fail-Safe Scheduling:** Always verify drafts in Buffer before enabling direct automatic publishing (`--mode draft` first).
