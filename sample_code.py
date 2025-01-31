from pyspark.sql import SparkSession
from pyspark import StorageLevel

spark = SparkSession.builder.appName("CachePersistExample").getOrCreate()

df1 = spark.read.csv("hdfs://data/sales.csv", header=True, inferSchema=True)

df2 = df1.filter(df1["region"] == "North America")
df3 = df2.groupBy("category").sum("sales").persist(StorageLevel.MEMORY_AND_DISK)  # Store in memory/disk
df4 = df3.withColumnRenamed("sum(sales)", "total_sales")

df4.show()  # Uses persisted df3
df4.write.mode("overwrite").parquet("hdfs://data/processed_sales")  # Uses persisted df3

df3.unpersist()  # Free up memory
