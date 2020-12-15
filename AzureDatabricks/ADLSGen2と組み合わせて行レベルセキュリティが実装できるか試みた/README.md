## はじめに

delta lakeテーブルのパーティションと、Azure DatabricksのAADパススルー、Azure Data Lake Storage Gen2のACLを組み合わせればDatabricks上で行レベルセキュリティが実装できるんじゃないかと思い試してみました。
(2020/11時点情報)

参考  
[Azure Data Lake Storage Gen2 のアクセス制御リスト | Microsoft Docs​​​​​​​](https://docs.microsoft.com/ja-jp/azure/storage/blobs/data-lake-storage-access-control)  
[Azure Active Directory 資格情報パススルーを使用して Azure Data Lake Storage へのアクセスをセキュリティで保護する](https://docs.microsoft.com/ja-jp/azure/databricks/security/credential-passthrough/adls-passthrough)


## 結論

特定のパーティションを参照するようにwhere文を指定していれば機能しましたが、通常の行レベルセキュリティの使用感とは異なる形です。  
権限をもたないレコードにはアクセスできないようにするという意味では達成していますが、実用は少し厳しいかもしれません。　　
UDFなどを利用して、ユーザ情報を取得・利用した認可用制御用のテーブルをかませてあげればよさそうですが、その場合ACLを使う必要はなくなりますね


## 手順

### データ作成

適当なクラスターでストレージにdeltaフォーマットデータを書き込みます。

``` :python

df = spark.read.json("dbfs:/databricks-datasets/iot/iot_devices.json")
# partitionをcca2（国コード）で分割して保存
location = "/mnt/mymt/iot"
df.write.partitionBy("cca2").format("delta").save(location)

```

### aclの権限付与

[Azure Data Lake Storage Gen2 のアクセス制御リスト (ACL) を再帰的に設定する](https://docs.microsoft.com/ja-jp/azure/storage/blobs/recursive-access-control-lists?tabs=azure-powershell#prerequisites)
が私のローカルのAzure Storage Explorerからだと効かなかったのでちょっと頑張ります

以下のように権限を振ります。

- ルートのコンテナ:x(実行)を付与
  - iotフォルダ:x
    - _delta_logフォルダとその配下ファイル:x,r,w
    - cca2=DAフォルダとその配下ファイル:x,r,w

### テーブル作成

adパススルーを有効にしたクラスタで以下を実行

```:python

location = "/mnt/mymt/iot"
configs = { 
"fs.azure.account.auth.type": "CustomAccessToken",
"fs.azure.account.custom.token.provider.class": spark.conf.get("spark.databricks.passthrough.adls.gen2.tokenProviderClassName")
}

spark.sql("""
  CREATE TABLE iot2
  USING DELTA
  LOCATION '{}'
""".format(location))

```

### SQLによる確認

まずは、権限をもったパーティション

```:python

%sql
select * from iot2
where cca2='AD'

```

成功します。

![](.media/スクリーンショット%202020-11-25%20220011.png)


次に権限をあたえていないパーティション
```:python

%sql
select * from iot2
where cca2='CA'

```

失敗します。

![](.media/スクリーンショット%202020-11-25%20220204.png)