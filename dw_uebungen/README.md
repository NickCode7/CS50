# DW Übungen downloader

Downloads every Übung (exercise) of a lesson on
[learngerman.dw.com](https://learngerman.dw.com), e.g.
[Nico kommt in Deutschland an](https://learngerman.dw.com/de/nico-kommt-in-deutschland-an/l-40322767/e-42382853).

The site is a JavaScript app, so the script uses a headless browser (Playwright).

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Run

```bash
python download_uebungen.py
```

Pass any other lesson or exercise URL to download a different lesson:

```bash
python download_uebungen.py "https://learngerman.dw.com/de/<lesson>/l-<id>/e-<id>" -o my_folder
```

Each exercise gets its own folder (`01_<title>/`, `02_<title>/`, ...) containing:

| File | Content |
|---|---|
| `uebung.pdf` | printable copy of the exercise page |
| `uebung.html` / `uebung.txt` | rendered page and its text |
| `media/` | images, audio, video and PDFs used by the exercise |
| `data/` | JSON the page loaded (exercise content and answers) |

Use `--show` to watch the browser while it scrapes (no PDF export in that mode).
