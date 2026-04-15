## 2026-03-29 - [Keyboard Accessibility for Custom Components]
**Learning:** Interactive elements rendered as 'div' tags (like the Kallax cubes) must be made keyboard-accessible using 'role="button"', 'tabindex="0"', and keydown listeners for 'Enter' and 'Space'. Without these, keyboard-only users cannot interact with key features of the application.
**Action:** Always check for custom interactive elements and apply standard ARIA roles and keyboard listeners. Use 'focus-visible' CSS to provide clear visual feedback.

## 2025-05-14 - [Standardizing Keyboard Accessibility for Monolithic UI]
**Learning:** In a monolithic HTML file with custom-rendered components (divs, table cells), consistent focus indicators via ':focus-visible' and standardized keydown handlers for 'Enter'/'Space' are essential for parity with native interactive elements. Screen readers also require 'aria-expanded' states for collapsible sections to maintain situational awareness.
**Action:** Apply global ':focus-visible' rules for '[role="button"]' and implement reusable 'onkeydown' listeners that match 'onclick' functionality for all custom interactive elements. Ensure state-changing interactions update their corresponding ARIA attributes immediately.

## 2025-05-15 - [Improving State Feedback for Theme Toggles]
**Learning:** A theme toggle button should not only change the appearance of the page but also provide clear visual and semantic feedback about the *target* state. Using a helper function to synchronize the icon (e.g., ☀️ in dark mode), ARIA label, and title ensures a consistent experience for both sighted and screen-reader users, including on initial page load.
**Action:** When implementing theme toggles, ensure the UI (icon/label) reflects the *action* (e.g., "Switch to Light Mode") or the *target* theme, and initialize this state correctly from localStorage or system preferences.
