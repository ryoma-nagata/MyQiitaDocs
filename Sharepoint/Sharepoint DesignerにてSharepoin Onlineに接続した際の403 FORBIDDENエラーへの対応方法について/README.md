# Sharepoint DesignerにてSharepoin Onlineに接続した際の403 FORBIDDENエラーへの対応方法について


<!-- TOC -->

- [Sharepoint DesignerにてSharepoin Onlineに接続した際の403 FORBIDDENエラーへの対応方法について](#sharepoint-designer%e3%81%ab%e3%81%a6sharepoin-online%e3%81%ab%e6%8e%a5%e7%b6%9a%e3%81%97%e3%81%9f%e9%9a%9b%e3%81%ae403-forbidden%e3%82%a8%e3%83%a9%e3%83%bc%e3%81%b8%e3%81%ae%e5%af%be%e5%bf%9c%e6%96%b9%e6%b3%95%e3%81%ab%e3%81%a4%e3%81%84%e3%81%a6)
  - [概要](#%e6%a6%82%e8%a6%81)
  - [手順](#%e6%89%8b%e9%a0%86)
  - [参考リンク](#%e5%8f%82%e8%80%83%e3%83%aa%e3%83%b3%e3%82%af)

<!-- /TOC -->

## 概要

SharePoint Designerを、下記のエラーが表示がされたのですが、後述のリンク記事を参考に"Microsoft SharePoint Designer 2013 (KB2817441) 32 ビット版 Service Pack 1"を適応したところ解決したことを共有します。



>403 FORBIDDEN403 FORBIDDEN403 FORBIDDEN403 FORBIDDEN403 FORBIDDEN

![image-20200522173125115](.media/README/image-20200522173125115.png)





Microsoft 365の"ツールおよびアドイン"からインストールした場合、同様のエラーになってしまうため注意が必要です。



Microsoft 365の"ツールおよびアドイン"からインストールした場合、同様のエラーになってしまうため注意が必要です。

![image-20200522174648142](.media/README/image-20200522174648142.png)





## 手順

1.  [リンク](https://www.microsoft.com/ja-jp/download/details.aspx?id=42015)から、"Microsoft SharePoint Designer 2013 (KB2817441) 32 ビット版 Service Pack 1"をダウンロードし、既存のSharePoint Designerを更新

![image-20200522173351772](.media/README/image-20200522173351772.png)





2.  SharePointのサイトに接続したことを確認。

![image-20200522174049060](.media/README/image-20200522174049060.png)



## 参考リンク

-   [SharePoint Designerの開く権限がありませんエラーについて](http://sptakesato.blog.fc2.com/blog-entry-15.html)