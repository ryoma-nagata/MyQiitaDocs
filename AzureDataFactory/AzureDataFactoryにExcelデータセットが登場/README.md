# AzureDataFactoryにExcelデータセットが登場

<!-- TOC -->

- [AzureDataFactoryにExcelデータセットが登場](#azuredatafactoryにexcelデータセットが登場)
  - [ADFをいじっていたら見つけました](#adfをいじっていたら見つけました)
  - [早速使ってみた](#早速使ってみた)
    - [手順](#手順)
  - [所感](#所感)

<!-- /TOC -->

## ADFをいじっていたら見つけました


**Excel 使えるようになってる！**

思わず勢いそのままつぶやく
![](.media/01.png)


## 早速使ってみた

### 手順

1. Datasetを作成します。
![](.media/02.png)
2. Excelを置いたStorageのあるLinked Serviceを選択して、Excelを選択します。
![](.media/03.png)
3. ファイル、シートを選びます。
![](.media/04.png)
4. データセットができあがります。
![](.media/05.png)
5. あとはCopy ActivityでDBに書き込むもよし、型を変換してParquetにして保存するもよしです

## 所感

ご質問をいただき「Excel 内のSheetのリストを取得するにはどうするか」を検証しましたが、現時点では難しそうでした。
ただし、公式DocsのほうもまだExcelに関する記載がないので、なにかいい感じの変数があるのかもしれません。
updateに期待です