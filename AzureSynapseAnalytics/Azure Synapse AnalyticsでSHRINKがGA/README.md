# Azure Synapse AnalyticsでSHRINK DBがGA

## 概要

Azure Synapse AnalyticsはSQL DWというブランド名だったころから、Shrink DBをサポートしていませんでしが、今月のUpdateで一般提供されたようです。

## SHRINK DBってなに?

SQL Serverを運用されている方はご存知かと思いますが、SQL Serverのデータ保存領域は確保されたディスク容量(①)と、実際の利用(②)が別々に管理されます。

通常、テーブルの増大(②)に伴ってディスクの確保領域(①)は自動拡張されます。

しかし、利用に応じて確保されたディスク容量(①)が増えたあと、テーブル削除などで実際の利用(②)が減ると、実際には使っていないのにディスク容量を確保している状態（①>>②）が生まれます。

ディスクの確保領域を減らしたい場合、SHRINK DBというコマンドを実行して、使われていない確保領域(①)を解放することで、①≒②のような状態にする必要があります。

Azure Synapse Analyticsでも同様の仕様があり、**テーブルは削除したはずなのに、ディスクの確保領域により課金が発生する**ため、一部の利用者の間では問題となっていました。  
> [ツールは適材適所で使う必要があるという話](https://qiita.com/neppysan/items/286c38d5ad38d8fafe3f)

## リファレンス

[DBCC SHRINKDATABASE (Transact-SQL)](https://docs.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinkdatabase-transact-sql?view=sql-server-ver15)

[リリースノート](https://docs.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/release-notes-10-0-10106-0#july-2020)  
en-usの記事でしか記載がないので注意

[Synapse Analytics Shrink Database](https://techcommunity.microsoft.com/t5/azure-synapse-analytics/synapse-analytics-shrink-database/ba-p/1559522)