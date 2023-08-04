---
title: Databricks上でPysparkデータフレームからRデータフレームに変換する
tags:
  - R
  - Spark
  - Pyspark
  - Databricks
private: false
updated_at: '2020-03-12T20:39:32+09:00'
id: bc7fcc1ea3a5c4d5c7f0
organization_url_name: null
slide: false
---
#はじめに
Databricks上で、Pyspark データフレーム->SparkRデータフレーム->Rデータフレーム　へ変換する方法のメモ


#コード

##Pyspark データフレーム作成
``` :notebook
%python
# データフレーム作成
spark_df = spark.createDataFrame([('a01', 150),('a02', 160)], ["item", "price"])
print(type(spark_df))
spark_df.show()

# Tempviewを作成
spark_df.createOrReplaceTempView("tempview_sparkr")

```
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/d41c235e-94b0-4ba2-97ab-526f235b67a7.png)

##SparkR データフレーム作成

``` :notebook

%r
# テーブルからSparkRデータフレームを作成
library(SparkR)
sparkr_df <- sql("select * from tempview_sparkr")
print(class(sparkr_df))
head(sparkr_df)

```
 ![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/27215678-556c-0232-fa57-92b6760e2a1b.png)

##R データフレーム作成
 
``` :notebook



%r
# SparkRデータフレームから Rデータフレームに変換
library(SparkR)

r_df <- collect(sparkr_df)

print(class(r_df))

head(r_df)

```
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/440b96ad-8407-8009-6ccb-1492a7b6174e.png)

# 各種ダウンロードリンク
## Databricksに直接インポートしたい方はこちら
[GitHub Pagesに飛びます](https://ryoma-nagata.github.io/MyDatabricks/samples/html/transform_r_df.html)
## dbcをダウンロードしたい方はこちら
[dbcファイルがダウンロードされます](https://github.com/ryoma-nagata/MyDatabricks/blob/master/samples/dbc/transform_r_df.dbc?raw=true)
