# GCP上のデータを利用してAzureMachineLearningを実行する_その2_GCS

## 概要

以下の記事のGoogle Cloud Storage(GCS)での手順です。
[GCP上のデータを利用してAzureMachineLearningを実行する_その1_まとめと環境設定](../GCP上のデータを利用してAzureMachineLearningを実行する_その1_まとめと環境設定/README.md)


## 構成

![](../GCP上のデータを利用してAzureMachineLearningを実行する_その1_まとめと環境設定/.media/GCSAML.drawio.svg)

## 手順概要

1. GCS準備
2. ローカル実験によるテスト
3. AMLのリモート実験

## 1.GCS準備
jupyter notebookで[01_GCS_Create_Bucket.ipynb]を実行します。<br>

利用ファイル：
- 01_GCS_Create_Bucket.ipynb
- project_folder/サービスアカウントキー作成で出力したjsonファイル
- data/breast_cancer.csv

## 2. ローカル実験によるテスト
jupyter notebookで[02_GCS_ML_Local.ipynb](./source/02_GCS_ML_Local.ipynb)を実行します。<br>

利用ファイル：
- 02_GCS_ML_Local.ipynb
- project_folder/サービスアカウントキーを作成で出力したjsonファイル

## 3. AMLのリモート実験

jupyter notebookで[03_GCS_Azure_ML_Remote.ipynb](./source/03_GCS_Azure_ML_Remote.ipynb)を実行します。<br>

利用ファイル：
- 03_GCS_Azure_ML_Remote.ipynb
- project_folder/サービスアカウントキーを作成で出力したjsonファイル
- project_folder/train_breast_cancer.py

