hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/hemal
hdfs dfs -copyFromLocal ~/Desktop/stroke\ data/* /user/hemal
hdfs dfs -copyFromLocal ~/Desktop/stroke_data/* /user/hemal
hdfs dfs –chmod –R 755 /user/hemal
hdfs dfs -chmod -R 755 /user/hemal

Command to run job
$SPARK_HOME/bin/spark-submit trial.py