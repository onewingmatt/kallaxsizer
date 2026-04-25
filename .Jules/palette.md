## 2026-03-29 - [Keyboard Accessibility for Custom Components]
**Learning:** Interactive elements rendered as 'div' tags (like the Kallax cubes) must be made keyboard-accessible using 'role="button"', 'tabindex="0"', and keydown listeners for 'Enter' and 'Space'. Without these, keyboard-only users cannot interact with key features of the application.
**Action:** Always check for custom interactive elements and apply standard ARIA roles and keyboard listeners. Use 'focus-visible' CSS to provide clear visual feedback.

## 2025-05-14 - [Standardizing Keyboard Accessibility for Monolithic UI]
**Learning:** In a monolithic HTML file with custom-rendered components (divs, table cells), consistent focus indicators via ':focus-visible' and standardized keydown handlers for 'Enter'/'Space' are essential for parity with native interactive elements. Screen readers also require 'aria-expanded' states for collapsible sections to maintain situational awareness.
**Action:** Apply global ':focus-visible' rules for '[role="button"]' and implement reusable 'onkeydown' listeners that match 'onclick' functionality for all custom interactive elements. Ensure state-changing interactions update their corresponding ARIA attributes immediately.

## 2026-04-25 - [Accessible Table Sorting in Monolithic UI]
**Learning:** For sortable table headers, adding 'tabindex="0"' and 'keydown' listeners directly to the '<th>' elements is preferred over wrapping content in a 'button'. This preserves the semantic 'columnheader' role while enabling keyboard interaction. Accompanying 'aria-sort' attributes must be updated dynamically to reflect the current sort state.
**Action:** Use 'tabindex="0"' on '<th>' and implement a shared sorting handler for both 'click' and 'keydown' events. Ensure 'aria-sort' is synchronized in the rendering logic.
