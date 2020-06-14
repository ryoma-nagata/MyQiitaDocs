# 概要

DAX Studio 2.11.0にてプレビューとして実装されたQuery Builder機能をご紹介します。



GUIによるPivot形式でDAX Queryを記載できる便利な機能です。

>    ![image-20200612113028809](.media/README/image-20200612113028809.png)

引用元：[DAX Studio 2.11.0 Released](https://darren.gosbell.com/2020/06/dax-studio-2-11-0-released/)



下記のことが実施可能なため、開発プロセスにもすぐに組み込めます。

-   ディメンション、メジャーの選択

-   メジャーの作成

-   フィルター処理の実施

-   DAX Queryの出力

    



## 事前準備

### ①DAX Studioを起動後、"ファイル"タブを選択

![image-20200612110712894](.media/README/image-20200612110712894.png)



### ②"Options"→"Advanced"→"Show Query Builder Button"にチェックを入れます。

![image-20200612110750793](.media/README/image-20200612110750793.png)



### ③"Home"タブにある"Query Builder"が表示されていることを確認します。

![image-20200612110855699](.media/README/image-20200612110855699.png)



## 利用手順

### ①Power BI等のモデルに接続します。

![image-20200612111823567](.media/README/image-20200612111823567.png)



### ②"Home"タブにある"Query Builder"を選択します。

![image-20200612111844551](.media/README/image-20200612111844551.png)



### ③表示したい項目を、"Columns/Measures"にドラッグします。

![image-20200612112124375](.media/README/image-20200612112124375.png)



### ④フィルター処理したい項目を、"Filters"にドラッグし、フィルタ条件を選択・入力します。

![image-20200612112232184](.media/README/image-20200612112232184.png)



### ⑤下部にある"Run Query"を選択後、実行結果が表示されたことを確認します。

![image-20200612112356539](.media/README/image-20200612112356539.png)



### ⑥"Edit Query"を選択することで、DAX Queryを出力できます。

![image-20200612112524908](.media/README/image-20200612112524908.png)



以上です。

