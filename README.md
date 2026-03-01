# 🎲 Kallax Collection Calculator

A local web app to calculate how many **IKEA Kallax** cubes you need to store your board game collection.

## Features
- 📦 Import your BGG collection (auto-fetch via Playwright scraper or CSV upload)
- 📐 Auto-fetches physical game dimensions from BGG API
- 🏗️ Multiple packing orientations: Vertical, Horizontal, Best Fit, **Double Deep**
- 🎛️ Advanced mode: define your exact shelf configuration (e.g. 4×4 + 2×4)
- 🔍 Filter by minimum game size, exclude games with unknown dimensions
- 📊 Visual Kallax layout with per-cube game breakdowns
- 🖱️ Click any cube to see which games are packed inside

## Requirements

- Python 3.9+
- `playwright` Python package
- `requests` Python package

```bash
pip install playwright requests
playwright install chromium
```

## Usage

1. Start the local proxy server:
   ```bash
   python3 server.py
   ```
2. Open your browser at **http://localhost:8042**
3. Enter your BGG username and click **Fetch Collection**, or upload a BGG CSV export

## How It Works

`server.py` is a lightweight HTTP server that:
- Serves `index.html` as the frontend
- Proxies BGG API requests to bypass CORS restrictions
- Uses **Playwright** to scrape your full BGG collection (handles pagination)
- Fetches game dimensions from `api.geekdo.com` with a local disk cache (`dims_cache.json`)

All logic (packing, rendering, filtering) runs client-side in `index.html`.

## Files

| File | Description |
|------|-------------|
| `index.html` | The entire frontend app (single-file) |
| `server.py` | Local proxy server + BGG scraper |
| `dims_cache.json` | Cached game dimensions (auto-generated, gitignored) |
