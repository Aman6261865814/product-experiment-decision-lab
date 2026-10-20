-- Requires imported processed tables. SQL Server 2019+ / MySQL 8.0+.
WITH arm AS (
 SELECT variant, COUNT(*) AS users, SUM(converted) AS conversions,
 SUM(crashed) AS crashes, SUM(revenue_usd) AS revenue_usd
 FROM fact_experiment GROUP BY variant
)
SELECT *, conversions * 1.0/NULLIF(users,0) AS conversion_rate,
 crashes * 1.0/NULLIF(users,0) AS crash_rate,
 users * 1.0 / SUM(users) OVER () AS allocation_share
FROM arm ORDER BY variant;
