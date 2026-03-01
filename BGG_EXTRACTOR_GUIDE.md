# BGG Dimension Extractor - How to Use

## Quick Start

### Step 1: Get the Script
The script is in: `bgg_extractor_console.js`

Copy the entire contents of that file.

### Step 2: Open BGG in Your Browser
Go to any of these:
- Your individual game page (e.g., `https://boardgamegeek.com/boardgame/13/catan`)
- Your Board Game Collection (e.g., `https://boardgamegeek.com/collection/user/`)

### Step 3: Open Developer Tools
Press `F12` or Right-click → Inspect → go to **Console** tab

### Step 4: Paste & Run
1. Click in the Console area (at the `>` prompt)
2. Paste the entire script
3. Press Enter

### Step 5: Download CSV
A CSV file will automatically download with dimensions for all games found on the page.

## What the Script Does

✅ **Detects page type**:
  - Collection page → Scans all games in table
  - Single game page → Extracts that game's dimensions

✅ **Parses dimensions** like:
  - "12.0 x 8.0 x 5.0 cm"
  - "29.5 × 29.5 × 7.5 cm"
  - "12.0 x 8.0 x 5.0 inches"

✅ **Extracts**:
  - Game ID
  - Game Name
  - Length, Width, Height (in cm)

✅ **Generates CSV** with format:
  ```
  Game ID,Game Name,Length (cm),Width (cm),Height (cm)
  13,"Catan",29.5,29.5,7.5
  298619,"15 Days",12.0,8.0,5.0
  ```

## Tips for Best Results

### For Collection Pages
- The script scans visible rows
- If you have many games, scroll through to load more before running
- Or run the script multiple times while scrolling

### For Single Game Pages
- Make sure the "Size" or "Dimensions" section is visible
- Scroll down to the Versions section if dimensions aren't showing
- You'll need to run this once per game

### Batch Processing
1. Open each game in a new tab/window
2. Run the console script on each
3. Let each download a CSV
4. Combine all CSVs into one file:
   ```
   # On your computer, combine all CSVs:
   cat bgg_dimensions_*.csv > all_dimensions.csv
   ```
5. Upload the combined CSV to the app

## Import into Shelf Planner

Once you have the CSV:
1. Open the Shelf Planner app (`index.html`)
2. Load your BGG collection
3. Use the "📋 Batch Edit" button to update dimensions
4. Or upload the CSV directly if that feature exists

## Troubleshooting

**Script runs but finds 0 games:**
- You might be on a page without dimension data visible
- Try scrolling to the Versions section
- Check that dimension field is populated on BGG

**"No console visible":**
- Try `Ctrl+Shift+J` (Windows/Linux) or `Cmd+Option+J` (Mac)
- Or Right-click → Inspect → Console tab

**Script errors:**
- Make sure you copied the ENTIRE script without modifications
- Check for red X icons in the console
- Try on a different game page

**CSV doesn't download:**
- Check your browser's download settings
- Look for a popup asking to allow downloads
- File goes to your Downloads folder by default

## Security Note

This script:
- ✅ Only reads visible page content (no network requests)
- ✅ Runs entirely in your browser
- ✅ Doesn't send data anywhere
- ✅ Safe to use with your personal BGG collection

