## 2026-03-29 - [Keyboard Accessibility for Custom Components]
**Learning:** Interactive elements rendered as 'div' tags (like the Kallax cubes) must be made keyboard-accessible using 'role="button"', 'tabindex="0"', and keydown listeners for 'Enter' and 'Space'. Without these, keyboard-only users cannot interact with key features of the application.
**Action:** Always check for custom interactive elements and apply standard ARIA roles and keyboard listeners. Use 'focus-visible' CSS to provide clear visual feedback.

## 2025-05-14 - [Standardizing Keyboard Accessibility for Monolithic UI]
**Learning:** In a monolithic HTML file with custom-rendered components (divs, table cells), consistent focus indicators via ':focus-visible' and standardized keydown handlers for 'Enter'/'Space' are essential for parity with native interactive elements. Screen readers also require 'aria-expanded' states for collapsible sections to maintain situational awareness.
**Action:** Apply global ':focus-visible' rules for '[role="button"]' and implement reusable 'onkeydown' listeners that match 'onclick' functionality for all custom interactive elements. Ensure state-changing interactions update their corresponding ARIA attributes immediately.

## 2025-05-15 - [Accessible Table Sorting]
**Learning:** Sortable table headers must be explicitly identified as interactive using 'role="button"' and 'tabindex="0"'. Assistive technologies require the 'aria-sort' attribute ('ascending', 'descending', or 'none') to communicate state changes that are otherwise only visual. Decorative sort indicators (like arrows) should be hidden from screen readers using 'aria-hidden="true"' when 'aria-sort' is used.
**Action:** When implementing table sorting, ensure headers are keyboard-accessible and dynamically update 'aria-sort' and 'aria-hidden' attributes during the render cycle.
