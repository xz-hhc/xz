---
name: code-review
description: "Comprehensive code review and analysis for any project. Use when the user asks to review, audit, inspect, analyze, or evaluate their codebase. Covers architecture, structure, frontend, CSS, JavaScript, HTML, performance, security, accessibility, and code quality. Also use for code review, code audit, inspect code, check code, analyze project, find issues, or when the user wants a systematic breakdown of their code."
---

# Code Review

Perform a comprehensive, structured code review of any project. Read every significant file, then produce a findings-led report organized by severity.

## Workflow

### 1. Discover the project surface

List all files recursively. Note:
- Total file count, total lines of code
- Project type (static site, SPA, Node app, Python project, etc.)
- Build/config files (package.json, requirements.txt, Dockerfile, etc.)
- Any README, docs, or design doc

### 2. Read every significant file

Read non-binary files that are part of the shipped code or its configuration. Skip:
- .git/, node_modules/, __pycache__/, and similar generated directories
- Lock files (package-lock.json, yarn.lock, poetry.lock)
- Binary assets (images, fonts, audio)

### 3. Run the five-dimension review

For each dimension, load the corresponding reference file for the full checklist.

| Dimension | Reference file | Primary target |
|-----------|---------------|----------------|
| Architecture & Structure | references/architecture.md | File layout, components, DRY, conventions |
| CSS & Styling | references/frontend.md | CSS files, inline styles, design tokens |
| JavaScript & Logic | references/javascript.md | JS/TS files, event handling, data flow |
| HTML & Semantics | references/frontend.md | HTML structure, meta tags, a11y |
| Security & Performance | references/architecture.md | Config, resource loading, XSS/CSRF |

### 4. Prioritize findings

Order findings by severity:
- P0 ！ Bug or blocker: causes incorrect behavior, breaks on edge cases
- P1 ！ Regression risk: will break under specific conditions
- P2 ！ Design or maintainability: makes code harder to work with
- P3 ！ Minor / style: nitpicks without functional impact

Group findings by file path with line numbers, severity, impact, and fix recommendation.

### 5. Produce the output

Follow the template at references/output-template.md. Structure:
1. Executive summary ！ project overview, major risks
2. Findings table ！ grouped by severity
3. Architecture & structure
4. Specific dimension sections
5. Open questions
6. Summary

### 6. If no issues found

State "No issues found" then list residual risk and a recommended follow-up.

## Reference files

- references/architecture.md ！ architecture checklist
- references/frontend.md ！ CSS/HTML/component checklist
- references/javascript.md ！ JS/TS checklist
- references/output-template.md ！ report template

## Notes

- Read files with cat, rg, or the native file tool
- Parallelize file reads with multi_tool_use.parallel
- Do not skip the project-surface scan even for targeted reviews