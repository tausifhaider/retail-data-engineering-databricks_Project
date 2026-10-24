# Auto Loader: Read CSV files from source volume and write to Delta table
source_path = "/Volumes/retail_q/volumes/blob_source/transactions_source/"
checkpoint_path = "/Volumes/retail_q/volumes/blob_source/_checkpoints/transactions/"
target_table = "retail_q.blob_bronze.transactions"

# Ensure the target schema exists
spark.sql("CREATE SCHEMA IF NOT EXISTS retail_q.blob_bronze")

# Define the expected schema explicitly (avoids issues with headerless files)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("customer_name", StringType(), True),
    StructField("product", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", IntegerType(), True),
    StructField("remarks", StringType(), True),
    StructField("_corrupt_record", StringType(), True),
])

# Configure Auto Loader to incrementally read CSV files
raw_df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", checkpoint_path)
    .option("header", "true")
    .option("sep", ",")
    .option("escape", "\"")
    .option("multiLine", "true")
    .option("mode", "PERMISSIVE")
    .option("columnNameOfCorruptRecord", "_corrupt_record")
    .schema(schema)
    .load(source_path)
)

# Write to the Delta target table using AvailableNow trigger (batch-like processing)
(raw_df.writeStream
    .format("delta")
    .option("checkpointLocation", checkpoint_path)
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .toTable(target_table)
)

# Verify the ingested data
print("=== Row count ===")
spark.sql("SELECT COUNT(*) AS total_rows FROM retail_q.blob_bronze.transactions").show()

print("=== Sample data ===")
display(spark.sql("SELECT * FROM retail_q.blob_bronze.transactions LIMIT 10"))

print("=== Corrupt records (if any) ===")
spark.sql("SELECT COUNT(*) AS corrupt_rows FROM retail_q.blob_bronze.transactions WHERE _corrupt_record IS NOT NULL").show()

print(f"Auto Loader pipeline complete. Data written to {target_table}")
