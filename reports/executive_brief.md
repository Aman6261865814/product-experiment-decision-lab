# Product Experiment Decision Lab

SYNTHETIC PORTFOLIO CASE STUDY — not actual company results.

## Decision: SHIP
Conversion change is 1.78 percentage points (95% CI 1.01 to 2.54). Assignment SRM p=0.2987. Crash-rate one-sided upper bound is 0.43 pp; guardrail limit is +0.50 pp.

## Prespecified policy
Analyze once after all users have 7 days of follow-up; assignment May 1–14, extraction May 22, 2026. Intent-to-treat unit is user. SRM threshold .001. Ship only if conversion CI lower bound exceeds +0.50 pp AND crash upper bound is below +0.50 pp. Planned MDE +1.50 pp at 80% power requires approximately 7,368 users/arm. No optional stopping.

## Limits
Revenue bootstrap and device slices are exploratory, not additional launch criteria; no segment winner claims. Synthetic independent users cannot establish real customer lift. Missing outcomes are absent by construction; production must monitor missingness and exposure logging. Normal approximations require sufficient successes/failures; use exact methods for sparse experiments.
