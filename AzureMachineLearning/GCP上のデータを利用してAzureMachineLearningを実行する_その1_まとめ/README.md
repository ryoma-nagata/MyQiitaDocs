# GCP_BigQueryと接続してAzureMachineLearningを実行する

## 概要

Azure Machine LearningからはAzure SQLをはじめとしたAzure上のデータストアからデータを取り出して機械学習を実施することが可能ですが、今回はGoogle Cloud Platform 上のデータを利用する方法を紹介します。

### 紹介内容について

以下の実行方法を紹介します。
 - GCS上のデータを利用する。
 - GBQ上のデータを利用する。 

#### GCS上のデータを利用する

Azure ML の実験で実行されるpythonスクリプト内で、GCS上のCSVをデータフレーム化して実験を行います

構成イメージ
![](.media/GCSAML.drawio.svg)

#### GBQ上のデータを利用する

Azure ML の実験で実行されるpythonスクリプト内で、GBQに対して発行したクエリ結果をデータフレーム化して実験を行います

構成イメージ
![](.media/GBQAML.drawio.svg)

## 構成

 - 環境設定<br>
 本記事です。
 - Google Cloud Storage 上のデータを利用する
 - Google Big Query 上のデータを利用する

## 環境設定手順

 1. ローカル環境
 2. Azure ML 環境
 3. GCP 環境

### 1. ローカル環境

本記事の紹介内容は下記のバージョンで動作確認済みです。

python version:  3.6.10<br>
google cloud storage version:  1.29.0<br>
azureml version: 1.8.0<br>

新しいanaconda環境作成する場合は、anaconda prompt で下記のコードを実行します。

```bash:anaconda prompt
conda create -n py36gcp python=3.6 jupyter
conda activate py36gcp
jupyter notebook
```

anaconda promptで下記のコードを実行してライブラリをインストールします。

google-cloud
```bash:anaconda prompt
pip install google-cloud    
``` 
google-cloud-storage
```bash:anaconda prompt
!pip install google-cloud-storage
``` 

google-cloud-bigquery
```bash:anaconda prompt
!pip install google-cloud-bigquery
``` 

gcsfs
``` bash:anaconda prompt
!pip install gcsfs
``` 

azureml-sdk<br>

```bash:anaconda prompt
!pip install azureml-sdk
```

azureml-widgets<br>

```bash:anaconda prompt
!pip install azureml-widgets
```

### 2. Azure ML 環境

下記リンクを参考に、Azure ML リソースとComputing Clusterを準備してください

[チュートリアル:Python SDK で初めての ML 実験を作成する](https://docs.microsoft.com/ja-jp/azure/machine-learning/tutorial-1st-experiment-sdk-setup)

[実験を作成して実行する](https://docs.microsoft.com/ja-jp/azure/machine-learning/tutorial-first-experiment-automated-ml#create-and-run-the-experiment)
※「7.次のように [Configure Run](構成の実行) フォームに入力します。」にてComputing Clusterを構成可能です。

### 3. GCP 環境

GCP Projectを用意したら、下記手順でサービスアカウント（アプリケーションがGCPに対して認証するためのアカウント）の準備を実施してください。

#### サービスアカウントを作成
Google Cloud console GUIで下記の手順を行います。
- [プロジェクトを選択] をクリックし、プロジェクト名を選択して、[開く] をクリックします。
- [APIとサービス]＞[認証情報] を選択します。
- [＋認証情報を作成]＞[サービスアカウント]を選択します。
- サービスアカウント名を入力します。
- [作成]を選択します。

#### サービスアカウントキーを作成
Google Cloud　console GUIで下記の手順を行います。
- [APIとサービス]＞[認証情報] を選択します。
- サービスアカウント名を選択します。
- [鍵を追加]＞[新しい鍵を作成]を選択します。
- JSON＞[作成]を選択します。
- サービスアカウントキーの保存先を選択し、[保存]を選択します。
- 例：gbqtoaml-dev-1c3df6d8f54e.json

このファイルは後の作業で利用します。
※運用の際にはキー情報はAzure Key Vaultで管理するのが良いと思います。


#### サービスアカウントへの権限付与
- Cloud Console で[IAM と管理]を選択します。
- [+追加]を選択します。
- サービスアカウントを追加します。
- 「編集者」、「Storage オブジェクト管理者」に割り当てます。

参考リンク： 
サービス アカウントの作成 https://cloud.google.com/iam/docs/creating-managing-service-accounts
サービス アカウントの説明 https://cloud.google.com/iam/docs/understanding-service-accounts

## 次のstep

 - GCS上のデータを利用する。・・・作成中
 - GBQ上のデータを利用する。・・・作成中



## 参考


