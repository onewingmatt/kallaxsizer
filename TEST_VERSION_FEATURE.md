# Version Selection Feature in Edit Modal

## What's New

The edit dimensions modal now displays available versions (editions) of a game from BoardGameGeek and lets you select one to populate the dimensions automatically.

### Features

✅ **Auto-fetch versions**: When you open the edit modal, it automatically fetches all available editions/versions for that game from BGG  
✅ **Display options**: Shows version name, year, publisher, and dimensions  
✅ **One-click selection**: Click any version to instantly populate the L×W×H fields  
✅ **Smart sorting**: Versions are sorted by largest dimension (most relevant modern editions first)  
✅ **Highlight current**: If a version matches your current dimensions, it's highlighted  
✅ **Fallback**: Works gracefully even if server isn't available—just shows the manual input fields  

## How to Use

1. Load your collection into the Kallax app
2. Click on any game's name or dimensions to open the **Edit Dimensions** modal
3. Look for the **📦 Available Versions from BGG** section at the top
4. Click any version to populate the L/W/H fields with its dimensions
5. Adjust if needed, then click **Save**

## Technical Details

### Client-side (index.html)
- Enhanced `openEditModal()` function now async
- Fetches from `/api/versions?id=GAME_ID`
- Displays clickable version list with inline selection
- Falls back gracefully if endpoint unavailable

### Server-side (server.py)
- New `/api/versions` endpoint
- `fetch_game_versions(game_id)` function
- Fetches up to 10 versions per game
- Uses api.geekdo.com (no auth required)
- Includes rate limiting (0.15s between calls)

### API Response Format
```json
{
  "id": 123456,
  "versions": [
    {
      "id": 999,
      "name": "Standard Edition (Publisher Name)",
      "year": 2023,
      "l": 29.5,
      "w": 29.5,
      "h": 7.5
    },
    ...
  ]
}
```

## Example: Catan

When you click to edit Catan (#13), the modal will show:
- **Original German Edition (1995)** - 30 × 30 × 9 cm
- **US Edition (1995)** - 29.5 × 29.5 × 7.5 cm  
- **Newer Revision (2020)** - 29.5 × 29.5 × 7.5 cm

Pick the one that matches your physical copy!

## Requirements

- Server must be running: `python3 server.py`
- OR use CORS proxy fallback (slower but works)
- BGG API access (public, no auth needed)
