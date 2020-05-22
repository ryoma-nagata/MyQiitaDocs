# PowerBIの.pbix,.pbit,.pbidsについて

## はじめに

### 参考記事

https://powerbi.microsoft.com/en-us/blog/power-bi-desktop-october-2019-feature-summary/#pbids

https://docs.microsoft.com/ja-jp/power-bi/connect-data/desktop-data-sources#using-pbids-files-to-get-data

https://powerbi.tips/2019/10/make-pbids-files/

## それぞれの違い

| # | 対象  |説明  |
|---------|---------|---------|
|1|pbix|基本の拡張子です。レポート、接続情報、(importの場合、データ+モデル。Direct Queryの場合モデルのみ)が含まれます         |
|2|pbit|テンプレートファイルの拡張子です。レポートとモデルが含まれます。データは含まれません|
|3|pbids|接続情報のみが含まれます|

## pbix

[Power BI のチュートリアル](https://docs.microsoft.com/ja-jp/power-bi/create-reports/sample-datasets)をご参照ください。

## pbit

参考記事
[Power BI Desktop のレポート テンプレートを作成する](https://docs.microsoft.com/ja-jp/power-bi/create-reports/desktop-templates)

### 作成方法

#### 手順

1. データの入手
2. レポート作成
3. テンプレートをエクスポート

##### データの入手

財務サンプルのExcelファイルを[ダウンロード](https://docs.microsoft.com/ja-jp/power-bi/create-reports/sample-financial-download)します。

##### レポート作成

Power BI を起動して、Excelデータを取得します。

![](.\image\pbit01.png)

対象ファイルを開いて、「financials」データを読み込みます。

![](.\image\pbit02.png)

適当なレポートを作成します。

![](.\image\pbit03.png)

このままテンプレートを作成することも可能ですが、工夫をしてみます。Excelファイルパスをパラメータ化してみます。

まずはPower Query エディターを開きます。
![](.\image\pbit03-1.png)


現在のファイルパスをメモしておきます。

![](.\image\pbit03-1-1.png)

パラメータを作成します。

![](.\image\pbit03-2.png)

適当な名前を入力して、種類をテキストにしておきます。

![](.\image\pbit03-3.png)

先ほどメモするために開いた、データソースのパスをパラメータの名称に変更します。完了したら閉じて適用を選択します。

![](.\image\pbit03-4.png)


ではpbitファイルをエクスポートしてみましょう。

ファイルタブを開きます。

![](.\image\pbit04.png)

エクスポートします。
![](.\image\pbit05.png)


#### 利用方法

先ほど作成したFinancialSample.pbit（という名前で作成しました。）を開いてみると、パラメータの内容を求められます。
Excelのデータをおいているパスを入力することで、指定されたファイルからレポートテンプレートにデータが読み込まれます。

![](.\image\pbit06.png)

#### テンプレートファイルはこちら

### pbids




#### 作成方法

#### 利用方法

