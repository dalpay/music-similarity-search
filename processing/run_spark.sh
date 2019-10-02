# spark-submit --master local[*] --package org.postgresql:postgresql:42.1.1 batchprocessing.py --conf "spark.dynamicAllocation.enable = true" --conf "spark.dynamicAllocation.executorIdleTimeout = 2m" --conf "spark.dynamicAllocation.minExecutors = 1" --conf "spark.dynamicAllocation.maxExecutors = 2000" --conf "spakr.stage.maxConsecutiveAttempts = 10" --conf "spark.memory.offHeap.enable = true" --conf "spark.memory.offheep.size = 3g" --conf "spark.yarn.executor.memoryOverhead = 0.1 * (spark.executor.memory + spark.memory.offHeap.size)"

spark-submit --master local[*] ~/project/processing/spark_processing.py --number 50 --source msd --method gauss
