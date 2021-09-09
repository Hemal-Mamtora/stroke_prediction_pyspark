from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.classification import GBTClassifier, RandomForestClassifier, DecisionTreeClassifier

spark = SparkSession.builder.appName('stroke').getOrCreate()

train_data = spark.read.csv("/user/hemal/train.csv",header=True,inferSchema=True)
test_data = spark.read.csv("/user/hemal/test.csv",header=True,inferSchema=True)

assembler=VectorAssembler(
  inputCols=[
    'gender','age','hypertension',
    'heart_disease','ever_married','work_type',
    'residence_type', 'avg_glucose_level', 'bmi', 'smoking_status'
    ],
  outputCol='features')

train=assembler.transform(train_data)
test= assembler.transform(test_data)

train.printSchema()
test.printSchema()

final_train= train.select('features','stroke')
final_test = test.select('features', 'stroke')

evaluator = BinaryClassificationEvaluator(labelCol = 'stroke')

dt = DecisionTreeClassifier(featuresCol = 'features', labelCol = 'stroke', maxDepth = 10)
dtModel = dt.fit(final_train)
DTpredictions = dtModel.transform(final_test)

rf = RandomForestClassifier(featuresCol = 'features', labelCol = 'stroke', numTrees=50)
rfModel = rf.fit(train)
RFpredictions = rfModel.transform(test)

gbt = GBTClassifier(featuresCol = 'features', maxIter=50, labelCol = 'stroke')
gbtModel = gbt.fit(train)
GBTpredictions = gbtModel.transform(test)

sample = open('samplefile2.txt', 'w') 

print("1. Evaluations For Decision Tree Classifier\n", file=sample)
DTpredictions.select('stroke', 'rawPrediction', 'prediction', 'probability').show(10)
print("Test Area Under ROC: " + str(evaluator.evaluate(DTpredictions, {evaluator.metricName: "areaUnderROC"})), file=sample)
print("Test Area Under Precision Recall Curve: " + str(evaluator.evaluate(DTpredictions, {evaluator.metricName: 'areaUnderPR'})), file=sample)
print(", file=sample")

print("2. Evaluations For Random Forest Classifier\n", file=sample)
RFpredictions.select('id', 'stroke', 'rawPrediction', 'prediction', 'probability').show(10)
print("Test Area Under ROC: " + str(evaluator.evaluate(RFpredictions, {evaluator.metricName: "areaUnderROC"})), file=sample)
print("Test Area Under Precision Recall Curve: " + str(evaluator.evaluate(RFpredictions, {evaluator.metricName: 'areaUnderPR'})), file=sample)
print("", file=sample)

print("3. Evaluations For Gradient Boosted Tree\n", file=sample)
GBTpredictions.select('id', 'stroke', 'rawPrediction', 'prediction', 'probability').show(10)
print("Test Area Under ROC: " + str(evaluator.evaluate(GBTpredictions, {evaluator.metricName: "areaUnderROC"})),file=sample)
print("Test Area Under Precision Recall Curve: " + str(evaluator.evaluate(GBTpredictions, {evaluator.metricName: 'areaUnderPR'})), file=sample)
print("", file=sample)
sample.close()
