---
title: Azure Synapse Pipeline（Data Factory を含む） でweb activity の結果をBlobに書き込む
tags:
  - Azure
  - AzureDataLake
  - AzureDataFactory
  - AzureBLOBStorage
  - AzureSynapseAnalytics
private: false
updated_at: '2022-12-23T19:56:56+09:00'
id: be4bb1b7ce5d0c5baf09
organization_url_name: null
slide: false
---
## はじめに

Azure Data lake Storage Gen2 には、Blob / Data Lake のREST APIの口があるので、pipelineからMSI認証でデータを書き込んでみる

## モチベーション

copyアクティビィでRESTをソースに処理ができますが、たまにうまくパースされないレスポンスを返すサービスがあり、なんとかデータレイクに書き込む方法を探していました。

そこで以下の記事を見つけたのですが、認証方法に改善の余地があるので、MSI認証で通す方法を検討しました。
https://geekshangout.com/azure-data-factory-how-to-save-web-activity-to-blob-storage/

## Put Blob ※Blob APIの利用

今回は、https://www.e-stat.go.jp/api/ からデータを取得してblobを書き込んでみようと思います。

参考：https://learn.microsoft.com/ja-jp/rest/api/storageservices/put-blob


### 準備

利用するのは、Synapse（マネージドVnet有効、データレイクにはファイアウォール設定あり）です。

![2022-12-23-19-06-30.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/2532b7bb-aee3-20a2-8e69-e0f87fa674bd.png)


![2022-12-23-19-07-24.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/8a36779c-6cf0-38d3-065a-3961dd393f8e.png)



まずは、e-statのサイトでAPI登録を行い、APP_IDを入手します。

1.会員登録後、マイページからAPI機能(アプリケーションID発行)をクリックします。

![2022-12-23-19-02-05.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/66d35d18-e503-cf52-e1c1-9ec8952464e5.png)


2.APPの情報を入力すると、APPIDが払い出されます。

![2022-12-23-19-03-35.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/29f451e4-8af7-7b72-5916-b960abf50263.png)


3.https://www.e-stat.go.jp/api/api-dev/how_to_use のページでサンプルがあるので、こちらをそのまま使います。URLパラメータにAPPIDを入れれば簡単に取得できる仕組みです。

![2022-12-23-19-04-59.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/63901b17-a2f2-7f71-c5f2-106cc2fa808a.png)


### 手順

1.PL_putblob_qiitaという名称で、パイプラインを作成します。{}ボタンから以下のコードを貼り付けます。

![2022-12-23-19-18-19.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/4a1cc0db-f5e5-8acb-6699-70a3860bd5c4.png)



``` json:

{
    "name": "PL_putblob_qiita",
    "properties": {
        "activities": [
            {
                "name": "put blob",
                "type": "WebActivity",
                "dependsOn": [],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": false,
                    "secureInput": false
                },
                "userProperties": [],
                "typeProperties": {
                    "url": {
                        "value": "https://@{pipeline().parameters.accountName}.blob.core.windows.net/@{pipeline().parameters.containerName}/@{pipeline().parameters.path}",
                        "type": "Expression"
                    },
                    "connectVia": {
                        "referenceName": "AutoResolveIntegrationRuntime",
                        "type": "IntegrationRuntimeReference"
                    },
                    "method": "PUT",
                    "headers": {
                        "x-ms-blob-type": "BlockBlob",
                        "x-ms-version": "2021-06-08"
                    },
                    "body": {
                        "value": "@pipeline().parameters.body",
                        "type": "Expression"
                    },
                    "authentication": {
                        "type": "MSI",
                        "resource": "https://storage.azure.com/"
                    }
                }
            }
        ],
        "parameters": {
            "accountName": {
                "type": "string"
            },
            "containerName": {
                "type": "string"
            },
            "path": {
                "type": "string"
            },
            "body": {
                "type": "object"
            }
        },
        "annotations": []
    }
}

```

貼り付けると今回作ったものが再現されます。

![2022-12-23-19-09-59.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/5f588be3-5194-3a4c-2f3e-c9aadabc3c9f.png)


パラメータの内容は以下のようになっています。

- accountName: ストレージアカウント名
- containerName: コンテナの名前
- path: ファイルパス
- body: 書き込みたい内容

設定はこんな感じ

![2022-12-23-19-10-29.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/440facd0-4e29-70bb-c1ee-7d853d7da93f.png)


urlはパラメータからblobエンドポイント上のファイル名を作成するようになっています。

```

https://@{pipeline().parameters.accountName}.blob.core.windows.net/@{pipeline().parameters.containerName}/@{pipeline().parameters.path}

```


MSI認証でREST APIを実行するときは実行したい操作を管理しているリソースのエンドポイントのURLをリソースとして入力します。
今回はhttps://storage.azure.com/ でした。

参考：https://learn.microsoft.com/ja-jp/rest/api/storageservices/authorize-with-azure-active-directory#use-oauth-access-tokens-for-authentication

2.次にe-statsからデータを取得するためのパイプラインを作成し、webアクティビティを配置します。
内容は先ほど確認したサンプルURLを入れています。

![2022-12-23-19-15-49.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/8b759d9e-8ca3-6b7c-a2b1-8d58a2ec81a7.png)


3.デバッグすると、出力結果からレスポンスの内容が確認できます。


![2022-12-23-19-20-10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/8320e651-a7db-6d30-03bb-e58b79652fef.png)


GET_STATS_DATAという部分に結果が出ています。


![2022-12-23-19-20-19.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/c0080a15-339c-19f3-10ff-5105a0ef20f7.png)


4.先ほど作成したPL_putblob_qiitaを実行するように構成します。

![2022-12-23-19-20-47.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/2231a721-b9c8-245c-46b3-0bdc1620c477.png)

5.パラメータのbodyを動的なコンテンツで構成します。

![2022-12-23-19-21-30.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/a843d423-f203-af1c-86f5-06642e83c65b.png)


@activity('Web1').output.GET_STATS_DATA と入力してやります。

![2022-12-23-19-22-47.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/36a0679e-6eba-99fa-0ae0-971e10a2ab8f.png)


6.他のパラメータを入力してデバッグします。

![2022-12-23-19-23-52.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/80324fe9-64da-3c92-4aab-a1e0d795973f.png)



7.成功するとblobが書き込まれます。

![2022-12-23-19-24-41.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/acdf8b97-8b93-bded-73db-a222459d22b9.png)


## (供養) ※Data Lake APIの利用

こちらの方法はPipelineでは不適と判断しましたが、学びがあったのでメモだけ残します。

参考：
- https://techcommunity.microsoft.com/t5/azure-paas-blog/how-use-storage-adls-gen2-rest-api-to-upload-file-via-aad-access/ba-p/2108778

Data Lake APIでのファイルの書き込み方法は以下の3ステップで行います

1.ファイルの作成(create)
2.ファイルの書き込み(append)
3.ファイルの書き込みのコミット＝フラッシュ(flush)

2で実際にデータを投入しますが、フラッシュしない限りファイルに反映されません。これが色々と厄介な仕様でした。

フラッシュ時には書き込んだバイト数を計算して、positionパラメータを指定しないと

>{"error":{"code":"InvalidFlushPosition","message":"The uploaded data is not contiguous or the position query parameter value is not equal to the length of the file after appending the uploaded data.

のようなエラーが返ります。今回e-statsからcontents-lengthが取れたので使いましたが、数字は一致せず。。。動的にpositionをとることはpipeline上では難しいという判断にいたりました。


なお、2のappendと同時にフラッシュするっぽいパラメータflush=trueはうまく動作しませんでしたので、私のわかる範囲だとこの3ステップが必須です。

内容は以下に供養します。　　
パイプライン名をPL_create_file_qiitaにして以下のコードを貼り付けて下さい

```json:


{
    "name": "PL_create_file_qiita",
    "properties": {
        "activities": [
            {
                "name": "create path",
                "type": "WebActivity",
                "dependsOn": [],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": false,
                    "secureInput": false
                },
                "userProperties": [],
                "typeProperties": {
                    "url": {
                        "value": "https://@{pipeline().parameters.accountName}.dfs.core.windows.net/@{pipeline().parameters.filesystemName}/@{pipeline().parameters.path}?resource=file",
                        "type": "Expression"
                    },
                    "connectVia": {
                        "referenceName": "AutoResolveIntegrationRuntime",
                        "type": "IntegrationRuntimeReference"
                    },
                    "method": "PUT",
                    "authentication": {
                        "type": "MSI",
                        "resource": "https://storage.azure.com/"
                    }
                }
            },
            {
                "name": "append",
                "type": "WebActivity",
                "dependsOn": [
                    {
                        "activity": "create path",
                        "dependencyConditions": [
                            "Succeeded"
                        ]
                    }
                ],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": false,
                    "secureInput": false
                },
                "userProperties": [],
                "typeProperties": {
                    "url": {
                        "value": "https://@{pipeline().parameters.accountName}.dfs.core.windows.net/@{pipeline().parameters.filesystemName}/@{pipeline().parameters.path}?action=append&position=0",
                        "type": "Expression"
                    },
                    "connectVia": {
                        "referenceName": "AutoResolveIntegrationRuntime",
                        "type": "IntegrationRuntimeReference"
                    },
                    "method": "PATCH",
                    "body": {
                        "value": "@pipeline().parameters.body",
                        "type": "Expression"
                    },
                    "authentication": {
                        "type": "MSI",
                        "resource": "https://storage.azure.com/"
                    }
                }
            },
            {
                "name": "flush",
                "type": "WebActivity",
                "dependsOn": [
                    {
                        "activity": "append",
                        "dependencyConditions": [
                            "Succeeded"
                        ]
                    }
                ],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": false,
                    "secureInput": false
                },
                "userProperties": [],
                "typeProperties": {
                    "url": {
                        "value": "https://@{pipeline().parameters.accountName}.dfs.core.windows.net/@{pipeline().parameters.filesystemName}/@{pipeline().parameters.path}?action=flush&position=@{pipeline().parameters.position}",
                        "type": "Expression"
                    },
                    "connectVia": {
                        "referenceName": "AutoResolveIntegrationRuntime",
                        "type": "IntegrationRuntimeReference"
                    },
                    "method": "PATCH",
                    "headers": {
                        "content-length": {
                            "value": "0",
                            "type": "Expression"
                        }
                    },
                    "body": "",
                    "authentication": {
                        "type": "MSI",
                        "resource": "https://storage.azure.com/"
                    }
                }
            }
        ],
        "parameters": {
            "accountName": {
                "type": "string"
            },
            "filesystemName": {
                "type": "string"
            },
            "path": {
                "type": "string"
            },
            "body": {
                "type": "string",
                "defaultValue": "test"
            },
            "position": {
                "type": "int",
                "defaultValue": 4
            }
        },
        "variables": {
            "respheader": {
                "type": "String"
            }
        },
        "annotations": []
    }
}

```
