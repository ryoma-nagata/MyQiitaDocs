# Power BI Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法

<!-- TOC -->

- [Power BI Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法](#power-bi-desktop%e3%81%ab%e3%81%a6%e3%83%86%e3%83%bc%e3%83%96%e3%83%ab%e3%81%ae%e3%83%87%e3%83%bc%e3%82%bf%e3%82%92%e3%83%86%e3%82%ad%e3%82%b9%e3%83%88%e3%83%95%e3%82%a1%e3%82%a4%e3%83%abcsvtsv%e3%81%ab%e3%82%a8%e3%82%af%e3%82%b9%e3%83%9d%e3%83%bc%e3%83%88%e3%81%99%e3%82%8b%e6%96%b9%e6%b3%95)
  - [概要](#%e6%a6%82%e8%a6%81)
  - [利用ツール](#%e5%88%a9%e7%94%a8%e3%83%84%e3%83%bc%e3%83%ab)
  - [DAX Query結果をエクスポートする方法](#dax-query%e7%b5%90%e6%9e%9c%e3%82%92%e3%82%a8%e3%82%af%e3%82%b9%e3%83%9d%e3%83%bc%e3%83%88%e3%81%99%e3%82%8b%e6%96%b9%e6%b3%95)
    - [手順](#%e6%89%8b%e9%a0%86)
    - [DAX Studioのエクスポート設定について](#dax-studio%e3%81%ae%e3%82%a8%e3%82%af%e3%82%b9%e3%83%9d%e3%83%bc%e3%83%88%e8%a8%ad%e5%ae%9a%e3%81%ab%e3%81%a4%e3%81%84%e3%81%a6)
  - [複数のテーブルを一括でエクスポートする方法](#%e8%a4%87%e6%95%b0%e3%81%ae%e3%83%86%e3%83%bc%e3%83%96%e3%83%ab%e3%82%92%e4%b8%80%e6%8b%ac%e3%81%a7%e3%82%a8%e3%82%af%e3%82%b9%e3%83%9d%e3%83%bc%e3%83%88%e3%81%99%e3%82%8b%e6%96%b9%e6%b3%95)

<!-- /TOC -->


## 概要

DAX Studioにて、30,000行をPower BI Desktop上のテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法を共有します。



Power BI には、ビジュアルからデータをエクスポートすることも可能ですが、下記のようにレコード数に制約があります。

>   -   **Power BI Desktop** および **Power BI サービス**で**インポート モード レポート**から *.csv* ファイルにエクスポートできる最大行数は、30,000 です。

>アプリケーションで**インポート モード レポート**から *.xlsx* ファイルにエクスポートできる最大行数は、150,000 です。

引用元：[視覚エフェクトの作成に使用されたデータをエクスポートする](https://docs.microsoft.com/ja-jp/power-bi/visuals/power-bi-visualization-export-data#limitations-and-considerations)



本手順で、上記制約を超えたレコード数のデータをエクスポートが可能となり、下記のような活用ができそうです。

-   Power BI Dataflowに接続して、データをエクスポート
-   Power BI Premiumであれば、データモデルに接続し、データをエクスポート



## 利用ツール　

-   Power BI Desktop
-   DAX Studio



## DAX Query結果をエクスポートする方法

### 手順

1.  Power BI Desktopに、ファイルを開く。必要に応じてでデータをインポート。


![](.media/Power%20BI%20DesktopにてテーブルのデータをCSVファイルにエクスポートする方法/image-20200522100017941.png)



2.  DAX Studioにて、レポートに接続する。

![image-20200522100307786](.media/Power%20BI%20DesktopにてテーブルのデータをCSVファイルにエクスポートする方法/image-20200522100307786.png)



3.  DAX Studioにて、"Output"を"File"に設定し、下記のクエリを実施。

![image-20200522100519636](.media/Power%20BI%20DesktopにてテーブルのデータをCSVファイルにエクスポートする方法/image-20200522100519636.png)

コードサンプル：

```DAX
EVALUATE
    {テーブル名}
```

実例：

```DAX
EVALUATE
    SalesFact
```



4.  エクスポートしたファイルを確認（本手順では、ヘッダー行を除き、1,260,752行。）。

![image-20200522100811540](.media/Power%20BI%20Desktopにてテーブルのデータをテキストファイルにエクスポートする方法/image-20200522100811540.png)



### DAX Studioのエクスポート設定について

1.  "ファイル"タブを選択します

![image-20200522101800751](.media/Power%20BI%20Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法/image-20200522101800751.png)



2.  "Options"→"Standard"→"Custom Export Format"にて、エクスポートする形式を変更可能。

![image-20200522101814263](.media/Power%20BI%20Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法/image-20200522101814263.png)





![image-20200522101907622](.media/Power%20BI%20Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法/image-20200522101907622.png)



## 複数のテーブルを一括でエクスポートする方法

1.  "Advanced"→"Export Data"を選択。

![image-20200522110340626](.media/Power%20BI%20Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法/image-20200522110340626.png)



2.  "CSV Files"を選択。

![image-20200522110416709](.media/Power%20BI%20Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法/image-20200522110416709.png)



3.  データ保存先、ファイル形式を選択し、"Next >"を選択。

![image-20200522110450960](.media/Power%20BI%20Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法/image-20200522110450960.png)



4.  エクスポート対象のテーブルを選択。

![image-20200522110549458](.media/Power%20BI%20Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法/image-20200522110549458.png)



5.  ファイルがエクスポートされていることを確認

![image-20200522110734674](.media/Power%20BI%20Desktopにてテーブルのデータをテキストファイル（CSV、TSV）にエクスポートする方法/image-20200522110734674.png)