## はじめに

Purviewから簡単にDatabricksのスキャンができるPreviewが来ていたので試してみました。

[Microsoft Purview で Azure Databricks に接続して管理する (プレビュー)](https://learn.microsoft.com/ja-jp/azure/purview/register-scan-azure-databricks)

### 注意事項

2023/01/19 時点の確認結果です。

また、一部リソース名などからエンドポイントを推定できる箇所があるかもしれませんが、デモ用の一次的な環境で作成してます。

## 取得対象

![](.image/2023-01-19-15-03-33.png)

現時点では、スコープスキャンができないのですべて取得される想定ですが、
hive_metastoreの対象は以下からdemo_devを確認したいと思います。

![](.image/2023-01-19-10-58-42.png)

salesはマネージドテーブルです。

![](.image/2023-01-19-10-58-12.png)

movies はアンマネージドテーブルとしてtype=EXTERNALとなっています。

![](.image/2023-01-19-10-57-52.png)

## 準備

### Purview用のセルフホステッド統合ランタイムの構成

AzureVMを利用しています。ちなみにDSVMイメージを使うと色々楽でした。

1.JDK 11のインストール

数秒で完了

![](.image/2023-01-19-10-09-39.png)

2.Visual Studio 2012 Update 4 の Visual C++ 再頒布可能パッケージのインストール

数秒で完了

![](.image/2023-01-19-10-14-45.png)

3.セルフホステッド統合ランタイムのインストールと構成

[セルフホステッド統合ランタイムを作成して共有する](https://learn.microsoft.com/ja-jp/azure/purview/manage-integration-runtimes)に基づいてインストールから構成を進めました。

Purview上でランタイムを作成

![](.image/2023-01-19-10-17-26.png)

![](.image/2023-01-19-10-17-56.png)

キーを取得

![](.image/2023-01-19-10-18-24.png)

VM側でキーを設定して接続

![](.image/2023-01-19-10-25-41.png)

Purview側から見てセルフホステッド統合ランタイムがオンラインになっています

![](.image/2023-01-19-10-27-30.png)

### 個人用アクセストークンとクラスター作成

DatabricksへのPurviewからの認証には個人用アクセストークンを利用するので、これを発行します。

1. トークン発行

![](.image/2023-01-19-10-22-17.png)

![](.image/2023-01-19-10-22-24.png)

![](.image/2023-01-19-10-22-42.png)

発行したトークンをKey Vaultに登録しておきます。

![](.image/2023-01-19-10-23-37.png)

2. クラスター作成

手順など割愛しますが、低スペックのシングルノードクラスターを作成しました。

![](.image/2023-01-19-11-13-51.png)

### Purview用のKey Vaultの構成

トークンの保管されたKey Vaultに対してPurviewを接続しておく必要があります。

keyvault接続

![](.image/2023-01-19-10-24-13.png)


![](.image/2023-01-19-10-24-42.png)

## 手順 

では実際にDatabricksをスキャンしてみます。手順は冒頭のリンクに従っています。

### Databricks ソースの登録

まずは、ソース登録です。

1.ソース登録画面からDatabricksを選択します。

![](.image/2023-01-19-10-29-24.png)

2.対象のワークスペースを選択すれば完了です。

![](.image/2023-01-19-10-29-57.png)


### スキャンの実行 マウントポイントなし

最初の実行では、省略可能なマウントポイントはなしで実施してみます。

スキャン作成画面から資格情報を作成して、KeyVaultに保管した個人用アクセストークンを使えるようにしておきます。

![](.image/2023-01-19-10-30-53.png)

クラスターIDをクラスター情報から取得します。

![](.image/2023-01-19-10-32-07.png)

スキャン設定はこのようになりました。この設定で実行してみます。

![](.image/2023-01-19-10-31-55.png)

### 結果確認 マウントポイントなし

マウントポイントなしでの実行確認です。およそ2分超で完了しました

databricksワークスペースと関連するhive server , hive DBが登録されています。

![](.image/2023-01-19-10-51-03.png)

Databricksのアセットはこのようになります

![](.image/2023-01-19-10-51-59.png)

![](.image/2023-01-19-10-52-07.png)

関連はなし
![](.image/2023-01-19-10-52-18.png)

hive serverに遷移します。

![](.image/2023-01-19-10-52-48.png)

![](.image/2023-01-19-10-52-57.png)

Hive DBが関連として登場し、スキーマが表示されています。

![](.image/2023-01-19-10-53-07.png)

取得対象としたdemo_devのhive dbに移動します

![](.image/2023-01-19-10-54-15.png)

![](.image/2023-01-19-10-54-22.png)

![](.image/2023-01-19-10-54-30.png)

外部テーブルであるmovies

![](.image/2023-01-19-10-54-48.png)

![](.image/2023-01-19-10-55-01.png)

![](.image/2023-01-19-10-55-09.png)

![](.image/2023-01-19-10-55-23.png)

![](.image/2023-01-19-10-55-31.png)

マネージドテーブルであるsales


![](.image/2023-01-19-10-55-51.png)

![](.image/2023-01-19-10-56-00.png)

![](.image/2023-01-19-10-56-07.png)

![](.image/2023-01-19-10-56-18.png)

現時点ではアンマネージドテーブルとは特に差異がありませんね。


### スキャンの実行 マウントポイントあり

次にマウントポイントを指定してみます。

マウント情報は以下のように確認し、moviesテーブルが保管されている/mnt/dlsanalyticsdemo/datalakeを使ってみます。

![](.image/2023-01-19-11-01-26.png)

スキャン設定は以下の通り

![](.image/2023-01-19-11-02-42.png)



### 結果確認 マウントポイントあり

アンマネージドテーブルであるmoviesには系列が追加されました。マネージドテーブルには特に変更なしです。

![](.image/2023-01-19-14-01-21.png)


### スキャンの実行 Unity Catalog有効の場合

対象のワークスペースをunity catalogを適用してdata explorerでunity catalogのテーブルも表示されるようにしてみます。

![](.image/2023-01-19-15-02-18.png)

![](.image/2023-01-19-15-02-40.png)

この状態でスキャンを実行するとどうなるか。


### 結果確認 Unity Catalog有効の場合

取り込みアセット数が変わっていないので、やはりUnity Catalog配下のデータは取得対象外ですね

![](.image/2023-01-19-15-08-05.png)

実際に、Hiveテーブルなどのカタログ追加は発生していませんでした。

たとえばこのテーブルは

![](.image/2023-01-19-15-09-24.png)

カタログで検索しても表示されません。

![](.image/2023-01-19-15-09-55.png)

## 所見

アンマネージドテーブルのストレージとの関係がとれるのは結構うれしいですね。これであればDataFactoryとの連携が取れるのではと思います（リソースセットではなくパスの種類なので多少限定されると思いますが）

一方で、マウントする形式はUnity Catalog配下では推奨されなくなるものという認識なので、Unity Catalogとの連携が早く来るといいですね


## その他気になった点の確認結果

### クラスタの自動起動

クラスタ休止中にスキャンが走るとどうなるか確認しました。

きちんと自動起動しています。この分スキャン時間は延びるかとは思いますが、セルフホステッド統合ランタイムなのでコストも大丈夫そう

![](.image/2023-01-19-14-54-16.png)



### マネージドテーブルのリネージ

だめもとでマウントポイントにDatabricksマネージドストレージ上のrootを入れて動かしてみましたが、リネージは取れませんでした。
これについては別に良いかなという感じ（マネージドストレージへのリネージとってもしょうがないので）




