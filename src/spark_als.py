from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

from .make_preference_matrix import make_preference_df
import pandas as pd
import pymongo

mc=pymongo.MongoClient()
db=mc['game_recommender']
reviews=db['reviews']

spark = SparkSession.builder.getOrCreate()
spark_df=spark.createDataFrame(make_preference_df())

(training, test) = spark_df.randomSplit([0.8, 0.2])

als = ALS(maxIter=5, regParam=0.01, rank=10,
            userCol="user_number",itemCol="game_number",
            ratingCol="score",coldStartStrategy="drop")

model = als.fit(training)

user_factors = model.userFactors.toPandas()
item_factors = model.itemFactors.toPandas()

predictions = model.transform(test)
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
                                predictionCol="prediction")

rmse = evaluator.evaluate(predictions)
