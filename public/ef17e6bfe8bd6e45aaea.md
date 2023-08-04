---
title: ' Power BIの複数利用ケースにおけるフィールドの項目（ディメンション項目・メジャー項目）の多言語表示可否に関する調査'
tags:
  - Microsoft
  - PowerBI
  - PowerBIDesktop
  - AnalysisServices
private: false
updated_at: '2020-12-15T17:47:16+09:00'
id: ef17e6bfe8bd6e45aaea
organization_url_name: null
slide: false
---
## 概要
Power BIには、フィールドの項目を多言語で表示可能とする翻訳機能があり、利用できるケースを整理します。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/cad135d7-d861-e51f-f2b7-409348e12d6a.png)

下記表に調査結果を記載します。Power BI Services上で表示する場合にはPower BI Premiumが必須ですが、Power BI Desktopから接続する場合にはPower BI Premiumが必須ではないようです。グローバルでの利用を行う場合には、レポート作成者のためにも、翻訳機能の設定を検討してもいいかもしれません。

| 番号 | ケース                                                         | 翻訳の実施可否 |
| ---- | ------------------------------------------------------------ | -------------- |
| 1    | Power BI Premiumであるワークスペース上で表示した場合   | 〇             |
| 2    | Power BI Premiumでないワークスペース上で表示した場合   | ×              |
| 3    | Power BI Premiumであるワークスペース上のデータセットにPower BI Desktopから接続した場合 | 〇             |
| 4    | Power BI Premiumでないワークスペース上のデータセットにPower BI Desktopから接続した場合 | 〇             |

検証結果の画面と翻訳の設定手順を紹介します。

### 翻訳機能
翻訳機能とは、Analysis Servicesで利用できる機能であり、特定のカルチャー（言語）で項目をマッピングした翻訳ファイルを登録することで、データモデリング利用時に指定の言語で表示で表示できる機能です。Power BIにおいても、XMLAエンドポイント機能が有効になったことで利用できるようになりました。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/59b2ab21-3a13-e26b-2653-2ec2505efc87.png)
引用元：[Analysis Services テーブルモデルでの翻訳 | Microsoft Docs](https://docs.microsoft.com/ja-jp/analysis-services/tabular-models/translations-in-tabular-models-analysis-services?view=asallproducts-allversions)

## 検証結果
### 1. Power BI Premiumであるワークスペース上で表示した場合の結果
翻訳されていることを確認。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/88f60148-972b-8013-9865-fab0f24b3f00.png)

### 2. Power BI Premiumでないワークスペース上で表示した場合の結果
翻訳されないことを確認。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/a85985d5-4480-fea5-b587-7924aa78c272.png)

### 3. Power BI Premiumであるワークスペース上のデータセットにPower BI Desktopから接続した場合の結果
翻訳されていることを確認。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/2a3e34d3-9b33-f0aa-bbef-6ab4f8ca5104.png)

### 4. Power BI Premiumでないワークスペース上のデータセットにPower BI Desktopから接続した場合の結果
翻訳されていることを確認。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/3f23cd30-045a-5839-ca3f-778536e0bd44.png)


## Powre BI Desktopでの実施手順
### 1. Power BIレポートをPower BI Desktopで表示後、"Tabular Editor"を起動。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/cc5c5ea7-647b-85d4-7c08-578a18bf9624.png)

### 2. "Translations"を右クリック後、"New Translation"を選択
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/5e7f559c-beb0-2c7e-6960-b3bdaec4d50d.png)

### 3. "Select Culture"ウィンドウにて、"ja-Jp - Japanese(Japan)" -> "OK"を選択。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/8309aed5-54c2-cb02-9a44-a72c1fc7dc7b.png)

### 4. 翻訳対象の項目を"Tables"にて選択し、"Translated Names"にて適切な項目（例：テスト①）を入力し保存。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/f8763d6c-276c-1094-0215-dc322b1d7d3b.png)

### 5. 項目が翻訳されたことを確認
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/24031/ef6b5bdc-5acc-312e-d1b4-99bfb7a01603.png)

## 備考
特になし。

