# ustrema.com: coming soon

The holding page for [ustrema.com](https://ustrema.com). It is a static site on GitHub Pages: plain HTML, CSS and a small inline script. It has no framework and no third-party requests.

- English at `/`, Bulgarian at `/bg/`, linked with `hreflang`.
- Background: the Ustrema u, built from hundreds of 30° blades in oblique projection. A slow wave runs through it along the brand's 30° axis. The pointer lifts the field and a click or tap sends a ripple. It renders on a canvas from pre-rendered blade images, starts only once the page is idle, and freezes into a still frame under `prefers-reduced-motion`.
- Lighthouse, mobile and desktop, EN and BG: Performance 100, Accessibility 100, Best Practices 100, SEO 100 (checked 14 Oct 2026 on a gzip-serving local server).
- Search and answer engines: canonical and `hreflang`, Open Graph and Twitter cards, Organization / WebSite / WebPage JSON-LD, `sitemap.xml`, `robots.txt` (AI crawlers allowed) and [`llms.txt`](llms.txt).

## Editing

Do not edit `index.html` or `bg/index.html` by hand. They are generated.

1. Change the copy in `build.py` (the `STRINGS` block) or the markup, styles and script in `src/template.html`.
2. Run `python3 build.py` (Python 3, standard library only).
3. Preview with `python3 -m http.server 8766`, then open http://localhost:8766.
4. Commit and push to `main`. GitHub Pages redeploys in about a minute.

House rules: no em or en dashes in copy (the build fails on them), Microsoft product names in full on first mention, no partner-status claims until Partner Center confirms them.

## Files

| Path | What it is |
| --- | --- |
| `src/template.html` | Page template: markup, CSS, script |
| `src/logo.svgfrag` | The approved wordmark, split into one path per letter for the intro |
| `build.py` | Renders both languages and writes `sitemap.xml`, `robots.txt`, `llms.txt` and `manifest.webmanifest` |
| `fonts/` | Manrope 600 to 800, Onest 400 and JetBrains Mono 500, subset to Latin and Cyrillic (69 KB total, OFL) |
| `assets/` | Favicons, app icons, `og.jpg` share image |
| `404.html` | Not-found page |
| `.nojekyll` | Tells Pages to serve files as they are |

---

## Putting the site on ustrema.com

**Status (14 Oct 2026):** live at **https://ustrema.com**. The custom domain is set in Pages (the `CNAME` file), and Cloudflare serves the site with its proxy on (orange cloud). The old github.io address redirects to it.

Two setups work. Use one of them, not a mix.

- **A. Cloudflare proxy on (current setup).** Cloudflare issues the certificate and caches the site. GitHub cannot issue its own certificate behind the proxy, so leave GitHub's "Enforce HTTPS" off and do these steps in Cloudflare instead:
  - **SSL/TLS** → **Overview**: set the mode to **Full**. Avoid **Flexible**: it sends traffic to GitHub unencrypted. Avoid **Full (strict)**: it fails, because GitHub has no certificate for ustrema.com.
  - **SSL/TLS** → **Edge Certificates**: turn on **Always Use HTTPS**. At the moment http://ustrema.com still answers on plain HTTP.
  - Then do step 1 below, the domain verification.
- **B. DNS only (grey cloud).** GitHub issues the certificate and enforces HTTPS. Follow steps 1 to 5 below exactly.

The steps below describe setup B in full. They are also the reference if the records ever need rebuilding. The domain is registered with Cloudflare, so the DNS steps happen in the Cloudflare dashboard.

### 1. Verify the domain for the GitHub organisation (5 minutes, do this first)

This stops anyone else from pointing a GitHub Pages site at ustrema.com.

1. GitHub → **ustrema** organisation → **Settings** → **Pages** (under "Code, planning, and automation") → **Add a domain** → enter `ustrema.com`.
2. GitHub shows a TXT record. It looks like `_github-pages-challenge-ustrema` with a random value.
3. In Cloudflare → **ustrema.com** → **DNS** → **Records** → **Add record**:
   - Type `TXT`, Name `_github-pages-challenge-ustrema`, Content: the value from GitHub. TTL Auto.
4. Back in GitHub, click **Verify**. It may take a few minutes to go through.

### 2. Point the domain at GitHub Pages (Cloudflare DNS)

In Cloudflare → **ustrema.com** → **DNS** → **Records**:

1. **Delete** any existing `A`, `AAAA` or `CNAME` records for `ustrema.com` (shown as `@`) and for `www`. These are often parking records.
   **Do not touch** `MX` records or `TXT` records for SPF, DKIM or DMARC. They carry email, including hello@ustrema.com.
2. **Add** these records. Set every one to **Proxy status: DNS only** (grey cloud):

| Type | Name | Content |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `ustrema.github.io` |

Why **DNS only**: GitHub issues the free HTTPS certificate itself (Let's Encrypt). Cloudflare's orange-cloud proxy hides the domain from that check, so issuing and renewing the certificate can fail. GitHub Pages already sits on a global CDN, so the proxy adds little here.

### 3. Tell GitHub Pages to use the domain

Choose one:

- **In the browser**: repo **ustrema/ustrema.com** → **Settings** → **Pages** → **Custom domain** → type `ustrema.com` → **Save**. GitHub commits a `CNAME` file to the repo. Pull before your next push (`git pull`).
- **From the terminal**:

  ```bash
  gh api -X PUT repos/ustrema/ustrema.com/pages -f cname=ustrema.com
  ```

GitHub then runs a DNS check, which shows as "DNS check in progress" and usually finishes within 10 to 30 minutes. `www.ustrema.com` redirects to `ustrema.com` automatically.

### 4. Turn on HTTPS

When the DNS check is green and the certificate is issued (up to about an hour), tick **Enforce HTTPS** on the same Pages settings screen. From the terminal:

```bash
gh api -X PUT repos/ustrema/ustrema.com/pages -F https_enforced=true
```

If the option stays greyed out, wait. If it is still greyed out after an hour, remove the custom domain, save, add it again and save. That restarts certificate issuance.

### 5. Check it

```bash
dig ustrema.com +short
```

This should list the four `185.199.10x.153` addresses.

```bash
curl -sI https://ustrema.com | head -1
```

This should print `HTTP/2 200`.

```bash
curl -sI http://www.ustrema.com | grep -i location
```

This should redirect to `https://ustrema.com/`.

Then open https://ustrema.com, https://ustrema.com/bg/ and https://ustrema.com/llms.txt in a browser.

### 6. After launch: register with search and answer engines

1. **Google Search Console**: add the domain property `ustrema.com`. Cloudflare can add the verification TXT record in one click. Then submit `https://ustrema.com/sitemap.xml`.
2. **Bing Webmaster Tools**: import the site from Search Console and submit the sitemap. Bing's index feeds Microsoft Copilot and ChatGPT search, so this matters for answer engines.
3. Make sure **hello@ustrema.com** receives mail before you share the page, for example with Cloudflare **Email Routing**: Email → Email Routing → add `hello` and forward it to a real inbox.

### What does not change

The brand guide stays at https://ustrema.github.io/brand-guide-ustrema/. A custom domain on a project repository only applies to that repository.

---

Microsoft, Power Platform, Copilot and Dynamics 365 are trademarks of the Microsoft group of companies.
