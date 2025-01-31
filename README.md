## Cache-and-Persist-in-Spark ( Optimization )

`cache()` and `persist()` in Apache Spark are used to store intermediate results in memory to speed up computation. However, they have key differences in how they store the data and their flexibility.

### cache()

- `cache()` is a lazy transformation, meaning data is not cached immediately; Spark caches the DataFrame/RDD when an action (like `count()`, `show()`, etc.) is performed.
- It stores the data only in memory (RAM).
- If the cached data is lost due to memory constraints, Spark recalculates it from the original source.
- Uses Storage Level: `MEMORY_AND_DISK` (equivalent to `persist(StorageLevel.MEMORY_AND_DISK)`).

✅ Best use case: When the dataset is small to medium-sized and fits in memory.

❌ Limitations:

- If the dataset is too large to fit in memory, some partitions might be recomputed instead of spilling to disk.
-  No flexibility in choosing different storage levels.


### persist()

- `persist()` is similar to `cache()`, but it provides different storage levels (memory, disk, or both).
- It allows fine-grained control over how data is stored.
- Default persistence level is `MEMORY_AND_DISK`, meaning if data does not fit in memory, Spark spills it to disk.

+------------------------+---------------------------------------------------------------+
| Storage Level          | Description                                                   |
+------------------------+---------------------------------------------------------------+
| MEMORY_ONLY            | Stores RDD/DataFrame in memory only. If memory is full,       |
|                        | Spark recomputes it.                                         |
+------------------------+---------------------------------------------------------------+
| MEMORY_AND_DISK (default) | Stores in memory; if full, spills to disk.                |
+------------------------+---------------------------------------------------------------+
| MEMORY_ONLY_SER       | Stores in memory in serialized format (uses less RAM).        |
+------------------------+---------------------------------------------------------------+
| MEMORY_AND_DISK_SER   | Stores in memory (serialized); spills to disk if needed.      |
+------------------------+---------------------------------------------------------------+
| DISK_ONLY             | Stores on disk only (no memory storage).                      |
+------------------------+---------------------------------------------------------------+
