from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.table(
    name="product_catalog",
    comment="Silver-layer product catalog with standardized fields and data quality checks",
)
@dp.expect_or_fail("valid_product_id", "product_id IS NOT NULL")
@dp.expect_or_drop("valid_unit_price", "unit_price >= 0")
@dp.expect("non_null_product_name", "product_name IS NOT NULL")
@dp.expect("non_null_category", "category IS NOT NULL")
def product_catalog_silver():
    return (
        spark.readStream
        .option("skipChangeCommits", "true")
        .table("retail_q.postgres_bronze.product_catalog")
        .filter(F.col("__END_AT").isNull())
        .withColumn("product_id", F.upper(F.trim(F.col("product_id"))))
        .withColumn("product_name", F.trim(F.col("product_name")))
        .withColumn("category", F.initcap(F.trim(F.col("category"))))
        .withColumn("subcategory", F.initcap(F.trim(F.col("subcategory"))))
        .withColumn("brand", F.trim(F.col("brand")))
        .withColumn("unit_price", F.col("unit_price").cast("decimal(10,2)"))
        .withColumn("supplier_name", F.trim(F.col("supplier_name")))
        .withColumn("is_active", F.col("is_active").cast("boolean"))
        .drop("__START_AT", "__END_AT")
    )
