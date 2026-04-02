## 2026-03-29 - [Keyboard Accessibility for Custom Components]
**Learning:** Interactive elements rendered as 'div' tags (like the Kallax cubes) must be made keyboard-accessible using 'role="button"', 'tabindex="0"', and keydown listeners for 'Enter' and 'Space'. Without these, keyboard-only users cannot interact with key features of the application.
**Action:** Always check for custom interactive elements and apply standard ARIA roles and keyboard listeners. Use 'focus-visible' CSS to provide clear visual feedback.

## 2025-05-14 - [Standardizing Keyboard Accessibility for Monolithic UI]
**Learning:** In a monolithic HTML file with custom-rendered components (divs, table cells), consistent focus indicators via ':focus-visible' and standardized keydown handlers for 'Enter'/'Space' are essential for parity with native interactive elements. Screen readers also require 'aria-expanded' states for collapsible sections to maintain situational awareness.
**Action:** Apply global ':focus-visible' rules for '[role="button"]' and implement reusable 'onkeydown' listeners that match 'onclick' functionality for all custom interactive elements. Ensure state-changing interactions update their corresponding ARIA attributes immediately.

## 2025-05-15 - [Unified Feedback and Loading States]
**Learning:** In a single-page board game utility with long-running async fetches (like BGG API requests), providing immediate visual feedback via button loading states (text change + disabling) and using a unified feedback element for both errors and successes improves perceived performance and user confidence. Ensuring these states are cleared in a 'finally' block prevents UI deadlocks.
**Action:** Always implement a loading state for primary action buttons during async operations. Enhance shared notification components (like 'showError') to handle success states with distinct visual cues (e.g., green theme/emojis) to celebrate user completion.
