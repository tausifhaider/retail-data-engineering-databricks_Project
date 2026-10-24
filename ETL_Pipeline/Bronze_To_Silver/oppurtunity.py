from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(
    name="retail_q.retail_silver.opportunity",
    comment="Silver-layer opportunity data from Salesforce bronze"
)
@dp.expect_or_drop("non-null name", "name IS NOT NULL")
def opportunity_clean():
    source_df = spark.read.table("retail_q.default.salesforce_bronze")
    
    return (
        source_df
        .filter(F.col("opportunity_name").isNotNull())
        .select(
            F.col("opportunity_name").alias("name"),
            F.col("stage").alias("stage_name"),
            F.col("amount"),
            F.col("close_date"),
            F.col("lead_source"),
            F.col("type").alias("opportunity_type"),
            F.col("description")
        )
    )
