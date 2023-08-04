# Data Wrangler for VSCode を試してみる

## Data Wrangler とは

現在パブリックプレビュー中のデータ探索、前処理用のツールです。

![Image from Gyazo](https://i.gyazo.com/b015c7008a092e0813bf71ccda50ec4c.png)

Github のリポジトリに記載のコンセプト訳文:
> Data Wranglerは、パンダコードを自動的に生成し、洞察に満ちた列統計と視覚化を表示する豊富なユーザーインターフェイスを提供することにより、データクリーニングを行うデータサイエンティストの生産性を向上させることを目的としています。

引用元：[Github Repo](https://github.com/microsoft/vscode-data-wrangler#using-data-wrangler)

VSCode の拡張機能があるので、試してみます。

[market place](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.datawrangler)

## 使ってみる

1. まずは拡張機能をインストールします ※Python インストール済みのWin環境です。
    ![Image from Gyazo](https://i.gyazo.com/00f9ec37b79bec6627492382bd62be26.png)
2. **ctrl + P** でVSCode コマンドパレットを呼び出してみます。
    ![Image from Gyazo](https://i.gyazo.com/00f9ec37b79bec6627492382bd62be26.png)
3. **>Open Walkthrough** を起動すると ガイドが立ち上がります。
    ![Image from Gyazo](https://i.gyazo.com/d62113c1812e0fcb36e3e2d8c0b934a5.png)
4. **Step 1 Open Data Wrangler　→ Open file in Data Wrangler** をクリックして、対象のファイルを選択します。
   ![Image from Gyazo](https://i.gyazo.com/197b2bf0b052fa2d1a834338dc2d97c7.png)

   今回は[Azure ML チュートリアル](https://learn.microsoft.com/ja-jp/azure/machine-learning/tutorial-first-experiment-automated-ml) の定期預金申込の予測モデル用データである、[bankmarketing_train.csv](https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv)　を利用します。

5. 初めて機能を利用する場合、　python/jupyter カーネルに接続するための画面が表示されますので、任意の環境を選択します。
   ![Image from Gyazo](https://i.gyazo.com/4a1cce5bc8142d9e421a5f397c81a9a4.png)

6. もしカーネルに必要な（pandasなど）が不足している場合、インストールに進みます。
   ![Image from Gyazo](https://i.gyazo.com/e429287e1595ebe461698ed322f7a808.png)

7. インストールが完了すると、データファイルをロードして、テーブルビューが表示されます。
   ![Image from Gyazo](https://i.gyazo.com/a37dc61557188f028c9ef30105a45b6f.png)

    画面中央では、それぞれの**列ごとの統計情報とレコード**が表示され、左側ペインでは、上から **Operations(処理内容の一覧)**、**Data Summary(テーブル全体の統計情報)**、**Cleaning Steps(行った処理ステップ)** が表示されています。

8. はじめに列を絞り込んでみます。**Select Columns** の処理を一覧から選択すると、列を選択するためのメニューに移動します。
   ![Image from Gyazo](https://i.gyazo.com/9150e4e2f668e48877c5f4924ef3dcc8.png)

9. age(年齢)と、Y(定期預金フラグ)に絞り込んでみました。**Apply** をクリックします。
    ![Image from Gyazo](https://i.gyazo.com/bf52d7f3333ce64ec2898e873f8b07f5.png)

10. 処理結果が表示されます。この状態で一度 **Preview code for all steps** をクリックすると、実施した処理がpandasコードとして生成されていることがわかります。
    ![Image from Gyazo](https://i.gyazo.com/976533166e9869c4b7b01e635f95d2c9.png)

11. 次に、年齢を年代で表現するための列を追加します。Settings で **By Example operation**をチェックしましょう
    ![Image from Gyazo](https://i.gyazo.com/d4f07f6bcf15b24a27ab93336ffeb442.png)

12. Operation の一覧に **New Column by example** が表示されるので、これをクリックします。

    ![Image from Gyazo](https://i.gyazo.com/c7460a61cdde9aec27f54ef96c7cbb23.png)

13. 対象列と追加列名を入力します。

    ![Image from Gyazo](https://i.gyazo.com/ca0ddb73134a498a3ce34164710c9bbf.png)

14. 緑色で表示される例入力欄に値を入れると、規則が予測され、残りの値が自動生成されます。

    ![Image from Gyazo](https://i.gyazo.com/f4ddf5aa503d770c3138aea2d3a49c02.png)

15. pandas 側も式が生成されています。10で割って小数点を丸めたあと10倍して戻すといったところでしょうか。

    ![Image from Gyazo](https://i.gyazo.com/bd720b434b446af1be8f23ba7d9acd1c.png)

16. **Export to Notebook** をクリックすると、生成されたコードを含む ipynb ファイルが生成されます。
    ![Image from Gyazo](https://i.gyazo.com/bb54ca625b24c02d932958c3df94f3be.png)

以上です。簡単なデータ処理は十分のように思いますし、サクサク探索できて結構いい感じのツールでした。ぜひご確認してみてください。
