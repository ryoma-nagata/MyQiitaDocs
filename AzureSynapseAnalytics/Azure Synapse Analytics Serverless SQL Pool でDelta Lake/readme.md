## はじめに

BuildあたりでプレビューがはじまったSynapse Analytics Serverless SQL PoolでのDelta Lakeのチュートリアルを紹介します。

参考のMSDocsのやつの拡張版的にお使いください。

※2021/6の情報となります

### 参考：

[Query Delta Lake files (preview) using serverless SQL pool in Azure Synapse Analytics](https://docs.microsoft.com/ja-jp/azure/synapse-analytics/sql/query-delta-lake-format)

[Synapse SQL で外部テーブルを使用する](https://docs.microsoft.com/ja-jp/azure/synapse-analytics/sql/develop-tables-external-tables?tabs=hadoop)


[Query Delta Lake files using T-SQL language in Azure Synapse Analytics](https://techcommunity.microsoft.com/t5/azure-synapse-analytics/query-delta-lake-files-using-t-sql-language-in-azure-synapse/ba-p/2388398)

## Delta Lake について

まずは手前味噌ですが

[Databrikcsのはじめかた](https://www.slideshare.net/ssuser61ea57/databricks-241742489)

[Delta Lake概要](https://www.slideshare.net/ssuser61ea57/delta-lakesummary-232412669)
※0.3のころなので古い点あるかも

DatabricksのCSAの方がめちゃめちゃわかりやすく活用方法まで記事を書いてくれています。

[@taka_yayoi](https://qiita.com/taka_yayoi)

[Qiita検索結果](https://qiita.com/search?q=Delta+Lake)

## サンプルコード

### Spark Poolでデータを準備

[Azure Open Datasets](https://docs.microsoft.com/ja-jp/azure/open-datasets/dataset-us-population-county?tabs=azureml-opendatasets)からアメリカの人口データを使っていきます。

300万件くらいのデータです。

```python:pyspark

# Create Data Frame and Display
from azureml.opendatasets import UsPopulationCounty

population = UsPopulationCounty()
population_df = population.to_spark_dataframe()
display(population_df.limit(5))

```


```python:pyspark

# Write format Delta

(population_df.write
.format("delta")
.mode("overwrite")
.save("abfss://datalake@<Azure Data Lake Storage Gen2名を入れてください>.dfs.core.windows.net/bronze/UsPopulationCounty/"))


```


#### ちなみに

Spark SQLでテーブル登録
この場合はSparkテーブルとして登録されますが、今のところServerelssSQLPoolからはうまく動作しません。


```sql:sql

CREATE TABLE UsPopulationCounty
USING DELTA
LOCATION 'abfss://datalake@<Azure Data Lake Storage Gen2名を入れてください>.dfs.core.windows.net/bronze/UsPopulationCounty/'


```

### Serverless SQL Pool でクエリ

右クリックから100行選択→パスをフォルダに変えてFORMATをDELTAに変更するのが簡単です

```sql:sql

SELECT
    TOP 100 *
FROM
    OPENROWSET(
        BULK 'https://dlsanalyticsdemo.dfs.core.windows.net/datalake/bronze/UsPopulationCounty/',
        FORMAT='DELTA'
    ) AS [result]


```

### Serverless SQL Pool 上で外部テーブル化

こちらも右クリックからスクリプトを生成させるのが楽です。

![](.media/001.png)

フォーマットがDeltaで、locationがファイルになっているので、変更します。（ハイライト箇所）

![](.media/002.png)

![](.media/003.png)


修正後のSQL例

```sql:sql

IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE name = 'SynapseDeltaFormat') 
	CREATE EXTERNAL FILE FORMAT [SynapseDeltaFormat] 
	WITH ( FORMAT_TYPE = delta)
GO

IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'datalake_<>_dfs_core_windows_net') 
	CREATE EXTERNAL DATA SOURCE [datalake_<>_dfs_core_windows_net] 
	WITH (
		LOCATION   = 'https://<Storage Account 名>.dfs.core.windows.net/datalake', 
	)
Go

CREATE EXTERNAL TABLE dbo.UsPopulationCountrySQL (
	[decennialTime] varchar(8000),
	[stateName] varchar(8000),
	[countyName] varchar(8000),
	[population] int,
	[race] varchar(8000),
	[sex] varchar(8000),
	[minAge] int,
	[maxAge] int,
	[year] int
	)
	WITH (
	LOCATION = 'bronze/UsPopulationCounty/',
	DATA_SOURCE = [datalake_<>_dfs_core_windows_net],
	FILE_FORMAT = [SynapseDeltaFormat]
	)
GO

SELECT TOP 100 * FROM dbo.UsPopulationCountrySQL
GO

```

実行後、外部テーブルとして表示されます。

![](.media/004.png)

なお、外部テーブル定義についてはデフォルトだと文字長が最大でとられてしまうので、適宜変更しましょう。

