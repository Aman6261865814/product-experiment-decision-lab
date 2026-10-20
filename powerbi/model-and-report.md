# Power BI implementation: Product Experiment Decision Lab

Status: import-ready CSV, Power Query, DAX, theme and RLS design supplied. No .pbix is included; Desktop/Service validation has not been performed.

1. Open Power BI Desktop, define `DataFolder` as an absolute path to data/processed.
2. Create fnLoadCSV from the supplied M function. Create `fact_experiment` using fact_query.pq. Import remaining needed dimensions using Get Data > Text/CSV. Set IDs to whole number and money to fixed decimal.
3. Create `dim_date = CALENDAR(MIN(fact_experiment[assigned_date]), MAX(fact_experiment[assigned_date]))`, mark Date as date table; connect dim_date[Date] 1:* to fact_experiment[assigned_date], single-direction.
4. Create dim_region = DISTINCT(fact_experiment[region]); connect dim_region[region] 1:* to fact_experiment[region], single-direction.
5. Add each measure separately from measures.dax. Import theme.json. Currency USD, rate measures 0.0%, pp measures 0.00.
6. Import security.csv separately, replace sample UPNs, keep it disconnected. In Manage roles add supplied rls.dax filter. Unknown users receive no rows. Never use a permissive default region.
7. Test View as with one UPN per region, an unknown user, and a user assigned two regions. Compare regional totals with CSV/Python. Test again as a **Viewer** in Service; RLS does not restrict workspace Admins, Members or Contributors.
8. Publish only after local totals match reports/metrics.json. Set refresh credentials/gateway for local file sources or replace with governed database sources; a local path will not auto-refresh in Service by itself.

## Three-page report specification

| Page | Visuals | Interaction / acceptance |
|---|---|---|
| Executive overview | KPI cards; primary trend or comparison; concise decision annotation | Date and region slicers; labels show units and synthetic source |
| Drivers | Variant conversion and crash-rate comparison; device slice | Drill-through to business key; tooltips explain denominators |
| Data quality | Duplicate count, grain check, freshness and null coverage | Link to validation evidence and metric definitions |

## Semantic safeguards

Inferential CIs and launch decisions apply to the full prespecified experiment only. Do not place fixed global decision/CI cards beside filterable regional slices. Keep global decision page in an analyst-only report; regional RLS report contains descriptive measures only. Do not load unfiltered variant_metrics/device_segments aggregate tables into the secured model.

## References

- https://learn.microsoft.com/en-us/power-bi/guidance/star-schema
- https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls
