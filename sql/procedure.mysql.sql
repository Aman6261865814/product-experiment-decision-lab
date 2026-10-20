DELIMITER //
CREATE PROCEDURE RegionalMetrics(IN p_from DATE, IN p_to DATE)
BEGIN
    IF p_to <= p_from THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='End date must follow start'; END IF;
    SELECT f.region AS region, COUNT(*) AS observations, SUM(f.converted) AS metric_total
    FROM fact_experiment f 
    WHERE f.assigned_date >= p_from AND f.assigned_date < p_to
    GROUP BY f.region;
END //
DELIMITER ;
