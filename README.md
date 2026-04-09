# OpenClaw setup repository

This repository is a **sanitized, shareable** version of my OpenClaw setup.
It is intentionally redacted so personal data, credentials, sessions, media, and
runtime state are not exposed on GitHub.

## Public repository policy

This repository is safe to publish publicly **only because it contains no live
tokens, private sessions, uploaded files, or machine-specific personal data**.
If you add new files later, keep them limited to templates, docs, and scripts
that do not reveal secrets or user content.

## What is included

- A safe `openclaw.sample.json` template
- A placeholder `.env.example` for local secrets
- Git ignore rules for local OpenClaw data
- Notes on how to keep private values on the local machine
- Public-safe agent prompt templates in `agents/`
- Public-safe workspace markdown templates in `workspace/`

## Layout

This repo now mirrors the OpenClaw split between **agent definition files**
and **workspace files**:

- `agents/<agent>/agent/` — public-safe agent prompts and identity files
- `agents/<agent>/workspace/` — public-safe workspace templates and memory
	placeholders

The top-level `agents/` and `workspace/` folders remain as shared templates,
while the nested folders show the same structure used by the local OpenClaw
configuration.

## What is excluded

Never commit these from a local OpenClaw install:

- `~/.openclaw/credentials/`
- `~/.openclaw/sessions/`
- `~/.openclaw/media/`
- `~/.openclaw/logs/`
- `~/.openclaw/memory/`
- `~/.openclaw/cron/runs/`
- SQLite registry/state files
- Telegram bot tokens
- Gateway auth tokens
- Personal workspaces, PDFs, images, and exported notes

## How to use this repo

1. Copy `openclaw.sample.json` to your private machine.
2. Replace placeholder values with local secrets or environment references.
3. Keep your real `~/.openclaw/` directory out of this repository.
4. Commit only safe templates, docs, and helper scripts.

## Install and run OpenClaw

If you are setting up OpenClaw locally, these are the typical first commands:

```bash
# Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# Run the onboarding wizard
openclaw onboard --install-daemon

# Check that the Gateway is running
openclaw gateway status

# Open the Control UI in your browser
openclaw dashboard
```

If you prefer to verify the UI from the terminal first, you can also launch the
interactive session view with:

```bash
openclaw tui
```

### Notes

- `openclaw onboard --install-daemon` sets up the gateway and service for your
	machine.
- `openclaw dashboard` opens the browser-based Control UI.
- `openclaw tui` is useful when you want a terminal UI for quick checks.
- If you use Telegram or another channel, keep those bot tokens private and do
	not commit them.

## Optional next step

If you want, you can extend this repo with:

- a private `.env.example`
- a bootstrap script that restores the local OpenClaw config
- public-safe agent templates without personal content

## Agent prompt templates

The `agents/` folder contains sanitized prompt files for:

- `cv-writer`
- `job-search`
- `linkedin-content`
- `interview-prep`

These are meant as public-ready templates. Keep your live auth profiles,
session history, memory files, and uploaded documents in your private OpenClaw
installation only.

## Workspace templates

The `workspace/` folder mirrors the local workspace structure with generic,
public-safe markdown files.

Real dated memory files like `workspace/memory/2026-04-06.md` are intentionally
left out of the public repo because they are private notes.

## Safety rule

If a file contains tokens, chat history, uploaded documents, or personal profile
information, it should stay out of GitHub.
