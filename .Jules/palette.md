## 2026-03-29 - [Keyboard Accessibility for Custom Components]
**Learning:** Interactive elements rendered as 'div' tags (like the Kallax cubes) must be made keyboard-accessible using 'role="button"', 'tabindex="0"', and keydown listeners for 'Enter' and 'Space'. Without these, keyboard-only users cannot interact with key features of the application.
**Action:** Always check for custom interactive elements and apply standard ARIA roles and keyboard listeners. Use 'focus-visible' CSS to provide clear visual feedback.

## 2025-05-14 - [Standardizing Keyboard Accessibility for Monolithic UI]
**Learning:** In a monolithic HTML file with custom-rendered components (divs, table cells), consistent focus indicators via ':focus-visible' and standardized keydown handlers for 'Enter'/'Space' are essential for parity with native interactive elements. Screen readers also require 'aria-expanded' states for collapsible sections to maintain situational awareness.
**Action:** Apply global ':focus-visible' rules for '[role="button"]' and implement reusable 'onkeydown' listeners that match 'onclick' functionality for all custom interactive elements. Ensure state-changing interactions update their corresponding ARIA attributes immediately.

## 2025-05-15 - [Accessible Data Tables & Implicit Submission]
**Learning:** Sortable table headers should use `tabindex="0"` and `aria-sort` to be accessible. Explicitly handling 'Enter' and 'Space' for sorting provides parity with button behavior. For search/login forms, a keydown listener for 'Enter' on input fields to trigger the primary action button is a critical "invisible" UX improvement that users expect.
**Action:** Always implement `aria-sort` and keyboard listeners for custom sortable headers. Ensure primary inputs support 'Enter' to submit.
