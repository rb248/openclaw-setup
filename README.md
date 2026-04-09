# OpenClaw Setup Repository

This repository is a **sanitized, shareable template** for running OpenClaw with:

- multiple agents
- Telegram bot routing
- agent-specific workspaces
- safe public docs/templates (without live secrets)

It is designed so you can keep private runtime state in `~/.openclaw/` while keeping this repo safe for GitHub.

---

## Quick start (10-minute version)

1. Install OpenClaw and run onboarding.
2. Copy `openclaw.sample.json` into your private config location as `openclaw.json`.
3. Copy `.env.example` to `.env` (local only), then fill your tokens.
4. Create Telegram bots in BotFather (one per agent).
5. Configure `channels.telegram.accounts` + `bindings` in `openclaw.json`.
6. Ensure each agent in `agents.list` points to valid `agentDir` and `workspace`.
7. Start OpenClaw gateway, then test each bot in Telegram.

If you want full detail, continue below.

---

## Repository structure

```text
.
├── openclaw.sample.json          # safe template for config
├── .env.example                  # placeholder secret names
├── agents/
│   ├── README.md
│   ├── cv-writer/
│   ├── job-search/
│   ├── linkedin-content/
│   └── interview-prep/
└── workspace/
		├── README.md
		├── BOOTSTRAP.md
		└── memory/README.md
```

For each agent folder, the intended layout is:

- `agents/<agent>/agent/` → prompt/identity/tooling docs
- `agents/<agent>/workspace/` → workspace markdown and memory templates

---

## Prerequisites

- Linux/macOS shell environment
- OpenClaw installed locally
- Telegram account + BotFather access
- API access for your selected model providers (if applicable)

---

## Step 1: Install OpenClaw locally

Use your preferred installation method. Typical flow:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw gateway status
openclaw dashboard
```

Optional terminal UI:

```bash
openclaw tui
```

---

## Step 2: Create your private config from template

Copy and customize `openclaw.sample.json` as your runtime config (`openclaw.json`) on your machine.

### Important

- Keep real config and secrets in your private OpenClaw location (typically `~/.openclaw/`).
- Do **not** commit live tokens.

This template already includes:

- `agents.defaults`
- `agents.list`
- `bindings` (channel/account → agent routing)
- `channels.telegram.accounts`
- `gateway` options
- safe node command denylist

---

## Step 3: Configure environment secrets

Copy `.env.example` to local `.env` and fill your values.

Expected keys:

- `TELEGRAM_BOT_TOKEN`
- `OPENCLAW_GATEWAY_TOKEN`
- `OLLAMA_API_KEY`

You can define additional keys for multiple bots (recommended), e.g.:

- `TELEGRAM_BOT_TOKEN_CVWRITER`
- `TELEGRAM_BOT_TOKEN_JOBFINDER`
- `TELEGRAM_BOT_TOKEN_LINKEDIN`
- `TELEGRAM_BOT_TOKEN_INTERVIEW_PREP`

Then reference them in your config with `${ENV_VAR_NAME}` placeholders.

---

## Step 4: Telegram multi-bot setup

### 4.1 Create bots in BotFather

For each agent, create one bot and keep token/account names aligned:

| Agent ID | Telegram accountId (suggested) | Purpose |
|---|---|---|
| `cv-writer` | `cvwriter` | CV and cover letter help |
| `job-search` | `jobfinder` | Job discovery and tracking |
| `linkedin-content` | `linkedin` | Content generation |
| `interview-prep` | `interview-prep` | Interview prep workflows |

Typical BotFather flow:

1. `/newbot`
2. Set display name
3. Set unique username (must end with `bot`)
4. Save token securely

Optional hardening:

- `/setprivacy` (depending on group behavior you want)
- `/setdescription`
- `/setabouttext`
- `/setuserpic`

### 4.2 Add accounts in `channels.telegram.accounts`

Add one entry per bot token in `openclaw.json`:

```json
"channels": {
	"telegram": {
		"enabled": true,
		"accounts": {
			"cvwriter": { "botToken": "${TELEGRAM_BOT_TOKEN_CVWRITER}", "enabled": true },
			"jobfinder": { "botToken": "${TELEGRAM_BOT_TOKEN_JOBFINDER}", "enabled": true },
			"linkedin": { "botToken": "${TELEGRAM_BOT_TOKEN_LINKEDIN}", "enabled": true },
			"interview-prep": { "botToken": "${TELEGRAM_BOT_TOKEN_INTERVIEW_PREP}", "enabled": true }
		}
	}
}
```

### 4.3 Add routing in `bindings`

Each `accountId` should route to exactly one `agentId`:

```json
"bindings": [
	{ "type": "route", "agentId": "job-search", "match": { "channel": "telegram", "accountId": "jobfinder" } },
	{ "type": "route", "agentId": "cv-writer", "match": { "channel": "telegram", "accountId": "cvwriter" } },
	{ "type": "route", "agentId": "linkedin-content", "match": { "channel": "telegram", "accountId": "linkedin" } },
	{ "type": "route", "agentId": "interview-prep", "match": { "channel": "telegram", "accountId": "interview-prep" } }
]
```

---

## Step 5: Agent setup

Define agents under `agents.list` with:

- unique `id`
- human-readable `name`
- `agentDir` path
- `workspace` path
- optional `tools.profile`

Example pattern:

```json
{
	"id": "job-search",
	"name": "job-search",
	"agentDir": "/home/you/.openclaw/agents/job-search/agent",
	"workspace": "/home/you/.openclaw/agents/job-search",
	"tools": { "profile": "full" }
}
```

### Agent content checklist

For each agent, ensure these exist:

- `agent/SOUL.md`
- `agent/IDENTITY.md`
- `agent/AGENTS.md`
- workspace docs (`SOUL.md`, `IDENTITY.md`, `TOOLS.md`, etc.)
- optional memory folder (`workspace/memory/`)

Use this repository’s `agents/*` templates as the source of truth for sanitized structure.

---

## Step 6: Model/provider setup

In your config, set:

- default model (`agents.defaults.model.primary`)
- fallback models (`agents.defaults.model.fallbacks`)
- provider configuration under `models.providers`

For Ollama-compatible provider config, ensure:

- local/base URL is reachable
- required API key env variables are available
- selected model IDs exist in provider

---

## Step 7: Gateway and runtime settings

Recommended safe defaults already shown in sample:

- `gateway.bind = "loopback"`
- token auth enabled
- command denylist in `gateway.nodes.denyCommands`

For local development only:

- `controlUi.allowInsecureAuth` should generally remain `false` unless you understand the risk.

---

## Step 8: Start and verify

1. Start OpenClaw/gateway.
2. Confirm gateway health/status.
3. Send a test message to each Telegram bot.
4. Verify each bot lands in the expected agent workflow.

Suggested smoke tests:

- CV bot: “draft a short CV summary for backend ML role”
- Job bot: “find 5 roles in Berlin for MLOps engineer”
- LinkedIn bot: “write a post on model monitoring lessons”
- Interview bot: “ask me 3 system design interview questions”

---

## Security checklist (must-do)

- [ ] Never commit real `openclaw.json` containing live tokens
- [ ] Keep `.env` local-only
- [ ] Rotate any token that was ever exposed in chat/history/screenshots
- [ ] Keep `~/.openclaw/credentials`, sessions, media, and logs out of git
- [ ] Keep gateway bound to loopback unless intentionally exposing securely

> If you previously exposed real bot tokens or gateway tokens, rotate them immediately in BotFather/provider dashboards.

---

## Troubleshooting

### Bot does not respond

- Check bot token validity in BotFather
- Verify `channels.telegram.enabled = true`
- Confirm account key in `accounts` exactly matches `bindings.match.accountId`
- Confirm target `agentId` exists in `agents.list`

### Messages route to wrong agent

- Check duplicate/overlapping `bindings`
- Ensure account IDs are unique per bot

### Agent starts but lacks context

- Validate `agentDir` and `workspace` paths
- Ensure required markdown files exist under agent/workspace folders

### Model/provider errors

- Verify provider base URL
- Verify API key/env mapping
- Verify model IDs are supported by provider

---

## What is safe to commit vs never commit

### Safe to commit

- Templates (`*.md`, sample JSON)
- Generic agent/workspace prompts
- Public-safe setup docs

### Never commit

- Live tokens/secrets
- Session logs and private memory
- Personal uploads (PDFs/images/audio)
- Runtime DB/state files

---

## Related docs in this repo

- `agents/README.md`
- `workspace/README.md`
- `workspace/BOOTSTRAP.md`
- `openclaw.sample.json`
- `.env.example`

---

## Maintainer note

If you add automation scripts later (cron, provisioning, Telegram setup helpers), document them in a dedicated section here with:

- purpose
- required env vars
- exact inputs/outputs
- idempotent usage steps
