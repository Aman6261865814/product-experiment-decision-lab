-- SQLite benchmark: capture EXPLAIN QUERY PLAN before and after the index.
EXPLAIN QUERY PLAN SELECT SUM(converted) FROM fact_experiment
WHERE assigned_date>='2026-05-01' AND assigned_date<'2026-06-01';
CREATE INDEX IF NOT EXISTS ix_fact_experiment_date ON fact_experiment(assigned_date);
EXPLAIN QUERY PLAN SELECT SUM(converted) FROM fact_experiment
WHERE assigned_date>='2026-05-01' AND assigned_date<'2026-06-01';
-- SQL Server: actual plan + SET STATISTICS IO,TIME ON; CREATE INDEX without IF NOT EXISTS.
-- MySQL 8.0.18+: EXPLAIN ANALYZE; CREATE INDEX without IF NOT EXISTS.
-- Never infer production speedups from this small local dataset.
