## 2026-03-29 - [Keyboard Accessibility for Custom Components]
**Learning:** Interactive elements rendered as 'div' tags (like the Kallax cubes) must be made keyboard-accessible using 'role="button"', 'tabindex="0"', and keydown listeners for 'Enter' and 'Space'. Without these, keyboard-only users cannot interact with key features of the application.
**Action:** Always check for custom interactive elements and apply standard ARIA roles and keyboard listeners. Use 'focus-visible' CSS to provide clear visual feedback.

## 2025-05-14 - [Standardizing Keyboard Accessibility for Monolithic UI]
**Learning:** In a monolithic HTML file with custom-rendered components (divs, table cells), consistent focus indicators via ':focus-visible' and standardized keydown handlers for 'Enter'/'Space' are essential for parity with native interactive elements. Screen readers also require 'aria-expanded' states for collapsible sections to maintain situational awareness.
**Action:** Apply global ':focus-visible' rules for '[role="button"]' and implement reusable 'onkeydown' listeners that match 'onclick' functionality for all custom interactive elements. Ensure state-changing interactions update their corresponding ARIA attributes immediately.

## 2024-05-21 - [Contextual ARIA Labels for Dynamic Lists]
**Learning:** When dynamically generating input rows for a list of items (e.g., Batch Edit rows), each input must have a descriptive `aria-label` that incorporates the item's specific context (like the game name). This ensures that screen reader users can distinguish between similar inputs (e.g., "Length") across different items in the list.
**Action:** Always map item-specific data into `aria-label` attributes for inputs rendered within loops or template literals. Ensure any special characters (like double quotes) in the item data are properly escaped to prevent malformed HTML.
