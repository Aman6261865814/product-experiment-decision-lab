-- Run once in a new empty database. Never run against production without review.
CREATE TABLE device_segments (
    variant VARCHAR(255) NULL,
    device VARCHAR(255) NULL,
    users BIGINT NULL,
    conversions BIGINT NULL
);

CREATE TABLE fact_experiment (
    user_id BIGINT NOT NULL,
    variant VARCHAR(255) NULL,
    region VARCHAR(255) NULL,
    device VARCHAR(255) NULL,
    assigned_date DATE NULL,
    converted BIGINT NULL,
    crashed BIGINT NULL,
    revenue_usd DECIMAL(19,4) NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE variant_metrics (
    variant VARCHAR(255) NULL,
    users BIGINT NULL,
    conversions BIGINT NULL,
    crashes BIGINT NULL,
    revenue_usd DECIMAL(19,4) NULL,
    conversion_rate FLOAT NULL,
    crash_rate FLOAT NULL
);