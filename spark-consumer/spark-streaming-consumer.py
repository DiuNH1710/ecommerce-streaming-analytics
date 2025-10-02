from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, count
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
from mysql_storage.insert_data import  *

spark = SparkSession.builder\
      .appName("May2022_CDC_Processing")\
      .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.4")\
      .getOrCreate()
      
spark.sparkContext.setLogLevel("WARN")

may_2022_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("sku", StringType(), True),
    StructField("style_id", StringType(), True),
    StructField("catalog", StringType(), True),
    StructField("category", StringType(), True),
    StructField("weight", DoubleType(), True),
    StructField("tp", DoubleType(), True),
    StructField("mrp_old", DoubleType(), True),
    StructField("final_mrp_old", DoubleType(), True),
    StructField("ajio_mrp", DoubleType(), True),
    StructField("amazon_mrp", DoubleType(), True),
    StructField("amazon_fba_mrp", DoubleType(), True),
    StructField("flipkart_mrp", DoubleType(), True),
    StructField("limeroad_mrp", DoubleType(), True),
    StructField("myntra_mrp", DoubleType(), True),
    StructField("paytm_mrp", DoubleType(), True),
    StructField("snapdeal_mrp", DoubleType(), True),
])

may_2022_payload_schema = StructType([
      StructField("after", may_2022_schema, True)
])

may_2022_full_schema = StructType([
      StructField("payload", may_2022_payload_schema, True)
])

# Đọc từ kafka
df = (spark.readStream 
      .format("kafka") 
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("subscribe", "cdc.public.may_2022")
      .option("startingOffsets", "earliest")
      .load()
      )

# Parse JSON để lấy payload.after.*

parsed_df = (df.selectExpr("CAST(value AS STRING)")
            .select(from_json(col("value"), may_2022_full_schema).alias("data"))
           .select("data.payload.after.*") )

parsed_df.printSchema()

# ✅ Ví dụ thống kê: số sản phẩm theo category
products_per_category = parsed_df.groupBy("category").agg(count("id").alias("total_products"))



query = products_per_category.writeStream \
    .outputMode("complete") \
    .foreachBatch(write_to_mysql) \
    .start()

query.awaitTermination()
