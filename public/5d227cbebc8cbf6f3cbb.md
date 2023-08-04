---
title: Azure Data Factory が信頼されたサービスリストに登録されました。
tags:
  - Microsoft
  - Azure
  - Storage
  - KeyVault
  - DataFactory
private: false
updated_at: '2020-10-16T09:52:58+09:00'
id: 5d227cbebc8cbf6f3cbb
organization_url_name: null
slide: false
---
#速報
2019/10/25時点の情報です

#投票機能から速報がありました
[Static IP ranges for Data Factory and add ADF to list of Trusted Azure Services](https://feedback.azure.com/forums/270578-data-factory/suggestions/20565967-static-ip-ranges-for-data-factory-and-add-adf-to-l?tracking_code=284de9653bdd03400fc151143955e7cd)

>We want to share the great news that ADF has been added to the list of “Trusted Azure service” for Azure Key Vault and Azure Storage (blob & ADLS Gen2)!! Now you can enable “Allow trusted Microsoft services” on AKV and Azure Storage for better network security, and your ADF pipelines will continue to run. There are two caveats to pay attention to: (1) In order for ADF to be considered as one of the “Trusted Microsoft services” you need to use MSI to authenticate to AKV or Azure Storage in the linked service definition, and (2) If you are running Mapping Data Flow activity – “Trusted Azure service” is not supported for Data Flow just yet and we are working hard on it.
What is coming up? Here are the additional enhancements we are making for better network security:
- Static IP range for Azure Integration Runtime so that you can whitelist specific IP ranges for ADF as part of firewall rules. ETA is next few months.
- Support service tag for ADF
We will provide an update as soon as these enhancements becomes available. Please stay tuned and thank you for using ADF!

翻訳
>Azure Key VaultとAzure Storage（blob＆ADLS Gen2）の「信頼されたAzureサービス」のリストにADFが追加されたという素晴らしいニュースを共有したいです!!これで、ネットワークセキュリティの向上のためにAKVおよびAzure Storageで「信頼されたMicrosoftサービスを許可する」を有効にでき、ADFパイプラインが引き続き実行されます。注意すべき2つの注意事項があります。（1）ADFを「信頼されたMicrosoftサービス」の1つと見なすには、MSIを使用してリンクされたサービス定義でAKVまたはAzure Storageを認証する必要があります。データフローマッピングアクティビティを実行している場合–「信頼されたAzureサービス」はデータフローでまだサポートされていないため、一生懸命取り組んでいます。

>何が近づいていますか？ネットワークセキュリティを改善するために行っている追加の機能強化は次のとおりです。
-Azure Integration Runtimeの静的IP範囲。これにより、ファイアウォールルールの一部としてADFの特定のIP範囲をホワイトリストに登録できます。 ETAは今後数か月です。
-ADFのサポートサービスタグ

>これらの拡張機能が利用可能になり次第、更新プログラムを提供します。お待ちください、ADFをご利用いただきありがとうございます！

#信頼されたサービスリストとは
Azure上でNWセキュリティ保護をした場合に特定のサービスからのアクセスに対してはパススルーさせる機能です。
https://docs.microsoft.com/ja-jp/azure/storage/common/storage-network-security#trusted-microsoft-services

#実際に試してみた

## 前提

以下の記事のようにADFにBLOBのデータアクションができるロール（BLOBデータ共同作成者など）のRBACロールの付与が必要となります。
https://qiita.com/ryoma-nagata/items/b09ffe2b1208cfed506d#adls%E3%81%AE%E8%A8%AD%E5%AE%9A

###信頼されたサービスに許可がないとはじかれます
Storage
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/89fea74f-0a1d-0ddc-fb18-fc7aae9cb122.png)
Data Factory
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/95a3965f-a082-12c5-3b74-ee1bf2dc434a.png)


###Azure サービス許可だけをチェックしてサービスエンドポイントは無効の状態にするとDataFactoryからアクセスができるように！

Storage
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/046ea9eb-3dd9-c853-8b59-f98ea797cdfb.png)

Data Factory
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/19bb2215-daf6-646b-8072-0106640d5819.png)

#注意
DataFactoryの認証はアクセスキーだと信頼されたサービス扱いになりません。
Managed Identity方式で認証する場合のみこのような動作になります。
逆に考えると、キーを悪用して他社のDataFactoryからとられるという心配はなくなってます。

※現在はそうという話です。今後はADFがどのような認証方法でも信頼されたサービス扱いになるかもしれません。

#今後について
DataFactoryがセキュアにデータストアにアクセスする方法は上記のように随時開発が進んでいます。
ADFに対する静的IPの設定や、NSGで利用できるサービスタグへの対応、Mapping Data FlowのPrivate Network内での利用などが進んでいるようです。



