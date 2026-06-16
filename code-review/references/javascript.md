# JavaScript Review Checklist

## Script Loading & Dependencies

- Script loaded at end of body or with defer attribute?
- No render-blocking scripts in head?
- External CDN scripts use crossorigin and integrity attributes?
- Libraries justified over native APIs?

## DOM Manipulation

- DOM queries cached (not re-queried on every interaction)?
- Event listeners use passive mode for scroll/touch?
- Event delegation used instead of many similar listeners?
- DOM content not gated on animation-end?

## Async & Data Flow

- Async operations handle error states (catch or try/catch)?
- Race conditions avoided?
- Data validation on user input before processing?
- Form submissions prevent default?

## State & Mutation

- State mutations predictable (no unexpected side effects)?
- No direct manipulation of another module state?
- Timers/intervals cleaned up when no longer needed?

## Code Quality

- Consistent formatting (semicolons, quotes, spacing)?
- Descriptive variable and function names?
- Functions with single responsibility?
- No commented-out code blocks?
- Console.log/debug statements removed from production code?

## Browser Compatibility

- Standard APIs used (avoid vendor prefixes except backdrop-filter)?
- IntersectionObserver has fallback for unsupported browsers?
