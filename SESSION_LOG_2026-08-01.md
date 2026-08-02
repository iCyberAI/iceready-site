# ICE Ready — Session Wrap-Up August 1, 2026

**Robert Perdomo | iCyberAI LLC**
**Note:** Drive doc creation was down when this session ended — this file is the durable copy. Copy into a `ICE_Ready_SessionWrapup_Aug1_2026` Google Doc on Drive when convenient, then this file can be deleted from the repo.

---

## COMPLETED TODAY

### Runway API
- Runway account created (org name "IceReadyApp"), API key created, $8 / 1,000 credits loaded
- `tools/runway/generate.js` CLI built and merged to main — image/video generation via `RUNWAYML_API_SECRET` env var
- Confirmed working end-to-end

### iceready.app site (PR #9 merged, PR #12 in progress)
- Sticker Pack: converted from static SVG mockup to a real 2-page picker (4 stickers/page). All 8 slots now have final art (shield, Batman, Cuba alligator, Spike vs melting Blockhead, 2 ice cubes, Mex Kid, Peru Kid).
- Cap product: real photo composites, two-color picker (light blue/nickel, navy/gunmetal). Cap name fixed, logo swapped to avoid pro-ICE/MAGA look.
- Nickel shield logo: background removed (colorkey + flood-fill + connected-component cleanup + manual GIMP touch-up).
- Footer: "ICE READY" → "ICE READY APP", redundant small logo row simplified.
- Mission section: 4-image gallery with lightbox (We Are Still Here, US 250th, alternate-history map, territorial-acquisitions map).
- Added `CLAUDE.md` with environment gotchas.

### Soccer ball vendor status
- CanvasChamp: ruled out, 6-panel only.
- RAGE Custom: confirmed capable of full 32-panel design. Anton replied Aug 1 with 4 attachments — **UNREVIEWED** (Gmail MCP cannot download attachment bytes).
- Ballprint (EU): capable but not pursued, shipping cost/time.
- Wooter Apparel (US): inquiry drafted, sending not confirmed.
- Character-ball art (Peru Kid, Mex Kid, Alligator Cuba, Barney/Batman, Blockhead-Tesler, Spike/melting-Blockhead) reused for sticker pack.

### Zazzle
- Confirmed viable for caps: $12.48/unit qty 1, no MOQ, print-on-demand drop-ship.

---

## STILL OPEN / NEXT SESSION

1. Review RAGE Custom's 4 attachments (Robert to forward/view directly)
2. Confirm Wooter Apparel inquiry was sent
3. Mex Kid redesign: half-Dominican tribute to Anita/Anelle, DR flag on hat
4. 9:16 promo video assembly (Protect_Your_rights_Promo_SD-2.mp4 + tail + end card)
5. Use Seedance 2.0 from the start next promo video
6. 3rd cap concept (deferred, low priority)
7. Apocalyptic "US 300th" parody graphic — deliberately not used in Mission section, save for video content once parody video is finished
8. Crreo subscription — glitch fixed per support, decide keep/cancel before renewal

---

## KEY LESSONS

- Drive MCP `download_file_content`: for files too big for the direct response it saves full base64 to a tool-results `.txt` file instead of failing — `jq -r '.content' <file> | base64 -d > out.png` recovers it. Only truly huge files (10MB+ video) are unreachable.
- This sandbox cannot reach Google Drive's or Runway's servers directly (network egress allowlist — GitHub is on it, Drive/Runway are not).
- Gmail MCP has no attachment-download capability — filenames/IDs only.
- Pasted/dropped-inline chat images are NOT real files this session can access — only genuine file attachments or Drive uploads land on disk.
- Cowork (desktop, real filesystem/PowerShell) vs Claude Code on the web (this session, isolated cloud container) are fundamentally different — video editing and large-file work belong on Cowork.
- Background removal on a JPG with no alpha: flood-fill from image corners beats a global color threshold, which either leaves residue or eats real dark artwork sharing the same color range.
- Vendor marketing pages can overstate real capability (CanvasChamp) or understate it (RAGE Custom) — always confirm directly.
- **Drive's file-creation API can go down entirely** (confirmed Aug 1, even a trivial write failed) — have a git/local fallback ready rather than blocking on it.

---

## TOOLS STATUS

- Runway: $8 / 1000 credits loaded, CLI working, org "IceReadyApp"
- GIMP 3.2.4: installed, first use this session
- iceready-site GitHub: PR #9 merged, PR #12 open

---

## TOP PRIORITIES NEXT SESSION

1. Review RAGE Custom's 4 ball design attachments
2. Resolve Mex Kid half-Dominican redesign
3. Finish 9:16 promo video assembly
4. Confirm/send Wooter Apparel inquiry if not already sent
