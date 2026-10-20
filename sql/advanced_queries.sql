-- Advanced, portable SQL (SQLite, SQL Server, MySQL 8); ranked regional drivers.
WITH regional AS (
 SELECT f.region AS region, f.user_id, SUM(f.converted) AS metric_total
 FROM fact_experiment f 
 GROUP BY f.region,f.user_id
), ranked AS (
 SELECT *, DENSE_RANK() OVER (PARTITION BY region ORDER BY metric_total DESC) AS regional_rank
 FROM regional
)
SELECT * FROM ranked WHERE regional_rank<=5 ORDER BY region,regional_rank;

-- Correlated subquery: observations above their calendar-date average.
SELECT f.user_id,f.assigned_date,f.converted
FROM fact_experiment f
WHERE f.converted > (SELECT AVG(g.converted*1.0) FROM fact_experiment g WHERE g.assigned_date=f.assigned_date);
