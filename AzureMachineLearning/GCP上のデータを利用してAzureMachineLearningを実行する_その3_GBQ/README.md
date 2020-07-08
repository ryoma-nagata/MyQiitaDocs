# GCP上のデータを利用してAzureMachineLearningを実行する_その3_GBQ

## 概要

以下の記事のGoogle Big Query (GBQ)での手順です。

## 構成

![](../GCP上のデータを利用してAzureMachineLearningを実行する_その1_まとめ/.media/GBQAML.drawio.svg)

## 手順概要

1. GBQ準備
2. ローカル実験によるテスト
3. AMLのリモート実験
4. GBQ データ削除

## 1.GBQ準備
jupyter notebookで[01_GBQ_Create_Table.ipynb]を実行します。<br>

利用ファイル：
- 01_GBQ_Create_Table.ipynb
- project_folder/サービスアカウントキー作成で出力したjsonファイル

## 2. ローカル実験によるテスト
jupyter notebookで[02_GBQ_ML_Local.ipynb](./source/**02_GBQ_ML_Local**.ipynb)を実行します。<br>

利用ファイル：
- 02_GCS_ML_Local.ipynb
- project_folder/サービスアカウントキーを作成で出力したjsonファイル

## 3. AMLのリモート実験

jupyter notebookで[03_GCS_Azure_ML_Remote.ipynb](./source/03_GBQ_Azure_ML_Remote.ipynb)を実行します。<br>

利用ファイル：
- 03_GCS_Azure_ML_Remote.ipynb
- project_folder/サービスアカウントキーを作成で出力したjsonファイル
- project_folder/train_breast_cancer.py

## 4.GBQ準備

課金が発生するので、不要な場合は、jupyter notebookで[04_GBQ_Delete_Data.ipynb](./source/02_GCS_ML_Local.ipynb)を実行して削除します。

