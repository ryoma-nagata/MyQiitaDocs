

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



1.  DAX Studioにて、レポートに接続する。


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