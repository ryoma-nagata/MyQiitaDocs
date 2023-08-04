## はじめに


[Power BI 共有データセットを基づいて改ページ調整されたレポートを作成する](https://learn.microsoft.com/ja-jp/power-bi/paginated-reports/report-builder-shared-datasets) の通り、ページ分割されたレポート(Paginated Report)では、Power BI Datasetをソースにすることができます。

しかし、以下の対応データソースページに記載の制限事項を考慮する必要があります。

![](.image/2023-01-19-15-52-35.png)

![](.image/2023-01-19-15-53-02.png)

引用：https://learn.microsoft.com/ja-jp/power-bi/paginated-reports/paginated-reports-data-sources


## 準備

1 XMLA エンドポイントの設定確認

私の環境ではPower BI Premium Per Capacity ではなく、Premium Per User環境を使っているので、テナント設定のページの Premium Per Userのデータセットのワークロード設定を読取 or 読み取り、書き込みの状態にしておく必要があります。

![](.image/2023-01-19-15-55-16.png)

2 XMLAエンドポイントの確認

対象のデータセットが存在するワークスペースにて、設定->Premiumから確認します

![](.image/2023-01-19-16-03-49.png)

## 手順

1.Power BI Report Builder を起動して、Azure Analysis Services を選択します。

![](.image/2023-01-19-16-04-11.png)

2.Build を選択します。

![](.image/2023-01-19-16-04-45.png)

3.サーバー名にコピーした XMLA エンドポイントの値を入れます。

![](.image/2023-01-19-16-05-51.png)

4.データベースを選択しようとするとサインインが走るので、サインインしてデータベースを選択します。

![](.image/2023-01-19-16-07-55.png)

5.Credentials タブにて「 Do not use credentials 」をチェックしておきます。

これは冒頭の対応データソースページの案内にしたがっています。これがないと、 Report Builder 内のデータセットの追加がうまくいきません。

![](.image/2023-01-19-16-10-35.png)



うまくいかないときのエラー

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/9ec2e33d-905d-25cf-facf-953625919681.png)

あとは、通常のデータセットに接続した差異の手順で続ければOKです。


## その他参考

https://learn.microsoft.com/ja-jp/power-bi/enterprise/service-premium-connect-tools#connecting-to-a-premium-workspace
