# ──────────────────────────────────────────────
# INPUT: Adjust these two dates to control the
#         date range populated in the calendar table
# ──────────────────────────────────────────────
start_date = "2025-01-01"
end_date   = "2028-12-31"

# Drop and recreate the calendar table using SQL
spark.sql(f"""
CREATE OR REPLACE TABLE retail_q.retail_gold.calendar AS
SELECT
    date                                                               AS date,
    YEAR(date)                                                         AS year,
    QUARTER(date)                                                      AS quarter,
    MONTH(date)                                                        AS month,
    DATE_FORMAT(date, 'MMMM')                                          AS month_name,
    DATE_FORMAT(date, 'MMM')                                           AS month_abbr,
    WEEKOFYEAR(date)                                                   AS week_of_year,
    CEIL(DAYOFMONTH(date) / 7)                                         AS week_of_month,
    DAYOFYEAR(date)                                                    AS day_of_year,
    DAYOFMONTH(date)                                                   AS day_of_month,
    DAYOFWEEK(date)                                                    AS day_of_week,
    DATE_FORMAT(date, 'EEEE')                                          AS day_name,
    DATE_FORMAT(date, 'EEE')                                           AS day_abbr,
    DAYOFWEEK(date) IN (1, 7)                                          AS is_weekend,
    date = DATE_TRUNC('month', date)                                   AS is_month_start,
    date = LAST_DAY(date)                                              AS is_month_end,
    date = DATE_TRUNC('quarter', date)                                 AS is_quarter_start,
    date = LAST_DAY(DATE_TRUNC('quarter', date) + INTERVAL '2' MONTH) AS is_quarter_end,
    date = DATE_TRUNC('year', date)                                    AS is_year_start,
    date = LAST_DAY(DATE_TRUNC('year', date) + INTERVAL '11' MONTH)    AS is_year_end
FROM (
    SELECT explode(sequence(
        to_date('{start_date}'),
        to_date('{end_date}'),
        INTERVAL 1 DAY
    )) AS date
)
""")

row_count = spark.sql("SELECT COUNT(*) AS cnt FROM retail_q.retail_gold.calendar").collect()[0]["cnt"]

display(spark.sql("SELECT * FROM retail_q.retail_gold.calendar ORDER BY date LIMIT 15"))
print(f"Calendar table created with {row_count} rows from {start_date} to {end_date}.")
