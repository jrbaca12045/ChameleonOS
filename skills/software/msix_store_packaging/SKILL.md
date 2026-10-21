---
name: msix_store_packaging
description: Build, sign, and submit the ChameleonOS/Free Agent Microsoft Store package correctly. Use when rebuilding the store MSIX, the signed test MSIX, or when anything about the payload, version number, publisher, or signing changes. Covers every failure mode that has bitten this project.
---

# MSIX Store Packaging — Complete Procedure

Read this before touching any MSIX, before bumping any version, before running any build.
Every rule below was learned by making the mistake.

## 1. The two packages

Two MSIX files are produced from the same payload. They are NOT interchangeable.

| Package | File | Publisher | Signed? |
|---|---|---|---|
| Store upload | `ChameleonOS_StoreUpload.msix` | `CN=647F11C2-C086-4EA5-AFEC-02C8A1FA898C` | NO — Partner Center re-signs |
| Local test | `ChameleonOS_LocalTest.msix` | `CN=FreeAgent` | YES — self-signed with thumbprint `B0E2C6628F389B080AC688FFFEA4FFC477B7D02C` |

Both use the same identity `Progenitorfreeagent.ChameleonOS` and same version.
The ONLY differences are Publisher field and signing.

## 2. Where everything lives

- Packaging root: `C:/ai/Setup Free Agent`
- Staging (store): `C:/ai/Setup Free Agent/HelloTest/stage_store`
- Staging (test): `C:/ai/Setup Free Agent/HelloTest/stage_test`
- Output (store): `C:/ai/Setup Free Agent/HelloTest/ChameleonOS_StoreUpload.msix`
- Output (test): `C:/ai/Setup Free Agent/HelloTest/ChameleonOS_LocalTest.msix`
- Built payload: `C:/ai/Setup Free Agent/HelloTest/payload_final_v2.zip`
- Manifest source: `C:/ai/Setup Free Agent/HelloTest/stage_store/payload.zip` (old one — the manifest of record is this file's contents)
- makeappx: `C:/Program Files (x86)/Windows Kits/10/bin/10.0.26100.0/x64/makeappx.exe`
- signtool: `C:/Program Files (x86)/Windows Kits/10/bin/10.0.26100.0/x64/signtool.exe`
- Cert: `C:/ai/Setup Free Agent/FreeAgent_Trust.cer` (764 bytes)
- Cert thumbprint: `B0E2C6628F389B080AC688FFFEA4FFC477B7D02C`

## 3. The stage folders

`stage_store/` and `stage_test/` contain EXACTLY 5 files each. No more.

1. `AppxManifest.xml` (store: Publisher=CN=647F..., test: Publisher=CN=FreeAgent)
2. `FreeAgentLauncher.exe` (316,928 bytes, from Launcher project)
3. `logo_150.png` (40,651 bytes)
4. `logo_44.png` (4,517 bytes)
5. `payload.zip` (~206 MB)

**GUARD BEFORE EVERY PACK.** Count files in the stage folder. If it is not 5, stop.
A 6th file is a bug — it will get packed into the MSIX.

## 4. What ships in the payload (inside payload.zip)

Source of truth for the file list: the contents of the CURRENT `stage_store/payload.zip`.
Roughly 656 entries. To that list, each release may add files (see section 9).

What ships:
- All Application/ files (Free Agent.exe, .dll, .deps.json, .runtimeconfig.json)
- Automation/ (all scripts and JSON)
- cua-driver/ (all daemons, launchers, screen_geometry.py, cua_client.py)
- Whisper/, runtimes/, dict/, models/ (including ggml-base.bin 147,951,465 bytes)
- AISpace/ (including automation_inventory.json — must be 48 entries or more)
- persona/, persona_memory/, personalities/, profiles/, skills/, updated_docs/
- docs/, icons/, logs/, memory/, memory_settings.json, prompt_scripts/, recordings/
- Root tools: universal_automate.py, capture.py, profile_wizard.py, install_dependencies.py
- populate_skill_triggers.py, apply_skill_triggers.py, promote_memory.py
- list_voices_to_file_v2.py, select_voice_v2.py, speechma_scroll_top.py, speechma_tts_final_v10.py
- FirstRunSetup.ps1, agent_memory.db (sanitized), README.txt
- facebook/desktop_scanner_20.py, facebook/ocr_menu_template.py

## 5. What must NEVER ship in the payload

- `Application/Free Agent.pdb` — debug symbols, not needed
- `updated_docs/msix_packaging_sop.txt`, `updated_docs/msix_build_sop.md` — internal SOPs
- `updated_docs/chameleonos_site_copy.md` — website copy draft
- `secrets/gmail.json` — personal credential (the real one)
- `gmail_app_pass.py` — ONLY IF it contains hardcoded credentials. If it reads from secrets/gmail.json, it is safe to ship.
- `universal_email_config.json` — contains personal email config
- Any file matching `*.bak_*`, `*.bak`, `*.broken_*`
- `HelloTest/` (the whole folder is build artifacts)
- `Launcher/` (source + build output, only the built exe ships)
- `Application_bak_*` folders
- Any file in `secrets/` except `*.example`

## 6. The version rules (Microsoft Store)

This is the rule that rejected v1.0.0.1 on first submit:

**The 4th segment (Revision) of the version must be 0.** `1.0.0.1` is illegal. `1.0.1.0` is legal. `1.0.0.0` is legal.

Second rule: **you cannot re-upload the same version with different contents.** If 1.0.0.0 is already validated in Partner Center, the next submission must be 1.0.1.0 or higher.

Version bump recipe:

```
# in stage_store/AppxManifest.xml:
#  Version="1.0.1.0"  becomes  Version="1.0.2.0"
```

The test package can stay at any version. Local Add-AppxPackage does not enforce the revision-zero rule.

## 7. The publisher/signing rule

**The manifest `Publisher` attribute must EXACTLY match the signing certificate's Subject.**

- Store package Publisher: `CN=647F11C2-C086-4EA5-AFEC-02C8A1FA898C` (store identity, does NOT match any local cert)
- Test package Publisher: `CN=FreeAgent` (matches `B0E2C6628F389B080AC688FFFEA4FFC477B7D02C`)

If they do not match, `signtool sign` fails with:
```
Error: SignerSign() failed. (-2147024885/0x8007000b)
```

That error is not diagnostic. It always means Publisher mismatch or another manifest identity problem.

**For the store package, do NOT sign it yourself.** Partner Center re-signs during certification. If you sign it locally with CN=FreeAgent, the package will be rejected as having a Publisher that does not match the declared one.

## 8. Step-by-step build
### 8.1 Sync code from live to Setup (before every build)

Files that change in live (`C:/ai/`) must be copied to Setup (`C:/ai/Setup Free Agent/`) before the payload is packed.

The six daemons — copy each one:
```
deepseek_daemon.py  → Setup/cua-driver/
gemini_daemon.py    → Setup/cua-driver/
copilot_daemon.py   → Setup/cua-driver/
qwen_daemon.py      → Setup/cua-driver/
chatgpt_daemon.py   → Setup/cua-driver/
capriole_daemon.py  → Setup/cua-driver/
screen_geometry.py  → Setup/cua-driver/  (helper, referenced by all six)
```

The VB app — publish from Visual Studio, then copy the output:
```
Free Agent.exe, .dll, .deps.json, .runtimeconfig.json  → Setup/Application/
```

Verify each copy: source size equals destination size.

### 8.2 Bump version if this is a new store submission

Edit `stage_store/AppxManifest.xml`. Bump the third segment, keep fourth at 0.

### 8.3 Build the payload

Read the manifest from `stage_store/payload.zip`. For each entry, copy fresh bytes from Setup.
Add any files new to this release. Write to `payload_final_v2.zip`.

Verify:
- Total entries = manifest count + new adds
- `models/ggml-base.bin` is 147,951,465 bytes
- `Application/Free Agent.exe` is the new size
- All six daemons at the new sizes
- No forbidden files present

### 8.4 Swap payload into stage_store

Back up the old payload FIRST, to `HelloTest/`, NOT into `stage_store/`.

Then copy `payload_final_v2.zip` over `stage_store/payload.zip`.

**Count files in stage_store/ — must be 5.**

### 8.5 Pack the store package

```
makeappx pack /d stage_store /p ChameleonOS_StoreUpload.msix /o
```

Verify immediately after:
- 7 top-level entries, not 8
- No file with `bak` in its name
- Embedded manifest Version is correct
- `signtool verify /pa` returns error (package is unsigned — that is correct)

### 8.6 Update stage_test and pack the test package

Copy the same payload to `stage_test/payload.zip`.
Count files in stage_test/ — must be 5.

```
makeappx pack /d stage_test /p ChameleonOS_LocalTest.msix /o
```

### 8.7 Sign the test package

```
signtool sign /fd SHA256 /sha1 B0E2C6628F389B080AC688FFFEA4FFC477B7D02C /a ChameleonOS_LocalTest.msix
```

Expected output: `Successfully signed: ...`

### 8.8 Verify the test package

```
signtool verify /pa ChameleonOS_LocalTest.msix
```

Must print `Successfully verified`. If not, the package is not usable on a test machine.

### 8.9 Final verification of BOTH packages
For each MSIX:
1. Open as zip, read `AppxManifest.xml`
2. Confirm Version, Publisher, Name
3. Extract `payload.zip` to temp, open it as zip
4. Confirm entry count matches expectation
5. Confirm models/ggml-base.bin size
6. Confirm Application/Free Agent.exe size
7. Confirm no forbidden files
8. Confirm `AISpace/automation_inventory.json` has expected entry count
9. For test package: `signtool verify /pa` returns success
10. For store package: unsigned (signtool verify returns error)

## 9. Adding files to the payload

When a new file must ship:
1. Copy it from live to Setup
2. Add its relative path to the build script's ADD list
3. Verify the payload contains it at expected size
4. If it is in a new folder that does not exist yet in the payload, that folder must be created — the build script handles this automatically

Examples added this session: `cua-driver/screen_geometry.py`

## 10. The failure modes we actually hit

Each of these happened. Each cost time. Each is prevented by the rules above.

### F1 — Backup file leaked into stage_store

I created `payload.zip.bak_20261019_1216` inside `stage_store/` during backup. `makeappx` packed both the payload and its 77 MB backup. Store MSIX came out at 282 MB instead of 206 MB.

**Fix:** backups go to `HelloTest/`, never to `stage_store/`. Count files before pack — must be 5.

### F2 — Same mistake twice

The next rebuild, I made the same error. This time the package came out at 411 MB.

**Fix:** the guard (count == 5) is mandatory. Do not pack if count is wrong.

### F3 — Publisher mismatch on test package

Copied stage_store to stage_test without changing Publisher. Tried to sign with `CN=FreeAgent`. SignTool returned `0x8007000B` with no useful message.

**Fix:** stage_test manifest Publisher must be `CN=FreeAgent`, not the store GUID. Two different manifest files for the two staging folders.

### F4 — Store rejected v1.0.0.1

Bumped to `1.0.0.1` and uploaded. Partner Center validation error: "Apps are not allowed to have a Version with a revision number other than zero."

**Fix:** bump the 3rd segment, not the 4th. `1.0.1.0`, not `1.0.0.1`.

### F5 — Daemons not copied to Setup

Edited six daemons in live. Built the payload. Payload got the OLD versions. The new daemons were never copied to `Setup/cua-driver/`.

**Fix:** sync live → Setup BEFORE building. Verify each copy by size.

### F6 — `screen_geometry.py` not in the manifest

New helper file referenced by all six daemons. Not in the manifest, so the build script did not include it.

**Fix:** any NEW file must be added to the build script's ADD list. Adding it to the manifest once does not update the manifest source, so this is an explicit add every rebuild until the manifest is regenerated.

## 11. The version history

| Version | What changed | Published? |
|---|---|---|
| 1.0.0.0 | Initial store upload | Yes — validated in Partner Center |
| 1.0.0.1 | Bumped after daemon changes | REJECTED — illegal revision |
| 1.0.1.0 | Legal version, daemons + screen_geometry + VB updates | Built, not yet uploaded (superseded by 1.0.1.0 rebuild with the new payload) |

Next legal version for a new submission: **1.0.2.0**

## 12. Test on a clean machine

Before declaring the store package good, install the test package on a machine without existing Free Agent installation.

Steps:
1. Import cert: `Import-Certificate -FilePath FreeAgent_Trust.cer -CertStoreLocation Cert:\LocalMachine\TrustedPeople` (elevated)
2. Install: `Add-AppxPackage -Path ChameleonOS_LocalTest.msix`
3. Click Free Agent tile, answer working folder prompt, wait for unpack
4. Verify `C:/ai/cua-driver/screen_geometry.py` exists
5. Verify `C:/ai/Application/Free Agent.exe` is the new size
6. Verify `C:/ai/models/ggml-base.bin` is 147,951,465 bytes
7. Open one daemon — it should open at 80% of the screen, centered
8. Check `C:/ProgramData/FreeAgent/launcher_log.txt` for clean unpack

## 13. What to hand to Partner Center

1. Upload `ChameleonOS_StoreUpload.msix` (unsigned)
2. In Submission options, submit a restricted capability justification for `runFullTrust`:

   > ChameleonOS is a packaged desktop application (Win32 via Desktop Bridge). It requires `runFullTrust` to launch its native executable, `FreeAgentLauncher.exe`, and to unpack and run its local AI agent payload. This is the standard full-trust capability for packaged desktop apps.

3. Wait for certification
4. Do not sign the store package yourself — Partner Center re-signs

## 14. When to re-run this whole procedure

- Any change to `Application/` (VB rebuild)
- Any change to a daemon (or to `screen_geometry.py`)
- Any new file that should ship
- Any new store submission (bump version)
- Any fix to a file that is in the payload

## 15. What to check if something looks wrong

If the store package is larger than ~210 MB:
- A backup file leaked into stage_store. Check the pack output for a `Processing` line that mentions a `bak` file.

If the store rejects the version:
- The 4th segment is not 0. Read `Version="1.0.X.Y"` — Y must be 0.

If signing fails with 0x8007000B:
- Manifest Publisher does not match the cert subject. Store test package: Publisher must be `CN=FreeAgent`. Store package: not signed at all.

If a daemon or file has the OLD contents on the installed machine:
- The file was not copied live → Setup before the payload build.

If the payload is missing a file:
- The file is not in the build script's ADD list.

