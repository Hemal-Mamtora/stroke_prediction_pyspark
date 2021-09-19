## Commands to store data on local hdfs:

1. `hdfs dfs -mkdir /user`
2. `hdfs dfs -mkdir /user/hemal`
3. `hdfs dfs -copyFromLocal ~/Desktop/stroke\ data/* /user/hemal`
4. `hdfs dfs -copyFromLocal ~/Desktop/stroke_data/* /user/hemal`
5. `hdfs dfs –chmod –R 755 /user/hemal`
6. `hdfs dfs -chmod -R 755 /user/hemal`

Command to run job:

`$SPARK_HOME/bin/spark-submit trial.py`
