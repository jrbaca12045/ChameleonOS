# ChameleonOS

The free library behind **ChameleonOS** - the operating system for web chats.

ChameleonOS turns any web chat into something that can actually operate your Windows PC. This repository holds the parts of the project that are free to read, copy, and use: the skills, the example scripts, and the persona definitions.

The app itself is distributed through the Microsoft Store. This repo is the library, not the installer.

## What is here

### `skills/`

The skill library. Each folder contains one `SKILL.md` file: a procedure written for an AI agent to follow, with frontmatter that makes it discoverable by trigger. Skills cover adding a new skill, systematic debugging, MSIX store packaging, documentation maintenance, website updates, and more.

If you want to see how an AI agent can be taught to do a repeatable job well, this is the folder to read.

### `example-scripts/`

Seven self-contained clusters of working Python, each with its own README and setup guide:

| Cluster | What it does |
|---|---|
| `check_disk_space` | Report disk usage for a drive or path, warn above 80 percent |
| `voice_switching` | List and select Windows speech voices |
| `window_listing` | List visible windows with process, PID, and title |
| `mouse_coordinates` | Live mouse position display |
| `ui_automation` | Inspect, wait for, and act on Windows UI controls |
| `email` | Gmail check and send via App Password; credentials read from a separate file, never included |
| `chameleonos-qr` | The site QR code and the script that made it |

Each cluster is standalone. Copy a folder anywhere and run it - it does not require ChameleonOS to be installed.

### `personas/`

The persona definitions. Each persona is a short text file describing a voice and posture an AI agent can adopt, plus an activation file that defines how it introduces itself and verifies it is running.

These are written to be read. They show how a general-purpose model can be given a stable role without fine-tuning.

## About the project

ChameleonOS was built over seven months by one person without a code background, working with AI. It grew the way a tool grows when someone actually needs it: hit a problem, try something, keep what works.

Every file here exists because it was needed. None of it is a demo.

## Using this library

Everything here is plain text and Python. There is no build step and no package to install to read it.

- **To read a skill:** open its `SKILL.md` in the matching folder under `skills/`. The frontmatter at the top tells you when the skill applies. The body tells you what to do.
- **To run an example script:** open the cluster folder and read its `setup.txt`. It tells you what to install, what config to create, and how to test it.
- **To use a persona:** copy its `.txt` file into your own agent setup. The matching `_activation.txt` describes how the agent should introduce itself and how it checks that it is running the right persona.

## What this repository is not

- It is not the ChameleonOS installer. The app is sold and delivered through the Microsoft Store.
- It is not the full application source. The library is published openly; the compiled application is a separate product.
- It does not include runtime state or credentials. Those stay local to each installation by design.

## Requirements

The example scripts target **Windows** and **Python 3.8 or newer**. Some clusters have additional dependencies, listed in their own `setup.txt`. Nothing in this repository requires ChameleonOS to be installed.

## License

Code in `example-scripts/` and the text in `skills/` and `personas/` are provided for reading and reuse. If you build something with them, a link back is appreciated but not required.

## Links

- **Store listing:** the ChameleonOS app on the Microsoft Store
- **Website:** https://chameleonos.online
- **Privacy policy:** https://chameleonos.online/privacy/
- **Support:** https://chameleonos.online/support/

---

Built over seven months. Grown by use.