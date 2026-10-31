# ICE Ready SEO loop (the Vaultaire method)

Based on the Starter Story interview with Rasty Turek (Vaultaire, about $41K/month,
no paid ads). Most of his growth comes from web search:

1. **Every morning**, pull Google search data and find queries where the site
   gets impressions but no clicks.
2. **One new guide per day** targets one of those exact queries.
3. **Internal links** from existing pages point to the new guide, so Google
   finds and indexes it in a few days.
4. Every guide ends with a download call to action.

**gum** (https://gumcli.dev, github.com/ehmo/gum) is Rasty's open-source CLI and
MCP server that gives an AI agent access to Google APIs. It isn't an SEO tool on
its own. Here it's only the pipe to Search Console.

## One-time setup (Windows: run in WSL or Git Bash; macOS/Linux: terminal)

```bash
# 1. Install gum (use the tap name; plain "brew install gum" is a different tool)
brew tap ehmo/tap https://github.com/ehmo/homebrew-tap && brew install ehmo/tap/gum
#   or: curl -fsSL https://raw.githubusercontent.com/ehmo/gum/main/install.sh | bash
gum doctor

# 2. Google Cloud console (signed in as icereadyapp@gmail.com):
#    create a project, enable "Google Search Console API",
#    create an OAuth client ID (type: Desktop app), copy the ID and secret.
printf '%s' "PASTE_SECRET" | gum auth use-oauth-client --client-id "PASTE_ID" --secret-stdin
gum login --service searchconsole
gum auth status --scopes webmasters,webmasters.readonly

# 3. Confirm the property name (sc-domain:iceready.app or https://iceready.app/)
gum read searchconsole.sites.list --output json

# 4. Submit the sitemap (one time; it's a write, so it needs --allow-write)
gum write searchconsole.sitemaps.submit --allow-write \
  --args '{"siteUrl":"sc-domain:iceready.app","feedpath":"https://iceready.app/sitemap.xml"}'

# 5. Optional: let Claude Code call gum directly over MCP
gum setup --target claude --features skills,mcp --dry-run   # preview, then drop --dry-run
```

If `sites.list` shows `https://iceready.app/` instead of `sc-domain:...`, change
`SITE` at the top of `keyword_opportunities.py` and the `siteUrl` above to match.

## Daily loop (about 5 minutes of your time)

```bash
python3 tools/seo/keyword_opportunities.py
```
Then paste `tools/seo/DAILY_GUIDE_PROMPT.md` into Claude Code. It writes the
guide, wires the internal links and sitemap, and opens a PR for you to review.

## Expectations
iceready.app is new, so Search Console will show little data at first. For the
first few weeks, write guides from the seed list below. Switch to the script's
output once it starts showing real queries.

Seed list (not yet written):
- know your rights card in Spanish / tarjeta roja
- what to do if ICE comes to your house
- can police make me unlock my phone with Face ID
- how to make a family preparedness plan for deportation
- power of attorney for children if parent is detained
- how to find someone detained by ICE (ICE detainee locator)
- REAL ID vs passport card: which proves citizenship
- what is an A-number and where to find it
- Spanish versions of each guide under /es/guides/
