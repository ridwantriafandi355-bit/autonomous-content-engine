# Copywriting & Editorial Prompts

Proven prompt templates for generating high-converting tech and AI content for LinkedIn & Instagram.

---

## 1. Research-to-Angle Converter

Use this prompt to convert raw news/research into 3 distinct content angles:

```markdown
Role: Senior AI Tech Strategist & Tech Creator
Task: Review this research data and generate 3 content angles:
1. The Architectural Breakdown (How it works under the hood)
2. The Economic / Workflow Impact (Why businesses and devs must care)
3. The Tactical Playbook (Step-by-step how to implement it today)

Research Data:
[PASTE RESEARCH SUMMARY]

Output requirements:
- For each angle: Catchy hook (1 line), Core thesis (2 lines), Target audience.
```

---

## 2. 5-Slide Carousel Script Generator

Use this prompt to create the exact JSON structure for `render_carousel.py`:

```markdown
Role: Visual Social Content Architect
Task: Generate a 5-slide technical carousel JSON for Instagram and LinkedIn.

Topic: [ENTER TOPIC]
Tone: Pragmatic, technical, high-signal, zero fluff.

Structure:
- Slide 1: Hook / Cover (Badge, Punchy Title ≤ 8 words, Subtitle)
- Slide 2: The Core Problem / Bottleneck (2 cards with title & description)
- Slide 3: The Architecture / Modern Approach (2 cards breaking down mechanism)
- Slide 4: Real-World Workflow / Code Insight (2 cards showing implementation steps)
- Slide 5: Takeaways & Next Steps (CTA card)

Format Output EXACTLY as valid JSON:
{
  "brand_handle": "@nusantaraai00001",
  "slides": [
    {
      "badge": "AI AGENTS 2026",
      "title": "Why Autonomous Agents Fail in Production",
      "subtitle": "And how multi-profile orchestration fixes the state drift problem.",
      "cards": []
    },
    ...
  ]
}
```

---

## 3. LinkedIn Post Copy Generator

```markdown
Role: AI Product Builder & Technical Storyteller
Task: Write a high-engagement LinkedIn post based on this carousel topic.

Formatting Rules:
1. First 2 lines MUST provoke curiosity or challenge conventional thinking.
2. Body: 3-5 concise bullet points using whitespace for readability.
3. Include real numbers, architecture patterns, or code node references.
4. Conclude with an open-ended technical question.
5. Add 3-5 high-signal hashtags (#AIAgents #Automation #n8n #ProductBuilder).
```
