## はじめに

Databrikcs に管理されたVnetを利用することは、Vnet管理不要というメリットがあるが、この場合、ファイアウォールの背後のストレージにアクセスするためのサービスエンドポイントや、プライベートエンドポイントの設置といったことができません。

![](https://camo.qiitausercontent.com/d6bc0138768f48df01a63f2d1453cedc48da10a7/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3238313831392f61373165623133382d333733652d643737342d313338652d6538326363336130653961342e706e67)

引用：https://qiita.com/ryoma-nagata/items/66c48dd2a86956c0d00d

## ねらい

このような構成をすることでアクセスさせます。ネットワークの素人なので雰囲気です

![](.image/2023-03-03-14-47-29.png)


## 手順

### 準備

以下を用意しておきます。

- Azure Databricks 
- Azure Data Lake Storage Gen 2 ※パブリックアクセス無効

![](.image/2023-03-03-14-50-38.png)


### 1. ネットワークを構成する

1. [仮想ネットワークのピアリング](https://learn.microsoft.com/ja-jp/azure/databricks/administration-guide/cloud-configurations/azure/vnet-peering)に従って、構成します。

![](.image/2023-03-03-14-52-12.png)

![](.image/2023-03-03-14-51-42.png)

2.接続したvnet にプライベートエンドポイントを作成します。

参考：https://learn.microsoft.com/ja-jp/azure/storage/common/storage-private-endpoints#creating-a-private-endpoint

![](.image/2023-03-03-14-53-21.png)

3.プライベートDNSゾーンをリンクしていることを確認します。

![](.image/2023-03-03-14-53-59.png)

また、DNSゾーンではデータレイクを示すAレコードの登録を確認します

![](.image/2023-03-03-14-54-50.png)

4.Private DNS Resolver を作成します。

![](.image/2023-03-03-14-56-10.png)

5.受信エンドポイントを作成してIPを確認しておきます。

![](.image/2023-03-03-14-56-27.png)

### 2. Databricksのクラスター初期化スクリプトを構成し、アクセスを確認する

1. 適当なクラスターを作成し、アカウントキーを使用したアクセスを試してみます。
![](.image/2023-03-03-14-57-47.png)

```python:pyspark

key = 'アカウントキー情報'

spark.conf.set("fs.azure.account.key.<ストレージ名>.dfs.core.windows.net",key)

dbutils.fs.ls("abfss://<コンテナ名>@<ストレージ名>.dfs.core.windows.net/")

```


アクセスはブロックされ、プライベートエンドポイントで名前解決ができていないことがわかります。


![](.image/2023-03-03-15-08-19.png)


2. 管理コンソールで Global Init scripts で **+追加**

![](.image/2023-03-03-15-10-34.png)

3.名前とコードを入力し **Enable** を確認して **Add** をクリック

```bash: dns setting

#!/bin/bash
mv /etc/resolv.conf /etc/resolv.conf.orig
echo nameserver 10.1.2.68 | sudo tee --append /etc/resolv.conf

```
4.クラスターを再起動し、再度実行を確認します。

アクセスできました。

![](.image/2023-03-03-15-18-40.png)

## 注意・課題

SQL ウェアハウスのDNS設定は調査中のです。