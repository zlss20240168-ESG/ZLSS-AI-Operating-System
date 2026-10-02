# SEO Website Optimizer — Audit Core V1

Temporary version-controlled home for the SEO Website Optimization project until PG10 creates the dedicated repository.

## Scope
This core is intentionally separated from crawler/renderer code. It implements deterministic scoring/version logic only:
- URL normalization
- Website/page fingerprinting
- volatile-data exclusion
- category scoring
- N/A reallocation within category
- Critical Caps
- score bands
- result identity by Website Fingerprint + Engine Version
- material-change classification

## Current validation
- Regression cases: 36
- Local execution result: 36/36 passed
- Audit Engine Core: 1.0.0-core
- Fingerprint Algorithm: 1.0.0

## Project governance
Source requirements are maintained in the project's Google Drive:
- PG04 100-Point Audit Scoring Specification
- PG05 Website Fingerprint & Result Versioning Specification
- PG06 V&V Regression Test Matrix
- Requirements Baseline & Decision Log

This folder is a temporary repository location. PG10 must migrate it to a dedicated project repository before production release.
