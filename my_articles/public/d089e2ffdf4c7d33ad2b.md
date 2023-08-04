---
title: Power BIの配置パイプライン機能を試してみた
tags:
  - Microsoft
  - BI
  - PowerBI
private: false
updated_at: '2020-08-27T21:11:03+09:00'
id: d089e2ffdf4c7d33ad2b
organization_url_name: null
slide: false
---
## はじめに

### 配置パイプラインとは

Power BIのコンテンツのうち、レポート、データセット、ダッシュボードを別のワークスペースに一括配置してくれる機能です。  
この機能により、開発環境→テスト環境→運用環境をといったステージ構成を簡単に準備し、リリース作業をスムーズに実施することが可能です。

![image](https://docs.microsoft.com/ja-jp/power-bi/create-reports/media/deployment-pipelines-overview/deployment-pipelines.png)

[デプロイ パイプラインの概要](https://docs.microsoft.com/ja-jp/power-bi/create-reports/deployment-pipelines-overview)


## 利用手順

[デプロイ パイプラインの使用を開始する](https://docs.microsoft.com/ja-jp/power-bi/create-reports/deployment-pipelines-get-started)にしたがって実施していきます。

### 前提条件

>- Power BI の Pro ユーザーである 
>- Premium 容量を持つ組織に属している
>- 新しいワークスペース エクスペリエンスの管理者である

https://docs.microsoft.com/ja-jp/power-bi/create-reports/deployment-pipelines-get-started#accessing-deployment-pipelines


### 手順概要

1. 事前準備
1. デプロイ パイプラインの作成
1. デプロイ パイプラインへのワークスペースの割り当て
1. 空のステージにデプロイする
1. データセット ルールを作成する
1. 1 つのステージから別のステージへのコンテンツのデプロイ

### 1. 事前準備

３つのDB（開発、テスト、運用）を準備します。

今回は以下のようなsql serverを準備しました。

![servers.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/f7265d04-0203-a28e-ffed-467785daa432.png)


データベース内容は**AdventureWorksLT** を利用しています。

![db_sample.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/d9e7a40a-dbea-7805-3fac-a906d7d157ed.png)

適当なレポートを作成して、Premium ライセンスを保有したテナントのPower BI ワークスペースに発行します。  
※開発環境のデータだとわかるように、pbi-pipeline-devの中のデータには**d-** とつけました。同様にテスト環境には**t-** とつけています。

![report.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/5c2e95d6-c1fa-800e-54a0-abcd7367619e.png)


### 2. デプロイ パイプラインの作成

では、デプロイパイプラインを構成してみます。

タブから「**配置パイプライン**」→「**パイプラインの作成**」の順にクリックします。

![pipeline1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/58eafd0f-afd6-4124-11d1-19b339ff5a15.png)


名前を設定します。

![pipe2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/99bfe723-4402-28f1-ca08-cd1e3185c0db.png)


最初の段階ではパイプラインは環境が割り当てられていない状態です。

![pipe3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/42c32b0b-5d7e-f766-63db-b8528c81f468.png)


### 3. デプロイ パイプラインへのワークスペースの割り当て

次に、「**ワークスペースの割り当て**」をクリックすると、指定のワークスペースを環境に割り当てられます。

![pipe4.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/bdc3e16d-a469-a8d0-ff02-02635271ad8e.png)


開発環境を割り当てました。

![pipe5.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/156dd5bf-fe9a-7c1a-625c-2a54351f9d5a.png)


**割り当てられるワークスペースについて**

>- ワークスペースは、新しいワークスペース エクスペリエンスである必要があります。
>- このワークスペースの管理者である必要があります。
>- このワークスペースが、他のパイプラインに割り当てられていないことを確認します。
>- ワークスペースは、 premium 容量に存在する必要があります。
>- パイプライン ステージに Power BI サンプルを含むワークスペースを割り当てることはできません。

https://docs.microsoft.com/ja-jp/power-bi/create-reports/deployment-pipelines-get-started#workspace-assignment-limitations


### 4. 空のステージにデプロイする

「**テストへの配置**」をクリックすると、コピーが開始されます。

![pipe6.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/3f74c18e-c885-d9ee-f02b-f9cf97275a6e.png)


「テスト」、「実稼働」にコピーが完了すると、それぞれのコンテンツが確認できます。  
それぞれのステージは、最初に割り当てたワークスペースに[TEST]などが付与された名称で新しいワークスペースが作成されます。

![pipe7.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/8febcaa7-1080-1313-cf0e-315c525a633f.png)


### 5. データセット ルールを作成する

さて、DBはそれぞれの環境ごとに用意していました。  
環境ごとにデータセットが参照するDBを変更したいと思います。

デプロイの設定ボタンをクリックします。

![pipe8.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/c70060a0-e517-6c70-f3d8-c474e0ff34ff.png)


参照先を変更したいデータセットを選択します。

![pipe9.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/d69e6a56-1049-02e4-cb63-75834d174ba2.png)


「**規則の追加**」をクリックします。

![pipe10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/f9a4135a-ef5e-94a4-b6ee-b91c818577e0.png)


DBの参照先を「**その他**」で置き換えます。  
内容は手入力可能です。  
ここでは、サーバ名を変更しました。ちなみに、パラメータの変更もこちらで可能です。

![pipe11.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/00d5fe64-20ee-a5c3-fb0c-53bca17e3049.png)


### 6. 1 つのステージから別のステージへのコンテンツのデプロイ

「**テストへの配置**」を実行するとルールを適用したうえで置き換えが開始されます。

![pipe12.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/48ed300a-8f50-bcb0-dedb-9f67b4ca6309.png)


資格情報が異なるので、テスト環境のデータセットに移動して、テスト環境のデータセットの資格情報を再セットしましょう。  
この時点で、デプロイのルールが適用されていることがわかります。

![pipe13.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/5b357c41-8f65-e77d-ac50-5c248f21b74b.png)


再設定後、テスト環境では、テスト環境用のDBが参照されるようになります。

![pipe14.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/d192d995-0a0f-07a4-18ad-f8fd27a72a23.png)


運用環境でも同様の確認が可能です。

![pipe15.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/5cbcf54b-221b-f291-7932-011683d05456.png)


## 補足

### 名称変更について

コンテンツの名称を変えた場合も反映されるようです。

![pipe16.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/f54ccd9b-6a9c-e737-5417-0a3710baa72b.png)


### 削除について

開発環境でコンテンツを削除した場合、他のステージへ削除の反映はされないようでした。

ただし、差分の検出することは可能です。※このパイプラインのUI上で削除することはできません。

![pipe17.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/ce463c96-8c72-18f1-d146-3ac45da4c5f3.png)
