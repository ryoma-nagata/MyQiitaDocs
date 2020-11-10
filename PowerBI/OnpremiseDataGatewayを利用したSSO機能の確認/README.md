# On-premise Data Gatewayを利用したSSO機能と行レベルセキュリティの確認

## はじめに

2020/11時点の情報です。

On-premise Data Gateway（以下、GW）を利用したAzure SQL に対するSSO(シングルサインオン)機能を試してみたいと思います。

[Azure SQLに対するシングルサインオン](https://docs.microsoft.com/ja-jp/power-bi/connect-data/service-azure-sql-database-with-direct-connect#single-sign-on)
[Power BI のゲートウェイ用シングル サインオン (SSO) の概要](https://docs.microsoft.com/ja-jp/power-bi/connect-data/service-gateway-sso-overview)

## Power BI SeirviceのSSO機能を活用するケース

Power BI ServiceでSSO機能を利用すると、Direct Queryで接続しているデータソースに対して、Power BI Serviceのログインユーザによる認証が実施されます。

これを活用することで、ログインしたユーザ情報を用いて、ユーザに見せるデータ範囲を制御する、いわゆる「**行レベルセキュリティ機能**」をデータベース側で実装することが可能です。

### 行レベルセキュリティ

ユーザにより、表示させるデータを絞り込む機能です。
DB側でフィルタをかけるか、Power BI データセット側でフィルタをかけるか2パターンあります。
1. Power BI データセット側での制御 [参考](https://docs.microsoft.com/ja-jp/power-bi/admin/service-admin-rls)
2. DB側での制御 [参考](https://docs.microsoft.com/ja-jp/sql/relational-databases/security/row-level-security?view=sql-server-ver15)

Power BI データセット側での制御のみを実施する場合、直接データソースに接続してロールを作成するユーザにはRLSがかけられません。
DB側での制御のみだと、ImportモードでPower BI データセット上にデータを取り込んだ場合のRLSがかけられません。

それぞれの特徴を考慮して設計をする必要があります。
例：  
- 利用者はPower BIデータセットにしかアクセスしないので、「直接データソースに接続してロールを作成するユーザ」にはデータ全件が見えてもいい→1のみ
- 利用者は自分でPower BI Desktopを使ってデータソースに接続する→2のみ


## 手順概要

2つのADユーザ(全てのデータ閲覧可能、)を利用して、検証します。

- 管理者・・・Azure SQLの管理者・GWの管理者・Azure SQL上のデータは全て閲覧可能
- 利用者・・・Power BI Service上でレポートを作る人。Azure SQL上のデータは自分のロール(sales1)のデータのみ閲覧可能

手順は以下の流れ
1. Azure SQLの準備
2. セキュリティポリシー設定
3. GWのインストール
4. Power BI レポートの作成、発行
5. GWの設定、SSOの有効化

### 1. Azure SQLの準備

適当なDBを作成します。
[クイック スタート:Azure SQL Database の単一データベースを作成する](https://docs.microsoft.com/ja-jp/azure/azure-sql/database/single-database-create-quickstart?tabs=azure-portal)

AD管理者を設定します。
[Azure AD 管理者をプロビジョニングする (SQL Database)](https://docs.microsoft.com/ja-jp/azure/azure-sql/database/authentication-aad-configure?tabs=azure-powershell#provision-azure-ad-admin-sql-database)


### 2. セキュリティポリシー設定

AD管理者でログインして、以下を実施(masterではなく、DBに対して実行)

```sql

--利用者をDBにアクセスできるようにする
CREATE USER [pbi-readuser@xxx.onmicrosoft.com] FROM EXTERNAL PROVIDER
GO
--ロールに作成、利用者を追加
CREATE ROLE sales1 AUTHORIZATION [dbo]
GO
EXEC sp_addrolemember 'Sales1' ,'pbi-readuser@xxx.onmicrosoft.com';  

--テスト用テーブル作成

CREATE TABLE Sales  
    (  
    OrderID int,  
    SalesRep sysname,  
    Product varchar(10),  
    Qty int  
    );  

INSERT INTO Sales VALUES (1, 'Sales1', 'Valve', 5);
INSERT INTO Sales VALUES (2, 'Sales1', 'Wheel', 2);
INSERT INTO Sales VALUES (3, 'Sales1', 'Valve', 4);
INSERT INTO Sales VALUES (4, 'Sales2', 'Bracket', 2);
INSERT INTO Sales VALUES (5, 'Sales2', 'Wheel', 5);
INSERT INTO Sales VALUES (6, 'Sales2', 'Seat', 5);
-- 6件が表示
SELECT * FROM Sales;

-- ロールに権限付与
GRANT SELECT ON Sales TO Sales1


-- セキュリティポリシーの作成
CREATE SCHEMA Security;  
GO  
 
-- サンプルクエリを改変して、ロールをチェックするように
CREATE FUNCTION Security.fn_securitypredicate(@SalesRep AS sysname)  
    RETURNS TABLE  
WITH SCHEMABINDING  
AS  
    RETURN 
	SELECT 
		1
	AS fn_securitypredicate_result
	where 1=IIF(ORIGINAL_LOGIN( ) = '管理者のID@nxxx.onmicrosoft.com',1,ISNULL(IS_ROLEMEMBER(@SalesRep , ORIGINAL_LOGIN()),0))
 ; 

-- テーブルに適用
CREATE SECURITY POLICY SalesFilter  
ADD FILTER PREDICATE Security.fn_securitypredicate(SalesRep)
ON dbo.Sales  
WITH (STATE = ON);  

-- セキュリティポリシーへアクセス権を付与
GRANT SELECT ON security.fn_securitypredicate TO [sales1];  

--テスト。フィルタが効くことを確認
EXECUTE AS USER =  'pbi-readuser@xxx.onmicrosoft.com';  
SELECT * FROM Sales;
REVERT;  

```

3. GWのインストール

