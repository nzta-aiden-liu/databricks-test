# Databricks notebook source
import dlt
import json
import requests
from pyspark.sql import types as T
from pyspark.sql import functions as F

# COMMAND ----------

@dlt.table(
    name="users",
    comment="""
    Request URL: https://reqres.in/api/users,
    Response: [
        {
            "page": 1,
            "per_page": 6,
            "total": 12,
            "total_pages": 2,
            "data": [
                {
                    "id": 1,
                    "email": "george.bluth@reqres.in",
                    "first_name": "George",
                    "last_name": "Bluth",
                    "avatar": "https://reqres.in/img/faces/1-image.jpg"
                },
                ...
            ],
            "support": {
                "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
                "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
            }
        }
    ]
    Schema: id, email, first_name, last_name, avatar
    """
)
def users():
    response = requests.get("https://reqres.in/api/users", headers={"Accept": "application/json", "x-api-key": "reqres-free-v1"})
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    data = json.loads(response.text)["data"]
    return (
        spark.createDataFrame(data, schema=T.StructType([
                T.StructField("id", T.IntegerType()),
                T.StructField("email", T.StringType()),
                T.StructField("first_name", T.StringType()),
                T.StructField("last_name", T.StringType()),
                T.StructField("avatar", T.StringType())
            ])
        )
    )

# COMMAND ----------

@dlt.table()
def resource():
    response = requests.get("https://reqres.in/api/{resource}", headers={"Accept": "application/json", "x-api-key": "reqres-free-v1"})
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    data = json.loads(response.text)["data"]
    return (
        spark.createDataFrame(data, schema=T.StructType([
                T.StructField("id", T.IntegerType()),
                T.StructField("name", T.StringType()),
                T.StructField("year", T.IntegerType()),
                T.StructField("color", T.StringType()),
                T.StructField("pantone_value", T.StringType())
            ])
        )
    )

# COMMAND ----------

spark.table("dev_bronze.stockmarket_nasdaq_raw.resource").show()