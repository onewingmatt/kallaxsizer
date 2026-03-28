# Palette's UX Journal

## 2026-03-28 - [Interactive Layout Accessibility]
**Learning:** In highly visual, grid-based layouts (like the Kallax cube preview), decorative 'div' elements that trigger detail views must be explicitly converted to accessible buttons.
**Action:** Always apply 'role="button"', 'tabindex="0"', and dual event listeners (click + keydown for Enter/Space) to non-semantic interactive elements. Ensure 'aria-label' includes the specific item index and a summary of its contents (e.g., "Cube 1 contains 2 games: [Names]").
