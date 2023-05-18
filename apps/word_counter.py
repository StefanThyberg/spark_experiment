from functools import reduce
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

DB_NAME = "word_data"

def init_spark():
  session = SparkSession.builder\
    .appName("word-counter")\
    .config("spark.jars", "/opt/spark-lib/postgresql-42.2.22.jar")\
    .getOrCreate()
  sc = session.sparkContext
  return session,sc

def main():
  url = f"jdbc:postgresql://demo-database:5432/{DB_NAME}"
  properties = {
    "user": "postgres",
    "password": "casa1234",
    "driver": "org.postgresql.Driver"
  }
  file = "/opt/spark-data/shakespeare.txt"
  session, sc = init_spark()
  df = session.read.text(file)

  df.repartition(4) \
    .withColumn("word", F.explode(F.split(F.lower(F.col("value")), "\s+"))) \
    .withColumn("word", F.regexp_replace("word", "[^\w]", "")) \
    .filter("word != ''") \
    .groupBy("word") \
    .count() \
    .sort("count", ascending=False) \
    .write \
    .jdbc(url=url, table=DB_NAME, mode="overwrite", properties=properties)

if __name__ == '__main__':
  main()