### 


データ: 売上

1. 202112(初期landing)
2. 202201(初期landing)
3. 202202+202201

- 販売日
- 注文番号
- 製品ID
- 顧客ID
- 明細金額
- 取り消しフラグ
- 更新日

- landing: csv rundate=
- raw: parquet rundate=
- enrich:
  - 販売：最新データ
  - 製品：履歴データ
  - 顧客：履歴データ
- curated:
  - 販売: 増分更新直近1か月を更新
  - 製品: scd1
  - 顧客: scd2

ディレクトリ構成：

## product 

landing/contoso/product/
- rundate=20220110/product_202201.csv ->full
- rundate=20220210/product_202202.csv ->full

raw/contoso/product/
- rundate=20220110/parquet ->full
- rundate=20220210/parquet ->full

enrich/contoso/product/parquet -> full reflesh

## sales

landing/contoso/sales/
- rundate=20220110/sales_202201.csv ->202112,202201
- rundate=20220210/sales_202202.csv ->202201,202202

raw/contoso/sales/
- rundate=20220110/parquet ->202112,202201
- rundate=20220210/parquet ->202201,202202

enrich/contoso/sales/
- salesYearMonth=202112　※1
- salesYearMonth=202201　※1,2
- salesYearMonth=202202　※2

