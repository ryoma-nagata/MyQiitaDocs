---
title: Azure Databricks サーバーレス SQL Warehouse からファイアウォールの背後のデータレイクに接続する
tags:
  - Microsoft
  - Azure
  - AzureStorage
  - DataLake
  - Databricks
private: false
updated_at: '2023-03-03T15:57:48+09:00'
id: 5cc56db7aa355ffe5ff5
organization_url_name: null
slide: false
---
## はじめに

[サーバーレス SQL ウェアハウスからのアクセスを許可するように Azure Storage ファイアウォールを構成する](https://learn.microsoft.com/ja-jp/azure/databricks/sql/admin/serverless-firewall)に記載の通り、
Azure Databricks サーバレスSQL Warehouse をファイアウォールの背後のストレージに接続するためには以下の構成用にサブネットを登録する必要がありますので、試してみます。

![](.image/2023-03-03-13-23-05.png)
![2023-03-03-13-23-05.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/2081916d-d467-a8bb-062d-14752d446459.png)


ただ、数が多いです。

![2023-03-03-13-25-21.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/66220e05-d024-14a7-d52d-52da4e6caeb4.png)

引用:[サーバーレス SQL サブネット](https://learn.microsoft.com/ja-jp/azure/databricks/resources/supported-regions#serverless-sql-subnets)

portal だけで完結したいので、テンプレートを作りました。

https://github.com/ryoma-nagata/register-databricks-serverless-sql-subnet


## 手順

### 準備

Data Lake Storage Gen2を有効化したストレージアカウントとシークレット格納用のkey vault、Premium エディションのDatabricksを準備します。
リージョンは現時点でプレビュー可能なCentralUSです。


また、データレイクへのアクセス用にサービスプリンシパルを用意し、Data Lake の ストレージ Blob データ共同作成者にしています

![2023-03-03-13-37-00.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/74eb3c97-3a7a-0eeb-2c55-6eb72a4d3b19.png)


シークレットスコープとシークレットの登録は、[UI を使用して Azure Key Vault でサポートされるシークレットのスコープを作成する](https://learn.microsoft.com/ja-jp/azure/databricks/security/secrets/secret-scopes#create-an-azure-key-vault-backed-secret-scope-using-the-ui)を参考にしてください。

![2023-03-03-13-44-22.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/6179a6f6-6cf6-65ba-f7d3-53cb230d421b.png)


### 1. サーバレスSQL ウェアハウスを有効にする

基本的に[
ステップ 1: ワークスペースのサーバーレス SQL ウェアハウスを有効にする](https://learn.microsoft.com/ja-jp/azure/databricks/sql/admin/serverless#---step-1-enable-serverless-sql-warehouses-for-your-workspace)に従います。

![2023-03-03-13-37-12.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/b55fb7db-aa63-3f7e-b0d5-d31104f33adb.png)


ここで変更を反映後は、サーバレスSQLが実行できるはずです。

![2023-03-03-13-48-10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/4543fb58-0761-537b-770d-c49235c77965.png)


### 2. サービスプリンシパルのアクセスを構成する

1.**+ Services Principal を追加**をクリックして表示されるサービスプリンシパルの追加画面から、情報を入力し、変更を反映します。

![2023-03-03-13-45-16.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/777fd80a-1843-d9e8-2223-4b522398b319.png)


2.テストとして、サーバレスSQLで、Create table してみます。

```sql:sql

CREATE TABLE test_non_fw (
id int 
)
USING DELTA 
LOCATION 'abfss://<コンテナ名>@<ストレージアカウント名>.dfs.core.windows.net/lakehouse/default/test_non_fw'

```

![2023-03-03-13-57-44.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/ab764d66-1e29-eb2f-33de-1b27308c7087.png)


作れてます。


![2023-03-03-13-58-29.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/7d3ebf49-81eb-ef0f-a8b6-45a7cea68247.png)

### 3. データレイクのファイアウォール設定を構成する

1.まず単純にファイアウォールを設定します。

![2023-03-03-13-59-31.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/f2815e63-2905-d571-db9d-33d4d9ad4b93.png)


2.すると、サーバレスSQLからはアクセスができなくなります。
![2023-03-03-14-00-42.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/1ef637f9-fac0-1521-ddb7-a3f110b9fb53.png)


3.サーバレスサブネットを許可するため、[テンプレート](https://github.com/ryoma-nagata/register-databricks-serverless-sql-subnet)を使っていきます。

![2023-03-03-14-04-35.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/4ada8440-78e1-012c-43eb-fb32b66aded1.png)

4.サンプルパラメータファイルが、Central USのサブネットを許可するものになっていますのでそのまま使います。

![2023-03-03-14-04-59.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/92b4f185-6db6-4287-445e-94fc1b413028.png)


5.成功を確認後、ネットワーク設定が反映されていることを確認します。

![2023-03-03-14-06-03.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/fb12fc12-c039-7ed7-2a05-b0db716926d2.png)


### 4. 実行の確認

 クエリが成功することを確認します。

※わかりにくいのでinsert 文も実行しました。

![2023-03-03-14-08-46.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/ca06a780-0ae3-243f-492c-7243f8ad74ad.png)
