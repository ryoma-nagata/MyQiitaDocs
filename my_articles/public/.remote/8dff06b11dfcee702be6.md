---
title: Sharepoint DesignerにてSharepoin Onlineに接続した際の403 FORBIDDENエラーへの対応方法について
tags:
  - Microsoft
  - SharePoint
private: false
updated_at: '2020-05-22T18:21:55+09:00'
id: 8dff06b11dfcee702be6
organization_url_name: null
slide: false
---

## 概要

SharePoint Designerを、下記のエラーが表示がされたのですが、後述のリンク記事を参考に"Microsoft SharePoint Designer 2013 (KB2817441) 32 ビット版 Service Pack 1"を適応したところ解決したことを共有します。



>403 FORBIDDEN403 FORBIDDEN403 FORBIDDEN403 FORBIDDEN403 FORBIDDEN

![image-20200522173125115.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/81598934-e39a-4bca-e7b9-3c75cbc7096c.png)






Microsoft 365の"ツールおよびアドイン"からインストールした場合、同様のエラーになってしまうため注意が必要です。



Microsoft 365の"ツールおよびアドイン"からインストールした場合、同様のエラーになってしまうため注意が必要です。

![image-20200522174648142.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/e30ad89d-ca58-6d39-5780-18581bc7d76b.png)





## 手順

1.  [リンク](https://www.microsoft.com/ja-jp/download/details.aspx?id=42015)から、"Microsoft SharePoint Designer 2013 (KB2817441) 32 ビット版 Service Pack 1"をダウンロードし、既存のSharePoint Designerを更新

![image-20200522173351772.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/e1f423fd-d7da-d49e-57d1-6bb0e829faff.png)






2.  SharePointのサイトに接続したことを確認。

![image-20200522174049060.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/0c562abc-3d42-a4b7-e40b-6326781c8487.png)




## 参考リンク

-   [SharePoint Designerの開く権限がありませんエラーについて](http://sptakesato.blog.fc2.com/blog-entry-15.html)
