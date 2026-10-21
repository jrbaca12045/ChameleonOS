---
name: telegram
description: Telegram communication through Free Agent bot access. Use when receiving, checking, replying to, or sending Telegram messages.
---

# Telegram Communication

## When to use this
Use this skill when Free Agent needs to communicate through Telegram or test its Telegram connection. Telegram is the communication channel; Free Agent remains responsible for the model, persona, skills, memory, commands, and orchestration.

## Procedure
1. Confirm Telegram bot configuration is available without displaying the bot token.
2. Use C:/ai/telegram_test.py when a connection test is required.
3. Receive Telegram updates and identify the accessible chat, sender, message, and reply or topic context.
4. Apply authorization and allowlist rules before acting. In groups, respect mention and reply requirements. Prevent replies to the bot itself and bot-to-bot loops.
5. Generate the response using the active Free Agent persona, skills, memory, and normal reasoning.
6. Send the response to the originating authorized chat and preserve reply or topic context when available.
7. Split responses that exceed Telegram message limits instead of truncating them.
8. Handle transient network and rate-limit failures safely. Never expose credentials or unnecessary raw API responses.

## Current capability boundary
The current integration uses the Telegram Bot API. It can communicate in chats the bot can access, including private chats with the bot and supported groups, supergroups, channels, and topics. Bot access does not provide access to the user's entire personal Telegram inbox. Full personal-account access would require a separate user-account client such as an MTProto integration.

## Hermes capability map
Hermes treats Telegram as a platform adapter. Its researched capability surface includes receive/send, private and group chats, topics and reply context, allowlists, mention gates, slash commands, inline keyboards, approvals, streaming or draft updates, message splitting, retry and flood handling, media and documents, locations and venues, reactions, and topic/session bindings.

For Free Agent, develop this progressively:
- Phase 1: status, receive/send, authorization, private/group chats, reply context, message splitting, retry/error handling, loop prevention.
- Phase 2: personas, skills, memory, commands, automation, scheduler, files, persistent sessions.
- Phase 3: streaming edits, inline keyboards, approvals, clarification, model and skill pickers, reactions, forum topics, media, sticker vision, webhooks, topic and skill bindings, network fallback.

## What NOT to do
- Do not claim Bot API access can read the entire personal Telegram account.
- Do not expose TELEGRAM_BOT_TOKEN or other credentials.
- Do not invent messages the bot has not received.
- Do not send to arbitrary or unauthorized chats.
- Do not create reply loops.
- Do not silently truncate long responses.

## Related
C:/ai/skills/chameleon_map/telegram_platform.md contains the Hermes research and Free Agent adaptation map.
C:/ai/telegram_test.py is the existing Telegram connection test harness.