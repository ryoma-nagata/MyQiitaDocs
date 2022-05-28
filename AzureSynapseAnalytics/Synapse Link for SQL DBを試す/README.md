# Azure Synapse Link for SQL DB を試す

## はじめに

Build2022で発表されたAzure Synapse Link for SQL DBを試してみます。
Azure SQL DBに対してNoETLでDWHに連携する機能です。

[Build](https://mybuild.microsoft.com/ja-JP/home)

### 参考リンク

[Azure Synapse Link for SQL とは (プレビュー)](https://docs.microsoft.com/ja-jp/azure/synapse-analytics/synapse-link/sql-synapse-link-overview)

[Azure SQL Database 用 Azure Synapse Link (プレビュー)](https://docs.microsoft.com/ja-jp/azure/synapse-analytics/synapse-link/sql-database-synapse-link)

[Azure Synapse Link for Azure SQL Database (プレビュー) の構成](https://docs.microsoft.com/ja-jp/azure/synapse-analytics/synapse-link/connect-synapse-link-sql-database)


## 手順

### 準備

#### Synapse workspace 作成

synapse を作成します。
1. [Synapse ワークスペースの作成](https://docs.microsoft.com/ja-jp/azure/synapse-analytics/get-started-create-workspace) を参考にSynapse workspaceを作成します

設定全体
![](.image/2022-05-25-07-27-34.png)

2. SQL Poolを作成します。

![](.image/2022-05-25-08-21-48.png)



#### SQL DB作成

1. Azure Portalから論理SQL Serverを作成します。

![](.image/2022-05-25-07-41-24.png)

設定全体

![](.image/2022-05-25-07-54-19.png)

AD管理者の設定などをしています。
。

2. 作成後は **ネットワークタブ** にて自身のクライアントIPを登録しておきます

![](.image/2022-05-25-08-03-37.png)

3. 同様に **IDタブ** にてシステム割当マネージドIDを有効化しておきます。

![](.image/2022-05-25-08-04-26.png)

#### world wide importersの構成

 [world wide importers の作成](https://docs.microsoft.com/ja-jp/sql/samples/wide-world-importers-oltp-install-configure?view=sql-server-ver16#azure-sql-database)を参考にdbを構成します。

1. [wide-world-importers-release](https://github.com/Microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0)から対応バージョンのdacpacをダウンロードします。
2. SSMSからAD認証で対象sqlserverにログインし、データベースを右クリックして**データ層アプリケーションのインポート** を実行します。

![](.image/2022-05-25-08-00-53.png)

設定画面

![](.image/2022-05-25-08-06-59.png)

3. インポートが完了したらSynapseリソースをSQL DBのdb_ownerに指定します。

```sql

CREATE USER <workspace name> FROM EXTERNAL PROVIDER;
ALTER ROLE [db_owner] ADD MEMBER <workspace name>;

```


### 1. Synapse Lin for SQLの構成

1. 統合ハブから　**リンク接続** を選択します。

![](.image/2022-05-25-08-18-29.png)

2. **リンク接続** から **新規** を選択します。

![](.image/2022-05-25-08-19-07.png)

3. 準備で作成したDBを選択します。

![](.image/2022-05-25-08-20-10.png)

4. ソーステーブルを選択します。


![](.image/2022-05-25-08-20-58.png)


確認画面

![](.image/2022-05-25-08-34-08.png)

5. リンク接続を確認します。

![](.image/2022-05-25-08-34-38.png)

6. リンクの構成画面で、警告を確認します。

![](.image/2022-05-25-08-37-04.png)

7. 対応外の型を含むのでHeapに変更します。

![](.image/2022-05-25-08-38-04.png)

8. **発行** します。

![](.image/2022-05-25-08-38-51.png)

9. 選択したテーブルのターゲットスキーマが存在する必要があるので、SQLPool上で作成しておきます

```sql

CREATE SCHEMA [Sales]

```

![](.image/2022-05-25-08-42-14.png)

10. **開始** します。

![](.image/2022-05-25-08-39-22.png)

11. 数分経つと開始が完了します。

![](.image/2022-05-25-08-45-36.png)

監視画面がReplecatingとなります。

![](.image/2022-05-25-09-52-59.png)

### 2.データの確認

#### 開始直後

まずは、ソーステーブルの件数を見ておきます。

![](.image/2022-05-25-08-46-47.png)


専用SQL Pool側も開始が完了しているので、同じ件数になっています。

![](.image/2022-05-25-08-47-35.png)

#### データ増幅確認

以下のクエリで雑にデータを増幅します。

```sql

DECLARE @maxOrder int
DECLARE @count int
SELECT @maxOrder = max( [OrderID])
  FROM [Sales].[Orders]


INSERT INTO [Sales].[Orders]
SELECT TOP 10000 @maxOrder  + [OrderID]
      ,[CustomerID]
      ,[SalespersonPersonID]
      ,[PickedByPersonID]
      ,[ContactPersonID]
      ,[BackorderOrderID]
      ,[OrderDate]
      ,[ExpectedDeliveryDate]
      ,[CustomerPurchaseOrderNumber]
      ,[IsUndersupplyBackordered]
      ,[Comments]
      ,[DeliveryInstructions]
      ,[InternalComments]
      ,[PickingCompletedWhen]
      ,[LastEditedBy]
      ,[LastEditedWhen]
  FROM [Sales].[Orders]
  order by 1 

print N'INSERT件数:'+ convert(nvarchar,@@ROWCOUNT)

SELECT @count=COUNT(1) FROM [Sales].[Orders]

print N'結果件数:'+ convert(nvarchar,@count)

```

（generatorが動かなかった..)

データの挿入を実行します。

SQL DB側の結果
![](.image/2022-05-25-09-44-00.png)



約1分後にはデータが同期されています※ここだえタイムゾーンに気づかずにやっているので+9時間読み替え必要

Synapse側の結果
![](.image/2022-05-25-09-44-47.png)

```sql

DECLARE @count int 

SELECT @count=count(1)
 FROM [Sales].[Orders];

print N'時刻:' + convert(nvarchar,dateadd(hh,9,SYSDATETIME()))
print N'件数:'+ convert(nvarchar,@count)

```

増やすためにTop句を外してみます。

SQL DB側の結果
![](.image/2022-05-25-09-46-13.png)

これも即反映されています。

Synapse側の結果
![](.image/2022-05-25-09-48-05.png)

300万件くらいから少しずつ反映に時間がかかるようになりました。
(この辺になるとSQLDB側の生成に時間がかかるようになります)

SQL DB側の結果

![](.image/2022-05-25-10-17-25.png)


Synapse側の結果

![](.image/2022-05-25-10-20-44.png)


## まとめ

SQLファミリーを利用されている方々はETL不要で分析環境にデータをエクスポートできるのでかなりいいんじゃないでしょうか。

このままでも運用DBに負荷をかけないまま分析クエリが効率化されると思いますが、
SQL Pool側でストアドプロシージャを組んで一定間隔で実行し、適切なモデリングや分散テーブルに整形するなどでニアリアルタイム分析もはかどりそうです。
外部テーブルと連携してデータレイクにオフロードするのもいいですね。

コスト面が気になるところです。

引き続きBuild2022 楽しんでいきましょう!