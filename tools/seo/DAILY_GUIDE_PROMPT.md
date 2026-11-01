# Daily guide prompt (paste into Claude Code, run in the iceready-site repo)

Read the newest `tools/seo/opportunities-*.md`. Pick the ONE highest-ranked query
that no existing page in `/guides/` already covers. Then:

1. Research the topic with web search. Use primary sources (uscode.house.gov,
   uscis.gov, ACLU state affiliates, NILC, ILRC, Nolo). Legal claims must be cited.
2. Write `/guides/<keyword-slug>.html`, using
   `/guides/what-documents-to-carry-if-stopped-by-ice.html` as the template:
   - `<title>` and `<h1>` contain the exact query wording
   - "Short Answer" box first, answering the query in 2 to 3 sentences
   - Article + BreadcrumbList + FAQPage JSON-LD (validate that it parses)
   - App Store / Google Play CTA box at the natural end of the article
   - "Related guides" block linking 2 existing guides
   - Sources line and a "not legal advice" note
3. Internal links (this is what gets Google to index the page fast):
   - Add an entry at the top of the `GUIDES:START` list in `/guides/index.html`
   - Add a link to the new guide from the 1 or 2 most related existing guides
   - If it's a top performer later, add it to the homepage "Free Guides" strip
4. Add the URL to `sitemap.xml` with today's `lastmod`.
5. Commit on a branch, open a PR, and give me the summary.

Hard rules for ICE Ready copy:
- NEVER say or imply ICE Ready encrypts documents. The device's OS does the
  encryption. ICE Ready's protection is offline-only storage plus PIN lock,
  triple-tap lock, and 30-second auto-lock.
- NEVER say a phone copy replaces carrying originals. For noncitizens 18+,
  8 U.S.C. 1304(e) requires the original registration document.
- No fabricated stats, quotes, or testimonials. One guide per day, quality over volume.
