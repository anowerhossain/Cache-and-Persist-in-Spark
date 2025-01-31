🚀 Apache Spark Optimization: cache() vs persist()

Apache Spark provides two key methods to optimize performance by reducing recomputation and improving execution speed ⚡:

- `cache()` → Stores data only in memory 🧠.
- `persist(storageLevel)` → Allows different storage levels like memory, disk, or both 💾.
- Using these methods efficiently can save processing time ⏳ and enhance Spark job performance 🔥.

### cache() 🧠

- `cache()` is a lazy transformation, meaning data is not cached immediately; Spark caches the DataFrame/RDD when an action (like `count()`, `show()`, etc.) is performed.
- It stores the data only in memory (RAM).
- If the cached data is lost due to memory constraints, Spark recalculates it from the original source.
- Uses Storage Level: `MEMORY_AND_DISK` (equivalent to `persist(StorageLevel.MEMORY_AND_DISK)`).

✅ Best use case: When the dataset is small to medium-sized and fits in memory.

❌ Limitations:

- If the dataset is too large to fit in memory, some partitions might be recomputed instead of spilling to disk.
-  No flexibility in choosing different storage levels.


### persist() 🧠 💾

- `persist()` is similar to `cache()`, but it provides different storage levels (memory, disk, or both).
- It allows fine-grained control over how data is stored.
- Default persistence level is `MEMORY_AND_DISK`, meaning if data does not fit in memory, Spark spills it to disk.

| Storage Level           | Description                                                   |
|-------------------------|--------------------------------------------------------------|
| MEMORY_ONLY             | Stores RDD/DataFrame in memory only. If memory is full,      |
|                         | Spark recomputes it.                                        |
| MEMORY_AND_DISK (default) | Stores in memory; if full, spills to disk.                 |
| MEMORY_ONLY_SER         | Stores in memory in serialized format (uses less RAM).       |
| MEMORY_AND_DISK_SER     | Stores in memory (serialized); spills to disk if needed.     |
| DISK_ONLY               | Stores on disk only (no memory storage).                     |


### Example: Data Pipeline Without cache() or persist() 🚀

Imagine a transformation pipeline where df1 transforms into df2, then df3, and finally df4.

```python
df1 = spark.read.csv("hdfs://data/sales.csv", header=True, inferSchema=True)
df2 = df1.filter(df1["region"] == "North America")  # Filter data
df3 = df2.groupBy("category").sum("sales")  # Aggregate sales by category
df4 = df3.withColumnRenamed("sum(sales)", "total_sales")  # Rename column

df4.show()
df4.write.mode("overwrite").parquet("hdfs://data/processed_sales")
```

Problem Without `cache()` or `persist()` `df4.show()` and `df4.write()` are executed separately, Spark will recompute all previous steps (`df1 → df2 → df3 → df4`) multiple times, wasting resources.

- To prevent recomputation, we cache df3 before performing the final transformation:

```python
df1 = spark.read.csv("hdfs://data/sales.csv", header=True, inferSchema=True)
df2 = df1.filter(df1["region"] == "North America")  
df3 = df2.groupBy("category").sum("sales").cache()  # Cache intermediate result
df4 = df3.withColumnRenamed("sum(sales)", "total_sales")

df4.show()  # Uses cached df3
df4.write.mode("overwrite").parquet("hdfs://data/processed_sales")  # Uses cached df3
```

- When df4.show() is called, df3 is cached in memory.
- When df4.write() runs, it uses the cached version of df3, avoiding recomputation. 
- Faster execution since Spark skips redundant steps.
- If df3 is too large for memory, we use persist() instead of cache() to allow disk storage:
  
  ```python
  df3 = df2.groupBy("category").sum("sales").persist(StorageLevel.MEMORY_AND_DISK)  # Store in memory/disk
  ```

  🔥 Performance Optimization Tips
✅ Use cache() for iterative processing (when the same data is accessed multiple times).
✅ Use persist() for large datasets that may not fit into memory.
✅ Unpersist data 🧹 (df.unpersist()) when it's no longer needed to free memory.

