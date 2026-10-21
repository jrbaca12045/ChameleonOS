---
name: website_updates
description: "Update the ChameleonOS / Free Agent website and publish it to Cloudflare Pages with Wrangler. Use when updating the website, editing the site pages, deploying the site, publishing to cloudflare pages, changing the privacy policy or support page, or pointing chameleonos.online at the site."
triggers: website updates, update the website, edit the website, deploy the website, deploy the site, publish the site, cloudflare pages, wrangler deploy, update privacy page, update support page, chameleonos.online, site is stale
---

# Website Updates

The public website lives in a local folder, is edited as plain HTML, and is published to Cloudflare Pages with one Wrangler command. The Wrangler login session persists on disk, so deploys work without re-authenticating.

## The facts (verified 2026-10-21)

- **Site folder:** `C:/ai/cloudflare_pages`
  - `index.html` — landing page (1,555 bytes)
  - `privacy/index.html` — privacy policy for Microsoft Store (6,679 bytes)
  - `support/index.html` — support page for Microsoft Store (2,821 bytes)
- **Cloudflare project name:** `chameleonos`
- **Production URL:** `https://chameleonos.pages.dev`
- **Wrangler binary:** `C:\Users\jrbac\AppData\Roaming\npm\wrangler.cmd`
- **Wrangler session:** `C:\Users\jrbac\AppData\Roaming\xdg.config\.wrangler\config\default.toml`
- **Custom domain:** `chameleonos.online` — NOT YET ATTACHED. The site is live on `pages.dev` only.
- **Unrelated to the site:** `connect.chameleonos.online` is the Free Agent tunnel. Never touch that DNS record.

## How to edit the site

1. Edit the HTML files in `C:/ai/cloudflare_pages`. Keep the existing structure: `index.html` at the root, one folder per page (`privacy/`, `support/`).
2. Relative links must use absolute paths (`/privacy/`, `/support/`, `/`) so they work on any host.
3. After editing, verify the files: every internal link resolves to an existing `index.html`, and the HTML parses.
4. Deploy (see below).

## How to deploy

Run through `cmd.exe` so the `.cmd` shim resolves:

    wrangler pages deploy "C:/ai/cloudflare_pages" --project-name=chameleonos

Expected output: `Uploading... (n/n)` then `Deployment complete!` with a preview URL. The production URL updates to the new deployment.

**Do not pass an API token.** The stored OAuth session is used automatically. If Wrangler asks you to log in, the session file is missing or expired — run `wrangler login` once, in a fresh command prompt, and approve in the browser. That login is the user's step, not the model's.

## How to verify a deploy

Fetch each URL and confirm HTTP 200 and the expected `<title>`:

- `https://chameleonos.pages.dev/`
- `https://chameleonos.pages.dev/privacy/`
- `https://chameleonos.pages.dev/support/`

A 404 on `/privacy/` usually means the folder structure was flattened on upload — `privacy/index.html` must stay in its folder.

## The custom domain — not done yet

`chameleonos.online` is not attached to the Pages project. When it is, these are the rules learned the hard way:

- Attaching a custom domain is a **dashboard** action: Workers & Pages → `chameleonos` → Custom domains → Set up a custom domain.
- Cloudflare creates the DNS record automatically because the zone is in the same account.
- **Delete any existing A record on the root `@` first.** An old Wix or Spaceship A record will conflict.
- **Never touch `connect.chameleonos.online`** — that proxied Tunnel record serves Free Agent phone access.