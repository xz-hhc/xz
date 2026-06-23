# Frontend Review Checklist

## HTML Structure

- DOCTYPE html and html lang attribute on every page?
- meta charset and meta viewport present?
- Semantic HTML (nav, main, section, article, footer) used?
- Heading hierarchy correct (h1 > h2 > h3)?
- Alt text on all images?
- Form inputs have associated label elements?

## Meta & Social

- Unique title and meta description per page?
- Open Graph tags (og:title, og:description, og:image) present?
- Favicon linked?
- Canonical URL specified where needed?

## CSS Quality

- CSS custom properties used for repeated values?
- Unused CSS rules that could be pruned?
- important overrides used excessively?
- z-index system structured (no 999/9999 values)?
- Fixed widths that should be fluid (clamp(), min/max)?
- Animations GPU-accelerated (transform/opacity only)?
- prefers-reduced-motion correctly suppresses motion?
- Consistent color space across files (OKLCH, HSL, or hex)?

## Typography & Contrast

- Body text contrast >= 4.5:1 against background?
- Line length capped at 65-75ch for readability?
- Font stacks include fallbacks?
- Heading letter-spacing >= -0.04em?
- Text does not overflow containers on any viewport?

## Responsive Design

- Layout works at 375px, 768px, 1024px, 1440px+?
- Touch targets >= 44px on mobile?
- No horizontal scroll on narrowest breakpoint?
- Navigation collapses to hamburger menu on mobile?

## Images & Assets

- Images have width/height or aspect-ratio to prevent layout shift?
- SVG preferred over raster where appropriate?
- Fallback for broken images?
