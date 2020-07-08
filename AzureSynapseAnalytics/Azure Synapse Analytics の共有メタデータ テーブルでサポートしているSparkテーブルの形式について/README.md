## 注意点

本情報は、2020年6月23日時点での情報であり、最新情報は、Microsoftドキュメントを参照してください。



## 概要

Qiitaの別記事にて記述した本件ですが、下記記事についてややわかりにくい表現があり、誤解した同僚がいたので備忘録

>   Azure Synapse Analytics では、さまざまなワークスペース計算エンジンが、Spark プール (プレビュー) と SQL オンデマンド エンジン (プレビュー) の間でデータベースとテーブルを共有できます。

引用元：[Azure Synapse Analytics の共有メタデータ](https://docs.microsoft.com/ja-jp/azure/synapse-analytics/metadata/overview)



## 誤解した点

ドキュメントにて、下記の記載があっため、

>   SQL エンジンを使用して Parquet 形式でデータを格納するマネージドおよび外部 Spark テーブルのみが共有されます。

引用元：[SQL での Spark テーブルの公開](https://docs.microsoft.com/ja-jp/azure/synapse-analytics/metadata/table#exposing-a-spark-table-in-sql)



下記のテーブルがサポートされていると勘違いしていたようです。

-   Parquet 形式でデータを格納するマネージドテーブル
-   外部 Spark テーブル



ただ、英語のドキュメントに下記の記載があるため、

>    only shares managed and external Spark tables that store their data in Parquet format with the SQL engines. 

引用元：[Exposing a Spark table in SQL](https://docs.microsoft.com/en-us/azure/synapse-analytics/metadata/table#exposing-a-spark-table-in-sql)



正しくは下記の解釈となります。句読点があれば違ったかもしれませんね

-   Parquet 形式でデータを格納するマネージドテーブル
-   Parquet 形式でデータを格納する外部 Spark テーブル



## 所感

とりあえずdocsのほうはプルリクなげましたが、英語版のドキュメントも合わせて確認すべきであると再認識しました。
