#!/usr/bin/env python3
"""Download all Übungen (exercises) of a DW "Deutsch lernen" lesson.

learngerman.dw.com is a JavaScript app, so this script drives a real (headless)
browser with Playwright. For every exercise of the lesson it saves:

    NN_<title>/
        uebung.pdf     printable copy of the rendered exercise page
        uebung.html    rendered HTML
        uebung.txt     plain text of the page
        media/         images, audio, video and PDFs used by the exercise
        data/          JSON the page loaded (exercise content, answers, ...)

Setup (once):
    pip install playwright
    playwright install chromium

Usage:
    python download_uebungen.py [URL] [-o OUTDIR] [--show]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urldefrag, urljoin, urlparse

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

DEFAULT_URL = "https://learngerman.dw.com/de/nico-kommt-in-deutschland-an/l-40322767/e-42382853"
MEDIA_EXTENSIONS = {".mp3", ".m4a", ".ogg", ".wav", ".mp4", ".webm", ".pdf",
                    ".jpg", ".jpeg", ".png", ".gif", ".webp"}
CONSENT_BUTTONS = ["Alle akzeptieren", "Akzeptieren", "Einverstanden", "Zustimmen",
                   "Accept all", "Accept", "I agree", "OK"]


def slugify(text, max_len=60):
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip()
    return re.sub(r"[\s_-]+", "_", text)[:max_len] or "uebung"


def safe_name(url, fallback):
    name = unquote(Path(urlparse(url).path).name) or fallback
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)


def unique_path(folder, name):
    path = folder / name
    stem, suffix, i = path.stem, path.suffix, 1
    while path.exists():
        path = folder / f"{stem}_{i}{suffix}"
        i += 1
    return path


def accept_cookies(page):
    for label in CONSENT_BUTTONS:
        button = page.get_by_role("button", name=label, exact=True)
        try:
            if button.count():
                button.first.click(timeout=2000)
                page.wait_for_timeout(500)
                return
        except PlaywrightTimeout:
            pass


def load(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except PlaywrightTimeout:
        pass  # some pages keep polling; carry on with what has loaded
    accept_cookies(page)
    # Scroll to the bottom so lazy-loaded images and players are fetched.
    page.evaluate("""async () => {
        for (let y = 0; y < document.body.scrollHeight; y += 600) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 150));
        }
        window.scrollTo(0, 0);
    }""")
    page.wait_for_timeout(1000)


def exercise_links(page, lesson_id):
    pattern = re.compile(rf"/l-{lesson_id}/e-(\d+)")
    hrefs = page.eval_on_selector_all("a[href]", "els => els.map(a => a.href)")
    links = {}
    for href in hrefs:
        href = urldefrag(href)[0]
        m = pattern.search(href)
        if m and m.group(1) not in links:
            links[m.group(1)] = href
    return links


def media_urls(page):
    """URLs of the media the rendered page uses (ignores small icons)."""
    urls = page.evaluate("""() => {
        const out = new Set();
        document.querySelectorAll('img').forEach(img => {
            if ((img.naturalWidth || img.width) >= 100) out.add(img.currentSrc || img.src);
        });
        document.querySelectorAll('audio, video, source, track').forEach(el => {
            if (el.currentSrc) out.add(el.currentSrc);
            if (el.src) out.add(el.src);
        });
        document.querySelectorAll('a[href]').forEach(a => out.add(a.href));
        return [...out];
    }""")
    return [u for u in urls if u.startswith("http")
            and Path(urlparse(u).path).suffix.lower() in MEDIA_EXTENSIONS]


def save_exercise(context, url, folder, make_pdf=True):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "media").mkdir(exist_ok=True)
    (folder / "data").mkdir(exist_ok=True)

    seen_media = set()

    def on_response(response):
        # Keep the JSON the app loads (exercise content) and media it streams.
        try:
            ctype = response.headers.get("content-type", "")
            rurl = response.url
            if not response.ok:
                return
            if "json" in ctype:
                body = response.json()
                name = safe_name(rurl, "data") or "data"
                path = unique_path(folder / "data", Path(name).stem + ".json")
                path.write_text(json.dumps({"url": rurl, "data": body}, ensure_ascii=False, indent=2),
                                encoding="utf-8")
            elif ctype.startswith(("audio/", "video/")) or ctype == "application/pdf":
                if rurl not in seen_media:
                    seen_media.add(rurl)
                    unique_path(folder / "media", safe_name(rurl, "media")).write_bytes(response.body())
        except Exception:
            pass  # e.g. streamed/partial responses without a body

    page = context.new_page()
    page.on("response", on_response)
    load(page, url)

    title = (page.locator("h1").first.inner_text() if page.locator("h1").count() else page.title()).strip()
    (folder / "uebung.html").write_text(page.content(), encoding="utf-8")
    (folder / "uebung.txt").write_text(f"{title}\n{url}\n\n{page.inner_text('body')}", encoding="utf-8")
    if make_pdf:
        page.emulate_media(media="screen")
        page.pdf(path=str(folder / "uebung.pdf"), format="A4", print_background=True)

    for media_url in media_urls(page):
        if media_url in seen_media:
            continue
        seen_media.add(media_url)
        try:
            resp = context.request.get(media_url, timeout=60000)
            if resp.ok:
                unique_path(folder / "media", safe_name(media_url, "media")).write_bytes(resp.body())
        except Exception as e:
            print(f"    ! {media_url}: {e}", file=sys.stderr)

    page.close()
    return title


def launch_browser(p, headless):
    """Use Playwright's Chromium, or fall back to an installed Chrome/Edge."""
    errors = []
    for channel in (None, "chrome", "msedge"):
        try:
            return p.chromium.launch(headless=headless, channel=channel)
        except Exception as e:
            errors.append(f"{channel or 'playwright chromium'}: {str(e).splitlines()[0]}")
    sys.exit("No browser found. Install Google Chrome, or run: python -m playwright install chromium\n"
             + "\n".join(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url", nargs="?", default=DEFAULT_URL, help="any lesson or exercise URL of the lesson")
    parser.add_argument("-o", "--outdir", default="uebungen", help="output folder (default: ./uebungen)")
    parser.add_argument("--show", action="store_true", help="show the browser window instead of running headless")
    args = parser.parse_args()

    m = re.search(r"/l-(\d+)", args.url)
    if not m:
        sys.exit("URL must contain a lesson id like /l-40322767")
    lesson_id = m.group(1)
    lesson_url = args.url[: m.end()]
    outdir = Path(args.outdir)

    with sync_playwright() as p:
        # PDF export only works headless; --show is for watching/debugging.
        browser = launch_browser(p, headless=not args.show)
        context = browser.new_context(locale="de-DE", viewport={"width": 1280, "height": 900})
        page = context.new_page()

        # Gather exercise links from both the given page and the lesson overview.
        links = {}
        for url in dict.fromkeys([args.url, lesson_url]):
            print(f"Scanning {url}")
            load(page, url)
            for ex_id, href in exercise_links(page, lesson_id).items():
                links.setdefault(ex_id, href)
        page.close()

        start = re.search(r"/e-(\d+)", args.url)
        if start:
            links.setdefault(start.group(1), args.url)
        if not links:
            sys.exit("No Übungen found on the page.")

        print(f"Found {len(links)} Übung(en). Saving to {outdir.resolve()}")
        for i, (ex_id, href) in enumerate(links.items(), 1):
            print(f"[{i}/{len(links)}] {href}")
            tmp = outdir / f"{i:02d}_{ex_id}"
            try:
                title = save_exercise(context, href, tmp, make_pdf=not args.show)
            except Exception as e:
                print(f"    ! failed: {e}", file=sys.stderr)
                continue
            final = outdir / f"{i:02d}_{slugify(title)}"
            if final != tmp and not final.exists():
                tmp.rename(final)
                tmp = final
            print(f"    -> {tmp.name}")

        browser.close()
    print("Done.")


if __name__ == "__main__":
    main()
