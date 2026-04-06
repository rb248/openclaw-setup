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

## Optional next step

If you want, you can extend this repo with:

- a private `.env.example`
- a bootstrap script that restores the local OpenClaw config
- public-safe agent templates without personal content

## Safety rule

If a file contains tokens, chat history, uploaded documents, or personal profile
information, it should stay out of GitHub.
