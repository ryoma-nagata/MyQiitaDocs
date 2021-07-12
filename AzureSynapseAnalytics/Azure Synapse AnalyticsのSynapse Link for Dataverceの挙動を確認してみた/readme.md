## はじめに

Microsoft Buildの
[Harness the power of data in your applications with Azure](https://mybuild.microsoft.com/sessions/46f12ac0-4d74-4a53-95b1-22e406edd72c)
にてアナウンスされたSynapse Link for Dataverseを試した手順を記載します。

※2021/07時点の情報です

### Azure Synapse Link for Dataverse とは

Microsoft Dataverse からデータレイクにエクスポートする機能は以前から存在しており、Common Data Modelのフォーマットを利用することで、Azure上で更に高度な分析ワークロードにシームレスにつなぐことが示唆されていました。

![](https://docs.microsoft.com/en-us/common-data-model/media/cdm-data-lake-2.png)
>https://docs.microsoft.com/en-us/common-data-model/data-lake

Synapse Link for Dataverseでは、出力されたCDM形式のデータがネイティブにSynapse Analyticsとつながることで、より簡単に分析を進めることができるようになります。

![](https://docs.microsoft.com/ja-jp/powerapps/maker/data-platform/media/azure-synapse-link-overview.png)


### 参考リンク

[Azure Synapse Link for Dataverse とは](https://docs.microsoft.com/ja-jp/powerapps/maker/data-platform/export-to-data-lake)

[Accelerate time to insight with Azure Synapse Link for Dataverse](https://cloudblogs.microsoft.com/powerplatform/2021/05/26/accelerate-time-to-insight-with-azure-synapse-link-for-dataverse/)

[Spark CDMコネクタ](https://github.com/Azure/spark-cdm-connector)

[自分の Azure Synapse ワークスペースを使用して Azure Synapse Link for Dataverse を構成する (プレビュー)](https://docs.microsoft.com/ja-jp/powerapps/maker/data-platform/azure-synapse-link-synapse)

[Power Platform で広がるデータ インテグレーションの世界 (1/2)](https://www.microsoft.com/ja-jp/events/decode/2020session/detail.aspx?sid=B07&tk=B)

こちらで、Dataverseとデータレイクの統合と、Azureへの再利用が紹介されています。

## 確認手順

### 事前準備

#### Power Appsの環境作成

[Power Apps管理ポータル](https://admin.powerplatform.microsoft.com/environments)にて環境を作成します。筆者は日本で作成しました。
※ライセンスがない場合は種類を評価版に変更しましょう

![](.media/paps01.png)

「データベース作成」は「はい」を選んでおきます

![](.media/paps02.png)

「サンプルアプリおよびデータの展開」を「はい」にするとたくさんデータがクエリできます

![](.media/paps03.png)





#### Azure Synapse Analytics の作成

Azure Portalから作成しますが、Power Apps環境が既定では西日本でであることがあるので、西日本の環境を使用する際は、西日本にデプロイするように注意しましょう

筆者は東日本で作成しました。

手順は以下を参照ください。

[Synapse ワークスペースの作成](https://docs.microsoft.com/ja-jp/azure/synapse-analytics/get-started-create-workspace)

#### 権限の確認

以下の権限が必要になります。
- 対象リソースグループの所有者
※もし難しい場合は、閲覧者とストレージのBlobデータ共同作成者をもらってください。
- Synapse管理者※リソース作成者に自動的に割り当てられます

### Synapse Link for Dataverseを構成する

作成したPower Apps環境内で、「Azure Synapse Link」-> 「データレイクへの新しいリンク」を選択していきます。

![](.media/paps04.png)

Synapse Linkのチェックボックスをチェックし、作成したSynapse Workspaceを選んでいきます。
ここで、権限が足りないorリージョンが異なると表示されなかったり、エラーが出ます。

![](.media/paps05.png)


対象テーブルを選択します。とりあえず全て選びました。

![](.media/paps06.png)

しばらく待つとリンクが完了します（数分）
Synapse Studioへ遷移するボタンが表示されます

![](.media/paps07.png)


### Synapse Studio からテーブルの確認

Synapse Studioを使って確認していきます。
はじめにデータレイク

DataVerseではじまるファイルシステムが作成され、先ほどインポート対象にしたエンティティ群がインポートされています。

![](.media/syna01.png)

次に、テーブルを確認します。
DataverseでインポートされたエンティティはSparkテーブルとして登録されます。スキーマ情報もきちんと連携できているように見えます。Azure Machine Learningによる自動機械学習もできそうです。

Spark テーブルはServerless SQL Poolからもアクセスが可能なので、右クリックで内容を確認してみます。

![](.media/syna02.png)

spark Dataframeとしての読み込み右クリックから呼び出してこのような形になります。

![](.media/syna03.png)

spark table として登録されているのでDESCRIBEの結果を見てみます。
locationなんかは想定通りにとれていましたが、それ以外の情報はほぼありませんでした。
![](.media/syna04.png)

![](.media/syna05.png)


### 蛇足:自前で構成できないか試した

Spark Poolには組み込みのCDMコネクタがインストールされています。（詳細は記事先頭の参考リンクをご覧ください）
これを利用してSynapse Linkがやったことを追ってみます。あわよくば他のCDM形式で連携される製品（Power BI Dataflowなど）をSynapse Link for Dataverseと同じような使い勝手にできるはずです

はじめにCDMコネクタを利用して、CDM形式で保存された各エンティティをdf.readしてみます。

```python:pyspark

readDf = (spark.read.format("com.microsoft.cdm")
  .option("storage",  "<storage account名>.dfs.core.windows.net")
  .option("manifestPath","dataverse-dvtest-unq4ecc478bf88244cf8eab341a8a032/model.json")
  .option("entity", "connectionroleassociation") 
  .load())

display(readDF)

```

![](.media/syna06.png)

これをSparkテーブルとして登録するためには、saveAsTableを実行する必要がありますが、試しにcdm形式でsaveAsTableしてみたらエラーとなりました。

```python

(readDf.write.format("com.microsoft.cdm")
  .option("storage", "<storage account名>.dfs.core.windows.net")
  .option("manifestPath", "dataverse-dvtest-unq4ecc478bf88244cf8eab341a8a032/model2.json")
  .option("entity", "TestEntity")
  .option("format", "parquet")
  .option("compression", "gzip")
  .saveAsTable("TestEntity"))

```

![](.media/syna07.png)


また、Synapse Link for Dataverseで作成されたテーブルは、うまくmodel.json/manifest.jsonのファイルを使って、外部テーブル化されています。（synapse/warehouseフォルダにデータをもたない）

マネージドテーブルについて参考
[AzureSynapseAnalyticsのメタデータ共有についてわかったこと
](https://qiita.com/ryoma-nagata/items/300ae6df431642bc9919)

外部テーブルを作る方法として、saveAsTableでパスを指定する以外に、SQLで外部テーブルを作成する方法もありますが、cdm形式での指定の仕方は不明でした。

```sql:sql

CREATE TABLE <テーブル名> 
USING <Format> 
LOCATION <abfssパス>

```

Synapse Link for Dataverseを連携したとき、Spark テーブルとして登録されているにもかかわらず、Spark sessionが起動した形跡はありませんでした。
Synapse Link for Dataverseでは、データレイクにエクスポート後は独自の方法でメタストアに直接テーブルの登録を行っているようです。

以上となりますが、上記蛇足もふくめて記事が役に立てば幸いです。
（もし、CDMコネクタを使って外部テーブルを作成する方法がわかる方がいたらぜひご指摘ください。。）