## Azure Data StudioのUIがかっちょよくなっていました

![](.media/0000.png)

ログインも求められますが、そこでも新UI

![](.media/000.png)

## SQL Serverをデプロイ？
Deploy ServerでSQL Serverがデプロイできることがわかったので、早速試してみます。

![](.media/02.png)

## 手順

画面の案内に従うだけでした。

### 前提条件

Docker desktopをインストールしておきます。
https://docs.docker.com/docker-for-windows/install/

インストールされていないとエラーメッセージ出てきます。（出てきました）

![](.media/01.png)

あと拡張機能は以下をいれてます。

![](.media/00.png)



### SQL Serverのデプロイ方式を選択

Versionも選べます。2019にしました。

![](.media/03.png)


### コンテナ名とパスワード、portを選択

とりあえず適用なportにしました

![](.media/04.png)

### Python Runtime設定

インストール済みでしたが、新規でインストールもできそう

![](.media/05.png)

### 依存関係を読み込み

jupyterがインストールされました。


![](.media/06.png)

### インストールが終わるとNotebookが生成

なんと今までの情報を元にnotebookが生成されて、順に実行することで、イメージをデプロイする模様

![](.media/07.png)

イメージを取得しています。

![](.media/08.png)

Click hear to connect to SQL Serverが表示されます。そこまで面倒みてくれるのか・・

![](.media/09.png)

### システムデータベースのみのインスタンスが表示されます。

![](.media/10.png)


### DB作成

run Queryから実行します。
インテリゼンスが効いて使いやすいですね。

```sql:sql

CREATE DATABASE TEST

```

### 確認

タブを戻ると、マネジメント画面に表示されます。
私はSSMSに慣れていますが、この管理画面かなりよいのでは。。。

![](.media/11.png)


### コンテナ削除

面倒見がよすぎる.

![](.media/12.png)

terminalが開きます。docker stop などもリンクをクリックすると、ターミナルにペーストされるので、2点実行して、終了です。


## まとめ

簡単に開発環境が作れますね。
イメージのデプロイ先もACIとか使えばリモート開発がはかどるんじゃないでしょうか
そして成功を収めたVSCodeのようにAzure Data Studioは開発と展開がより進むように思います。

がされているようです。SSMSはこの先生きのこれるのか・・・

