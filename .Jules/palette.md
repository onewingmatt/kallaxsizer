## 2026-03-29 - [Keyboard Accessibility for Custom Components]
**Learning:** Interactive elements rendered as 'div' tags (like the Kallax cubes) must be made keyboard-accessible using 'role="button"', 'tabindex="0"', and keydown listeners for 'Enter' and 'Space'. Without these, keyboard-only users cannot interact with key features of the application.
**Action:** Always check for custom interactive elements and apply standard ARIA roles and keyboard listeners. Use 'focus-visible' CSS to provide clear visual feedback.

## 2025-05-14 - [Standardizing Keyboard Accessibility for Monolithic UI]
**Learning:** In a monolithic HTML file with custom-rendered components (divs, table cells), consistent focus indicators via ':focus-visible' and standardized keydown handlers for 'Enter'/'Space' are essential for parity with native interactive elements. Screen readers also require 'aria-expanded' states for collapsible sections to maintain situational awareness.
**Action:** Apply global ':focus-visible' rules for '[role="button"]' and implement reusable 'onkeydown' listeners that match 'onclick' functionality for all custom interactive elements. Ensure state-changing interactions update their corresponding ARIA attributes immediately.

## 2026-04-21 - [Accessible Data Tables & Form Submission]
**Learning:** For monolithic UI data tables, adding 'tabindex="0"' and 'aria-sort' to column headers provides essential accessibility. In custom form layouts, explicitly adding 'Enter' key listeners to text inputs ensures parity with native form submission behavior, which users expect by default.
**Action:** Always implement 'aria-sort' and 'tabindex="0"' for sortable headers. Ensure all main text inputs have 'keydown' listeners for 'Enter' that trigger their primary action button.
