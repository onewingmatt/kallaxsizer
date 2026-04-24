## 2026-03-29 - [Keyboard Accessibility for Custom Components]
**Learning:** Interactive elements rendered as 'div' tags (like the Kallax cubes) must be made keyboard-accessible using 'role="button"', 'tabindex="0"', and keydown listeners for 'Enter' and 'Space'. Without these, keyboard-only users cannot interact with key features of the application.
**Action:** Always check for custom interactive elements and apply standard ARIA roles and keyboard listeners. Use 'focus-visible' CSS to provide clear visual feedback.

## 2025-05-14 - [Standardizing Keyboard Accessibility for Monolithic UI]
**Learning:** In a monolithic HTML file with custom-rendered components (divs, table cells), consistent focus indicators via ':focus-visible' and standardized keydown handlers for 'Enter'/'Space' are essential for parity with native interactive elements. Screen readers also require 'aria-expanded' states for collapsible sections to maintain situational awareness.
**Action:** Apply global ':focus-visible' rules for '[role="button"]' and implement reusable 'onkeydown' listeners that match 'onclick' functionality for all custom interactive elements. Ensure state-changing interactions update their corresponding ARIA attributes immediately.

## 2025-05-15 - [Communicating Async States in Monolithic Single-Page Apps]
**Learning:** For long-running async operations (like scraping), visual indicators (spinners/text) are insufficient for screen readers. Using 'aria-busy="true"' on the triggering button and 'aria-live="polite"' on status areas ensures that users of assistive technology are aware of the ongoing process and receive progress updates.
**Action:** Always pair visual loading states with 'aria-busy' and 'aria-live' regions. Ensure 'aria-busy' is removed once the operation concludes in a 'finally' block.
