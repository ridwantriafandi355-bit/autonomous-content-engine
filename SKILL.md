---
name: autonomous-content-pipeline
description: "Use when creating autonomous content: research, drafting, visual carousel rendering, and publishing via Buffer MCP."
category: "social-media"
---

# Autonomous Content Pipeline (Research to Publish)

End-to-end multi-stage pipeline for automated social content production:
1. **Intelligence Gathering**: Automated search & web extraction of trending AI / tech news.
2. **Editorial Drafting**: Hook crafting, carousel slide scripting (4-6 slides), long-form LinkedIn copy, and Instagram captions.
3. **Visual Engine**: Headless image rendering (1080x1350 vertical or 1080x1080 square) using Python Pillow with auto-wrapping, badges, and brand aesthetics.
4. **Distribution Engine**: Direct media upload and scheduling via Buffer MCP (LinkedIn, Instagram).

---

## Architecture Flow

```
[Web Search / News API]
         │
         ▼
[Stage 1: Research Aggregator] ──> Saves structured summary (JSON / Markdown)
         │
         ▼
[Stage 2: Copywriting Engine]  ──> Generates slide deck copy + captions + hashtags
         │
         ▼
[Stage 3: Visual Renderer]     ──> Python Pillow renders PNG/JPG slides
         │
         ▼
[Stage 4: Buffer MCP Dispatch] ──> Schedules posts to LinkedIn & Instagram
```

---

## 1. Stage 1: Intelligence Gathering & Research

Aggregates breakthroughs, model releases, funding, and benchmarks.

### Execution
Run search queries for 24h tech developments:
```bash
python3 scripts/research.py --topic "AI agents workflow n8n automation" --output research_latest.json
```

### Prompt Specification
- Filter out marketing hype; focus on benchmarks, architecture, practical productivity gains, or developer tooling.
- Extract: Headline, Core Mechanism, Impact/Numbers, Source Link.

---

## 2. Stage 2: Editorial & Copywriting

Converts raw research into an engaging narrative tailored for LinkedIn & Instagram.

### Carousel Slide Framework (4-5 Slides)
- **Slide 1 (Hook / Cover):** High-contrast title (≤ 8 words), bold problem statement, brand badge.
- **Slide 2 (The Shift / Problem):** Why traditional methods fail or what just changed.
- **Slide 3 (The Core Solution):** Architecture breakdown or step-by-step framework.
- **Slide 4 (Real Implementation):** Practical code node, tool stack, or workflow metric.
- **Slide 5 (Actionable CTA):** Next steps, profile handle, save/repost prompt.

### LinkedIn Post Rules
- Hook on lines 1-2 (before "see more" cutoff).
- Bullet points with whitespace separation for readability.
- Clear takeaway for professionals / business builders.
- No hashtag stuffing (3-5 relevant tags max: `#AIAgents #Automation #Productivity`).

---

## 3. Stage 3: Visual Generation Engine

Generates crisp, high-resolution carousel slides headless without a browser.

### Specifications
- **Dimensions:** 1080 x 1350 px (4:5 portrait ratio — maximizes mobile viewport).
- **Format:** High-quality JPG / PNG (< 2 MB for fast Buffer upload).
- **Typography:** LiberationSans-Bold (Headers), LiberationSans-Regular (Body), monospace for code.
- **Color Palette:**
  - Dark Theme: Background `#0A0F1D`, Surface Card `#161F36`, Accent `#4AB3D8`, Text Primary `#FFFFFF`, Text Dim `#94A3B8`.
  - Light Theme: Background `#F8FAFC`, Surface Card `#FFFFFF`, Accent `#0284C7`, Text Primary `#0F172A`, Text Dim `#64748B`.

### Script Usage
```bash
python3 scripts/render_carousel.py --input content_plan.json --out-dir ./output_slides
```

---

## 4. Stage 4: Buffer MCP Auto-Publishing

Publishes or queues drafts directly across connected social channels.

### Channel IDs
- **LinkedIn Profile:** Channel ID `6aaf2200ea19ca0bde8fb4e6`
- **Instagram Profile:** Channel ID `6aae3f6fea19ca0bde8554da`

### Media Hosting Requirement
Buffer requires publicly accessible media URLs for image attachments:
1. Upload generated slides to a temporary/permanent CDN or file host (e.g. S3, Cloudinary, or `https://uguu.se/upload.php`).
2. Pass the media URL array in the Buffer MCP payload.

### Buffer MCP Tool Execution
```json
{
  "channel_id": "6aaf2200ea19ca0bde8fb4e6",
  "text": "Caption text here...\n\n#AIAgents #Automation",
  "media": [
    "https://cdn.example.com/slide_1.jpg",
    "https://cdn.example.com/slide_2.jpg"
  ],
  "scheduling_type": "draft"
}
```

---

## Best Practices & Pitfalls

1. **Text Overflow:** Never hardcode text bounding boxes without word wrapping (`get_text_lines()`). Calculate text height dynamically before rendering boxes.
2. **Buffer Carousel Limits:** LinkedIn documents accept PDF format for multipage swipe carousels. For Instagram, carousel posts support up to 10 images.
3. **Rate Limits:** Space scheduled posts at least 4 hours apart to maximize reach and avoid platform spam filters.
