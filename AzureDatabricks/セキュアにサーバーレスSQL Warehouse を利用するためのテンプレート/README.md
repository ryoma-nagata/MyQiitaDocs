## はじめに

[サーバーレス SQL ウェアハウスからのアクセスを許可するように Azure Storage ファイアウォールを構成する](https://learn.microsoft.com/ja-jp/azure/databricks/sql/admin/serverless-firewall)に記載の通り、
Azure Databricks サーバレスSQL Warehouse をファイアウォールの背後のストレージに接続するためには以下の構成用にサブネットを登録する必要がありますので、試してみます。

![](.image/2023-03-03-13-23-05.png)

また、数が多いのと、portal だけで完結したいので、テンプレートを作りました。

![](.image/2023-03-03-13-25-21.png)

引用:[サーバーレス SQL サブネット](https://learn.microsoft.com/ja-jp/azure/databricks/resources/supported-regions#serverless-sql-subnets)


## 手順

### 準備

Data Lake Storage Gen2を有効化したストレージアカウントとシークレット格納用のkey vault、Premium エディションのDatabricksを準備します。
リージョンは現時点でプレビュー可能なCentralUSです。


また、データレイクへのアクセス用にサービスプリンシパルを用意し、Data Lake の ストレージ Blob データ共同作成者にしています
8942ec59-80b8-4a4c-b002-32b6193ca367
2065fdbc-aa3b-483a-bea9-63e559ef5eff
FBh8Q~xVLZlDKN6hJXfz.HtIDhjMxOUFOT6.Qc8L

![](.image/2023-03-03-13-37-00.png)

シークレットスコープとシークレットの登録は、[UI を使用して Azure Key Vault でサポートされるシークレットのスコープを作成する](https://learn.microsoft.com/ja-jp/azure/databricks/security/secrets/secret-scopes#create-an-azure-key-vault-backed-secret-scope-using-the-ui)を参考にしてください。

![](.image/2023-03-03-13-44-22.png)

### 1. サーバレスSQL ウェアハウスを有効にする

基本的に[
ステップ 1: ワークスペースのサーバーレス SQL ウェアハウスを有効にする](https://learn.microsoft.com/ja-jp/azure/databricks/sql/admin/serverless#---step-1-enable-serverless-sql-warehouses-for-your-workspace)に従います。

![](.image/2023-03-03-13-37-12.png)

ここで変更を反映後は、サーバレスSQLが実行できるはずです。

![](.image/2023-03-03-13-48-10.png)

### 2. サービスプリンシパルのアクセスを構成する

1. **+ Services Principal を追加**をクリックして表示されるサービスプリンシパルの追加画面から、情報を入力

![](.image/2023-03-03-13-45-16.png)

2. テストとして、サーバレスSQLで、Create table してみます。

```sql:sql

CREATE TABLE test_non_fw (
id int 
)
USING DELTA 
LOCATION 'abfss://<コンテナ名>@<ストレージアカウント名>.dfs.core.windows.net/lakehouse/default/test_non_fw'

```

![](.image/2023-03-03-13-57-44.png)

作れてます。

![](.image/2023-03-03-13-58-29.png)

### 3. データレイクのファイアウォール設定を構成する

1. まず単純にファイアウォールを設定します。

![](.image/2023-03-03-13-59-31.png)

2. すると、サーバレスSQLからはアクセスができなくなります。

![](.image/2023-03-03-14-00-42.png)

3. サーバレスサブネットを許可するため、[テンプレート](https://github.com/ryoma-nagata/register-databricks-serverless-sql-subnet)を使っていきます。

![](.image/2023-03-03-14-04-35.png)

4. サンプルパラメータファイルが、Central USのサブネットを許可するものになっていますのでそのまま使います。

![](.image/2023-03-03-14-04-59.png)

5. 成功を確認後、ネットワーク設定が反映されていることを確認します。

![](.image/2023-03-03-14-06-03.png)

### 4. 実行の確認

 クエリが成功することを確認します。

※わかりにくいのでinsert 文も実行しました。

![](.image/2023-03-03-14-08-46.png)