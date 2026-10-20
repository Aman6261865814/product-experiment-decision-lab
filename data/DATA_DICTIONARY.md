# Data dictionary and metric contracts

All source data is synthetic, generated locally; no real organization or customer is represented.

## Grain and key
fact_experiment: one assigned user, unique user_id. Assignment is 50/50 independent Bernoulli, not an exact fixed-size split. region and device are assigned pre-treatment in this simulation. assigned_date: May 1–14, 2026; outcomes fully mature by May 22.

## Core fields
converted: any conversion within seven days of assignment (0/1). crashed: any crash within seven days (0/1). revenue_usd: seven-day user revenue, zero for nonconverters. variant: control or treatment. No exposure-based exclusion occurs; all assigned users are analyzed.

## Contracts
SRM chi-square evaluates counts against 50/50 expectation. Conversion difference CI uses unpooled normal standard error; two-sided p value uses pooled null standard error. Crash noninferiority uses a one-sided 95% upper bound. Guardrail and practical effect thresholds are set in the generator/analysis specification before reading outputs. Revenue is exploratory and uses a user-level bootstrap. Simulation probabilities deliberately inject a treatment effect; this does not predict real lift.

Additional table/column types, nulls and uniqueness are in reports/data_profile.csv.
