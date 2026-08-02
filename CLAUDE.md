# iceready-site — working notes for Claude Code sessions

Static site for the ICE Ready app (`iceready.app`), plain HTML/CSS/JS in `index.html`, deployed via GitHub Pages from `main`. No build step.

## Environment gotchas (learned the hard way)

- **This sandbox cannot reach Google Drive's download servers, Runway's API, or most external hosts directly.** The egress proxy allowlists GitHub and a few others only. Don't waste time retrying `curl` against drive.google.com or dev.runwayml.com — it will 403.
- **Google Drive MCP `download_file_content` works, but caps around 10MB and often exceeds the tool's own token limit for anything over ~1-2MB.** When that happens, the tool saves the full base64 response to a local `.txt` file under `tool-results/` instead of erroring out uselessly. Decode it yourself:
  ```
  jq -r '.content' "<path from error message>" | base64 -d > output.png
  ```
  This works for files well past what would fit in a chat response — no real size ceiling other than disk.
- **Files over ~10MB (most videos) can't come through the Drive connector at all.** Ask the user to upload as a real chat attachment instead (`/root/.claude/uploads/<session>/`) — but note pasted/dropped-inline images do NOT land there, only genuine file attachments do. If `ls` on uploads doesn't show it, it wasn't a real upload.
- **Gmail MCP has no attachment-download tool** — `get_thread`/`get_message` return attachment filenames/IDs only, never bytes. Can't inspect email attachments directly; ask the user to forward/save them elsewhere.
- ffmpeg, GIMP, and Python (PIL/numpy/scipy, install on demand with `pip install`) are all available locally for real image editing — background removal, compositing, cropping. Prefer flood-fill from image corners (not global color-threshold) for background removal; it survives busy/textured backgrounds far better. Use connected-component size filtering (`scipy.ndimage.label`) to clean up stray specks without eroding real linework.
- A local `python3 -m http.server` + Playwright (`/opt/pw-browsers/chromium`) is the way to verify any HTML/CSS change actually renders before committing — don't just trust markup by eye.

## Git/PR workflow

- Designated branch: `claude/runway-mcp-integration-izhppx`. If its PR gets merged, **restart the branch fresh off `main`** (`git fetch origin main && git checkout -B <branch> origin/main`) before adding new commits — don't keep building on the old, now-merged branch tip.
- This repo's PRs open as drafts by default; mark ready + merge only when the user explicitly says so.

## Where the project history lives

Robert keeps daily session-wrap docs on Google Drive (`icereadyapp@gmail.com`), named `ICE_Ready_SessionWrapup_<Month><Day>_2026`. Check there for prior decisions, character specs, vendor status, and deadlines before assuming something hasn't been figured out yet — a lot of design/character/brand decisions (Blockhead spec, Barney gag, flag rules, etc.) are already locked in separate spec docs on that same Drive, searchable by keyword.

## Runway CLI

`tools/runway/generate.js` — Node CLI wrapping the Runway API for image/video generation. Reads `RUNWAYML_API_SECRET` from env. Run locally (not from this sandbox — no network path to Runway).
