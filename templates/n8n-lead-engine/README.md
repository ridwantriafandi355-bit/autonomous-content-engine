# Autonomous AI Lead Ingestion & CRM Enrichment Engine (n8n + Claude 3.5 + Perplexity)

![n8n](https://img.shields.io/badge/n8n-Workflow%20Automation-FF6D5A?style=flat&logo=n8n)
![Claude 3.5 Sonnet](https://img.shields.io/badge/Anthropic-Claude%203.5%20Sonnet-D97706?style=flat&logo=anthropic)
![HubSpot](https://img.shields.io/badge/CRM-HubSpot%20Sync-FF7A59?style=flat&logo=hubspot)
![Perplexity AI](https://img.shields.io/badge/Search-Perplexity%20Sonar-20B2AA?style=flat)
![Slack](https://img.shields.io/badge/Alerts-Slack%20Dispatch-4A154B?style=flat&logo=slack)

An enterprise-ready, production n8n automation pipeline that captures inbound B2B sales leads, filters corporate domains, enriches business intelligence in real time via search APIs, scores Ideal Customer Profile (ICP) fit using **Claude 3.5 Sonnet**, and synchronizes enriched attributes to CRM (HubSpot) and team dispatch channels (Slack).

---

## 🏗️ Architecture Overview

```
[Inbound Webhook] (Typeform, Webflow, Landing Page)
        │
        ▼
[Payload Validation & Normalization] (Strict Schema Cleanse)
        │
   ┌────┴──────────────────────────┐
[Corporate B2B Domain?]      [Personal Domain: gmail/yahoo]
   │ (YES)                          │ (NO)
   ▼                                │
[Perplexity Sonner API]             │
(Fetch Headcount, Industry, Ops)   │
   │                                │
   └───────────────┬────────────────┘
                   │
                   ▼
  [Claude 3.5 Sonnet AI Agent]
  + Strict JSON Schema Output Parser
  (ICP Fit 1-100, Tier 1/2/3, Personalized SDR Icebreaker)
                   │
                   ▼
  [HubSpot CRM Upsert Contact]
  (Write custom properties: icp_score, tier, icebreaker)
                   │
   ┌───────────────┴───────────────┐
[Score >= 75? (Tier 1)]     [Score < 75 (Tier 2/3)]
   │                                │
   ▼                                ▼
[Slack #leads-hot]          [Slack #leads-general]
(Instant Rep Notification)  (Standard Async Audit Log)
```

---

## ⚡ Key Capabilities

1. **Zero-Drop Inbound Ingestion**: Accepts webhook payloads from any form builder (Typeform, Webflow, Tally, or direct API).
2. **Defensive Schema Sanitization**: JavaScript normalization node strips leading spaces, formats emails to lowercase, and extracts clean domain entities.
3. **Smart Enrichment Branching**: Bypasses costly intelligence APIs if the lead registers with disposable/free domains (`gmail.com`, `yahoo.com`), saving API credits.
4. **Structured Reasoning (No Hallucinations)**: Uses LangChain structured output parser to guarantee valid JSON adhering to predefined scoring ranges.
5. **Actionable Sales Enablement**: Writes ready-to-send 1-sentence personalized SDR icebreakers directly into CRM contact fields.
6. **Tier-Based Routing**: Tier 1 deals alert account executives instantly in a priority Slack channel, while lower tiers proceed to automated nurture cadences.

---

## 🧩 Pipeline Nodes & Logic Breakdown

| Node Name | Node Type | Purpose & Logic |
| :--- | :--- | :--- |
| **Webhook: Inbound Lead Intake** | `n8n-nodes-base.webhook` | Entrypoint listener receiving `POST` JSON payloads. |
| **Code: Validate & Normalize** | `n8n-nodes-base.code` | Validates presence of `email` & `name`. Parses domain and flags B2B status. |
| **IF: Corporate Domain?** | `n8n-nodes-base.if` | Routes corporate domains to enrichment, free emails to direct evaluation. |
| **HTTP: Perplexity Company Intelligence** | `n8n-nodes-base.httpRequest` | Queries `sonar-pro` for company overview, revenue model, and team size. |
| **Anthropic Chat Model** | `@n8n/langchain.lmChatAnthropic` | Backs the evaluation agent with Claude 3.5 Sonnet (`temperature: 0.2`). |
| **Structured Output Parser** | `@n8n/langchain.outputParserStructured`| Enforces JSON schema: `icp_score`, `tier`, `reasoning`, `custom_icebreaker`. |
| **AI Agent: Lead Scorer** | `@n8n/langchain.chainLlm` | Core reasoning engine assessing prospect fit and drafting the outreach hook. |
| **HubSpot: Upsert Contact** | `n8n-nodes-base.hubspot` | Deduplicates by email; upserts contact and writes custom enrichment properties. |
| **IF: High Priority Tier 1?** | `n8n-nodes-base.if` | Checks condition: `icp_score >= 75`. |
| **Slack: Immediate Hot Lead** | `n8n-nodes-base.slack` | Dispatches rich markdown alert with executive summary and icebreaker to `#leads-hot`. |
| **Slack: Standard Inbound Log** | `n8n-nodes-base.slack` | Sends quiet audit log to `#leads-general`. |

---

## 🔑 Required Credentials

To run this pipeline in your n8n instance, configure the following credentials:

### 1. Anthropic API
- **Type**: `Anthropic API`
- **Required In**: `Anthropic Chat Model`
- **Scope**: Access to `claude-3-5-sonnet-20241022`

### 2. Perplexity API (Generic HTTP Header Auth)
- **Type**: `Header Auth`
- **Required In**: `HTTP: Perplexity Company Intelligence`
- **Header Key**: `Authorization`
- **Header Value**: `Bearer pplx-xxxxxxxxxxxxxxxxxxxx`

### 3. HubSpot App Token
- **Type**: `HubSpot App Token` (Private App)
- **Required In**: `HubSpot: Upsert Contact & Properties`
- **Scopes Required**: `crm.objects.contacts.read`, `crm.objects.contacts.write`
- *Note*: Ensure custom properties (`icp_score`, `lead_tier`, `sdr_icebreaker`, `ai_qualification_notes`) are created under HubSpot Contact Properties, or map them to standard note fields.

### 4. Slack Bot Token
- **Type**: `Slack API` (OAuth Bot Token `xoxb-...`)
- **Required In**: `Slack Dispatch Nodes`
- **Scopes Required**: `chat:write`, `chat:write.public`

---

## 🚀 Quick Setup & Import

1. **Clone this repository**:
   ```bash
   git clone https://github.com/ridwantriafandi355-bit/n8n-ai-lead-engine.git
   cd n8n-ai-lead-engine
   ```
2. **Import to n8n**:
   - Open your n8n dashboard.
   - Click **Workflows** → **Import from File**.
   - Select `workflow_lead_enrichment.json`.
3. **Attach Credentials**:
   - Assign your Anthropic, Perplexity, HubSpot, and Slack credentials to the respective nodes.
4. **Activate & Test**:
   - Click **Execute Workflow** (or switch to **Active**).
   - Send a sample test payload to the webhook URL:
   ```bash
   curl -X POST https://your-n8n-instance.com/webhook/lead-intake \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Sarah Jenkins",
       "email": "sarah@stripe.com",
       "company": "Stripe",
       "notes": "Looking to automate our international merchant verification triage."
     }'
   ```

---

## 🛡️ Production Considerations
- **Rate-Limiting Resilience**: All external HTTP/LLM calls include `continueOnFail` configurations to prevent pipeline stalls.
- **Data Privacy**: No lead PII is stored locally; data flows directly into your private CRM instance.

---

## 👨‍💻 Author
**Ridwan Triafandi**  
*AI Product Builder & Workflow Automation Specialist*  
- **GitHub**: [@ridwantriafandi355-bit](https://github.com/ridwantriafandi355-bit)  
- **LinkedIn**: [Ridwan Triafandi](https://www.linkedin.com/in/ridwan-triafandi-639a453b5)  
- **Email**: ridwantriafandi1@gmail.com
