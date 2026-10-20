-- Dates are an inclusive start and exclusive end; no wrapping indexed column in a function.
CREATE OR ALTER PROCEDURE dbo.usp_RegionalMetrics
    @FromDate date, @ToDate date
AS
BEGIN
    SET NOCOUNT ON;
    IF @ToDate <= @FromDate THROW 50001, 'End date must follow start', 1;
    SELECT f.region AS region, COUNT(*) AS observations, SUM(f.converted) AS metric_total
    FROM fact_experiment f 
    WHERE f.assigned_date >= @FromDate AND f.assigned_date < @ToDate
    GROUP BY f.region;
END;
GO
-- Example: EXEC dbo.usp_RegionalMetrics '2026-05-01','2026-06-01';
