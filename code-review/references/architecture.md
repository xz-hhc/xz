# Architecture & Structure Checklist

## File Layout & Project Structure

- Is there a README or project-level documentation?
- Does the directory structure follow framework conventions?
- Are config/asset/source files separated into clear directories?
- Are there unnecessary duplicate files or dead code?
- Is the entry point clearly identifiable?

## Components & Separation of Concerns

- Are presentation and logic reasonably separated?
- Is there excessive inline styling in markup?
- Are there repeated HTML/CSS patterns that could be componentized?
- Are third-party dependencies justified?
- Is error handling consistent?

## DRY & Conventions

- Is the same code written more than once where a helper would serve?
- Are naming conventions consistent across files?
- Are there hardcoded values that should be config?
- Is error handling consistent across the codebase?

## Security & Performance

- Are there any hardcoded secrets, API keys, or credentials?
- Are external resources loaded over HTTPS?
- Are forms vulnerable to CSRF/XSS?
- Are there unnecessary layout-triggering animations?
- Are large libraries loaded when smaller alternatives would suffice?

## Build & Config

- Is there a .gitignore and does it cover generated files?
- Are environment variables used for environment-specific values?
- Is the dependency tree clean?
