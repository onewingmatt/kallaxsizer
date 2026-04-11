## 2026-03-29 - [Keyboard Accessibility for Custom Components]
**Learning:** Interactive elements rendered as 'div' tags (like the Kallax cubes) must be made keyboard-accessible using 'role="button"', 'tabindex="0"', and keydown listeners for 'Enter' and 'Space'. Without these, keyboard-only users cannot interact with key features of the application.
**Action:** Always check for custom interactive elements and apply standard ARIA roles and keyboard listeners. Use 'focus-visible' CSS to provide clear visual feedback.

## 2025-05-14 - [Standardizing Keyboard Accessibility for Monolithic UI]
**Learning:** In a monolithic HTML file with custom-rendered components (divs, table cells), consistent focus indicators via ':focus-visible' and standardized keydown handlers for 'Enter'/'Space' are essential for parity with native interactive elements. Screen readers also require 'aria-expanded' states for collapsible sections to maintain situational awareness.
**Action:** Apply global ':focus-visible' rules for '[role="button"]' and implement reusable 'onkeydown' listeners that match 'onclick' functionality for all custom interactive elements. Ensure state-changing interactions update their corresponding ARIA attributes immediately.

## 2026-04-11 - [Accessible Data Tables and Sorting]
**Learning:** For sortable tables, it is not enough to just add `onclick` listeners to headers. They must have `role="button"`, `tabindex="0"`, and `keydown` support for keyboard users. Additionally, `aria-sort` must be used to communicate the current sorting state (ascending/descending/none) to screen readers, and decorative sort arrows should be hidden using `aria-hidden="true"`.
**Action:** When implementing sortable headers, ensure all accessibility attributes are applied and synchronized with the JavaScript rendering logic.
