## はじめに

[](https://techcommunity.microsoft.com/t5/azure-data-factory-blog/orchestrate-and-operationalize-synapse-notebooks-and-spark-job/ba-p/3724379)

## 準備

synapse側の準備をしておきます。

[サーバーレス Apache Spark プールを作成する](https://learn.microsoft.com/ja-jp/azure/synapse-analytics/get-started-analyze-spark#create-a-serverless-apache-spark-pool) を参考にSpark Poolを作成しておきます。

![](.image/2023-01-27-08-30-25.png)

notebookを作成します。どんな内容でもいいですが、今回はナレッジセンターから Azure Open Datasets を利用するサンプルを使います。

![](.image/2023-01-27-08-26-43.png)

![](.image/2023-01-27-08-27-41.png)

![](.image/2023-01-27-08-27-55.png)

![](.image/2023-01-27-08-28-08.png)

![](.image/2023-01-27-08-28-46.png)

今回は Data Factory からnotebookを実行するわけですが、その際にdata lakeへの読み書きはData Factory の権限で実行されます。
必要に応じて、利用するストレージにData Factory に ストレージ Blob データ共同作成者などの権限を振ります。

![](.image/2023-01-27-09-28-03.png)

Synapse Workspace の権限で実行したい場合はマネージドIDを利用したSpark Session 構成をするのですが、ADF からの実行ではうまくいきませんでした。

![](.image/2023-01-27-09-19-41.png)

## 手順

### Data Factory からの接続の構成

冒頭のURLの手順に従います。

1.Synapse Studio 上で Data Factory を Synapse コンピューティングオペレーター、および、成果物ユーザーロールに追加します。

![](.image/2023-01-27-08-33-54.png)

![](.image/2023-01-27-09-04-59.png)

2.Spark notebook内では、特別な構成がない場合、

3.Data Factory Studio上でリンクサービスを作成します。

リンクサービスのタブをコンピューティングに変更すると Azure Synapse Analytics が表示されます。

![](.image/2023-01-27-08-31-42.png)

ワークスペースを選択して作成します。

![](.image/2023-01-27-08-34-48.png)

作成完了したら発行しておきます。

![](.image/2023-01-27-08-35-38.png)

### Synapse Workspace が パブリックの場合（Azure サービスを許可する状態も含む）

このように、 Synapse Workspace にファイアウォールがかかっていないような状況でのテストからはじめてみます。

![](.image/2023-01-27-09-12-52.png)

1.パイプラインを構成します。

ノートブックアクティビティを配置します。

![](.image/2023-01-27-08-36-03.png)

配置後、対象ノートブックのあるワークスペースを設定し、

![](.image/2023-01-27-08-36-35.png)

現時点だと一覧がうまく読み込めませんでしたが、動的なコンテンツの追加から直接入力することにします

![](.image/2023-01-27-08-57-59.png)

ノートブック名を入力し、あとは省略してしまいます。ちなみに開くをクリックすると Synapse Studio 別タブで開きました

![](.image/2023-01-27-08-59-19.png)

4.実行確認します。

デバッグ実行してみます。Spark Pool の起動に数分かかるはずです。

![](.image/2023-01-27-09-56-54.png)

Synapse Studio からはApache Spark アプリケーションの実行が確認できます。

![](.image/2023-01-27-09-57-36.png)

成功しました。

![](.image/2023-01-27-10-10-40.png)


### Synapse Workspace が ファイアウォール設定済

ここから少し実践的に Synapse Workspace にファイアウォール設定をします。私のクライアントIPからしか接続できなくしました。

![](.image/2023-01-27-09-58-39.png)


そのまま実行するとエラーになります。Data Factory が接続に利用するAzure統合ランタイムはIPが特定できないためです。

![](.image/2023-01-27-10-04-35.png)

結論から言うと、現時点では、セルフホステッド統合ランタイムおよびManaged Vnetの利用はできませんでした。

セルフホステッド統合ランタイムはリンクサービス内で候補になりません。

![](.image/2023-01-27-10-38-36.png)

後者の[Managed Vnet](https://learn.microsoft.com/ja-jp/azure/data-factory/managed-virtual-network-private-endpoint) の利用を試してみます。

1.Managed Vnet Azure IRを構成する

Data Factory 上で 新しい統合ランタイムをセットアップします。

![](.image/2023-01-27-10-00-04.png)

Azureを選択

![](.image/2023-01-27-10-00-19.png)

仮想ネットワークを有効化

![](.image/2023-01-27-10-00-37.png)

作成

![](.image/2023-01-27-10-00-54.png)

2.マネージドプライベートエンドポイントを作成します。

![](.image/2023-01-27-10-01-49.png)

Synapse Analytics を選択後、サブリソースをdevで作成します。

![](.image/2023-01-27-10-02-33.png)

Azure Portal 上で Synapse Workspace からプライベートエンドポイント接続セクションにて承認します。

![](.image/2023-01-27-10-03-30.png)

コメントはなんでもよし

![](.image/2023-01-27-10-03-46.png)

Data Factory 上からも承認状態の更新が確認できるまで待ちます。

![](.image/2023-01-27-10-09-54.png)

3.Data Factoryのリンクサービスで統合ランタイムを先ほど作成したものに変更します。

![](.image/2023-01-27-10-05-49.png)

4.実行します。

が、失敗します。

![](.image/2023-01-27-10-20-09.png)

現時点では Azure Synapse Analytics (Artifacts)のリンクサービスはManaged Private Endpointに対応していないようでした。（対応していれば、マネージドプライベートエンドポイントの情報が出ます。）

![](.image/2023-01-27-10-19-36.png)