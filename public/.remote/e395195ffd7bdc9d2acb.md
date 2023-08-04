---
title: Azure Analysis ServicesをAzure Data Factory で更新する
tags:
  - Microsoft
  - Azure
  - ETL
  - AnalysisServices
  - DataFactory
private: false
updated_at: '2020-07-09T17:26:57+09:00'
id: e395195ffd7bdc9d2acb
organization_url_name: null
slide: false
---
#概要
下記参考リンクを元にAzure Analysis Services(以下、AAS)をAzure Data Factory(以下、ADF) で更新するパイプラインを構成します。

##参考リンク
https://github.com/furmangg/automating-azure-analysis-services

#手順
 1. AAS,ADFのリソースをデプロイする
 2. サンプルモデル作成
 2. 権限設定
 3. Pipeline作成
 4. 動作確認
 
## AAS,ADFのリソースをデプロイする
### AAS
クイックスタート参照
https://docs.microsoft.com/ja-jp/azure/analysis-services/analysis-services-create-server

### ADF
クイックスタート参照
https://docs.microsoft.com/ja-jp/azure/data-factory/quickstart-create-data-factory-portal#create-a-data-factory

## サンプルモデル作成
下記コードをSSMSから実行してください

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/b1df5876-0101-db04-3eab-a8c64335e4e6.png)


<details>
<summary>**クリックで展開します**</summary>
<div>

```XMLA:

{
  "create": {
    "database": {
      "name": "SAMPLE_AS",
      "compatibilityLevel": 1500,
      "model": {
        "name": "モデル",
        "culture": "ja-JP",
        "tables": [
          {
            "name": "T_SAMPLE_1",
            "columns": [
              {
                "name": "AMT_1",
                "dataType": "int64",
                "sourceColumn": "AMT_1"
              },
              {
                "name": "AMT_2",
                "dataType": "int64",
                "sourceColumn": "AMT_2"
              }
            ],
            "partitions": [
              {
                "name": "Partition",
                "dataView": "full",
                "source": {
                  "type": "m",
                  "expression": [
                    "let",
                    "    ソース = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText(\"i45WMjQwUNIBkQZKsTrRSkZwLoRvjOBDBEyQBCAipsgiQKFYAA==\", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [AMT_1 = _t, AMT_2 = _t]),",
                    "    変更された型 = Table.TransformColumnTypes(ソース,{{\"AMT_1\", Int64.Type}, {\"AMT_2\", Int64.Type}})",
                    "in",
                    "    変更された型"
                  ]
                }
              }
            ],
            "measures": [
              {
                "name": "MEASURE_1",
                "expression": [
                  "",
                  "SUM(T_SAMPLE_1[AMT_1])"
                ]
              },
              {
                "name": "MEASURE_2",
                "expression": [
                  "",
                  "SUM(T_SAMPLE_1[AMT_2])"
                ]
              }
            ]
          },
          {
            "name": "T_SAMPLE_2",
            "columns": [
              {
                "name": "AMT_3",
                "dataType": "int64",
                "sourceColumn": "AMT_3"
              },
              {
                "name": "AMT_4",
                "dataType": "int64",
                "sourceColumn": "AMT_4"
              }
            ],
            "partitions": [
              {
                "name": "Partition",
                "dataView": "full",
                "source": {
                  "type": "m",
                  "expression": [
                    "let",
                    "    ソース = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText(\"i45WMjIwMFDSUTJUitWJVjKGcIzAHBMIxxjMMYVwTMAcMwjHVCk2FgA=\", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type text) meta [Serialized.Text = true]) in type table [AMT_3 = _t, AMT_4 = _t]),",
                    "    変更された型 = Table.TransformColumnTypes(ソース,{{\"AMT_3\", Int64.Type}, {\"AMT_4\", Int64.Type}})",
                    "in",
                    "    変更された型"
                  ]
                }
              }
            ],
            "measures": [
              {
                "name": "MEASURE_3",
                "expression": [
                  "",
                  "SUM(T_SAMPLE_2[AMT_3])"
                ]
              },
              {
                "name": "MEASURE_4",
                "expression": [
                  "",
                  "SUM(T_SAMPLE_2[AMT_4])"
                ]
              }
            ]
          }
        ],
        "annotations": [
          {
            "name": "ClientCompatibilityLevel",
            "value": "600"
          }
        ]
      }
    }
  }
}




```

</div>

</details>



## 権限設定
SSMSでAASに接続します
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/1e084162-c315-3e0d-1037-92fd3fb33a38.png)

サーバ名を右クリックでプロパティ→セキュリティ→追加の順にクリック
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/824735cf-13a0-6954-b69f-fff485c6cc78.png)

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/3ad67435-d962-7055-7def-17d7204779c8.png)

ADFのプロパティ上にある、マネージドIDテナント、マネージドIDアプリケーションIDを利用して
「app:<マネージドIDアプリケーションID>@<マネージドIDテナント>」のような文字列を用意します。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/3019df2f-2cf9-1df2-15c2-c02085325ed4.png)

SSMSに戻り、手動エントリに入力後、追加→OKの順にクリック

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/30350142-0569-0ba0-f55b-cc5a054154ce.png)

### Pipeline作成
ADF上で、「ProcessAzureAS MSI」という名称のパイプラインを作成し、下記コードをcode欄から貼り付けます。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/1261967d-c367-5093-8f11-6637e1e1ac58.png)


<details>
<summary>**クリックで展開します**</summary>
<div>

```JSON:

{
    "name": "ProcessAzureAS MSI",
    "properties": {
        "activities": [
            {
                "name": "UntilRefreshComplete",
                "type": "Until",
                "dependsOn": [
                    {
                        "activity": "FilterToCurrentRefresh",
                        "dependencyConditions": [
                            "Succeeded"
                        ]
                    }
                ],
                "userProperties": [],
                "typeProperties": {
                    "expression": {
                        "value": "@not(equals(activity('GetAzureASRefreshStatus').output.status,'inProgress'))",
                        "type": "Expression"
                    },
                    "activities": [
                        {
                            "name": "GetAzureASRefreshStatus",
                            "type": "WebActivity",
                            "dependsOn": [
                                {
                                    "activity": "Wait30Seconds",
                                    "dependencyConditions": [
                                        "Succeeded"
                                    ]
                                }
                            ],
                            "policy": {
                                "timeout": "7.00:00:00",
                                "retry": 0,
                                "retryIntervalInSeconds": 30,
                                "secureOutput": false
                            },
                            "userProperties": [],
                            "typeProperties": {
                                "url": {
                                    "value": "@concat('https://',pipeline().parameters.Region,'.asazure.windows.net/servers/',pipeline().parameters.Server,'/models/',pipeline().parameters.DatabaseName,'/refreshes/',activity('FilterToCurrentRefresh').output.Value[0].refreshId)",
                                    "type": "Expression"
                                },
                                "method": "GET",
                                "authentication": {
                                    "type": "MSI",
                                    "resource": "https://*.asazure.windows.net"
                                }
                            }
                        },
                        {
                            "name": "Wait30Seconds",
                            "type": "Wait",
                            "dependsOn": [],
                            "userProperties": [],
                            "typeProperties": {
                                "waitTimeInSeconds": 30
                            }
                        }
                    ],
                    "timeout": "7.00:00:00"
                }
            },
            {
                "name": "StartProcessingAzureAS",
                "type": "WebActivity",
                "dependsOn": [],
                "policy": {
                    "timeout": "7.00:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": false
                },
                "userProperties": [],
                "typeProperties": {
                    "url": {
                        "value": "@concat('https://',pipeline().parameters.Region,'.asazure.windows.net/servers/',pipeline().parameters.Server,'/models/',pipeline().parameters.DatabaseName,'/refreshes')",
                        "type": "Expression"
                    },
                    "method": "POST",
                    "body": {
                        "Type": "Full",
                        "CommitMode": "transactional",
                        "MaxParallelism": 10,
                        "RetryCount": 2
                    },
                    "authentication": {
                        "type": "MSI",
                        "resource": "https://*.asazure.windows.net"
                    }
                }
            },
            {
                "name": "IfFailed",
                "type": "IfCondition",
                "dependsOn": [
                    {
                        "activity": "UntilRefreshComplete",
                        "dependencyConditions": [
                            "Succeeded"
                        ]
                    }
                ],
                "userProperties": [],
                "typeProperties": {
                    "expression": {
                        "value": "@equals(activity('GetAzureASRefreshStatus').output.status,'failed')",
                        "type": "Expression"
                    },
                    "ifTrueActivities": [
                        {
                            "name": "ThrowErrorOnFailure",
                            "type": "WebActivity",
                            "dependsOn": [],
                            "policy": {
                                "timeout": "7.00:00:00",
                                "retry": 0,
                                "retryIntervalInSeconds": 30,
                                "secureOutput": false
                            },
                            "userProperties": [],
                            "typeProperties": {
                                "url": {
                                    "value": "@string(activity('GetAzureASRefreshStatus').output)",
                                    "type": "Expression"
                                },
                                "method": "GET"
                            }
                        }
                    ]
                }
            },
            {
                "name": "GetAzureASRefreshes",
                "type": "WebActivity",
                "dependsOn": [
                    {
                        "activity": "StartProcessingAzureAS",
                        "dependencyConditions": [
                            "Succeeded"
                        ]
                    }
                ],
                "policy": {
                    "timeout": "7.00:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": false
                },
                "userProperties": [],
                "typeProperties": {
                    "url": {
                        "value": "@concat('https://',pipeline().parameters.Region,'.asazure.windows.net/servers/',pipeline().parameters.Server,'/models/',pipeline().parameters.DatabaseName,'/refreshes')",
                        "type": "Expression"
                    },
                    "method": "GET",
                    "body": {
                        "Type": "Full",
                        "CommitMode": "transactional",
                        "MaxParallelism": 10,
                        "RetryCount": 2
                    },
                    "authentication": {
                        "type": "MSI",
                        "resource": "https://*.asazure.windows.net"
                    }
                }
            },
            {
                "name": "FilterToCurrentRefresh",
                "type": "Filter",
                "dependsOn": [
                    {
                        "activity": "GetAzureASRefreshes",
                        "dependencyConditions": [
                            "Succeeded"
                        ]
                    }
                ],
                "userProperties": [],
                "typeProperties": {
                    "items": {
                        "value": "@json(activity('GetAzureASRefreshes').output.Response)",
                        "type": "Expression"
                    },
                    "condition": {
                        "value": "@greaterOrEquals(item().startTime,addseconds(activity('StartProcessingAzureAS').output.startTime,-30))",
                        "type": "Expression"
                    }
                }
            }
        ],
        "parameters": {
            "TenantID": {
                "type": "String"
            },
            "SubscriptionID": {
                "type": "String"
            },
            "Region": {
                "type": "String"
            },
            "Server": {
                "type": "String"
            },
            "DatabaseName": {
                "type": "String"
            }
        },
        "folder": {
            "name": "Azure AS"
        },
        "annotations": []
    },
    "type": "Microsoft.DataFactory/factories/pipelines"
}



```

</div>

</details>

##動作確認

debugをクリックすると処理パラメータの入力ができるので入力して実行（OK）します。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/8970004d-4ba2-46b6-2a2e-f7eb894c95af.png)

###パラメータの確認方法
 - Tenant ID:上記ADFのテナントと同様です。 
 - Subscription:下記画像参照
 - Region:東日本ならjapaneast
 - Server:下記画像参照
 - DatabaseName:サンプルならadventureworks

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/fb262259-7de9-74a5-849a-f0f561c3de60.png)


実行完了
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/27f79d2e-ba0f-6450-dfb0-19174e68e3e7.png)


#補足
AASのファイアウォールを設定する場合、ADFのAzure IRのIP範囲下記で確認してホワイトリストに登録しましょう。
https://docs.microsoft.com/ja-jp/azure/data-factory/azure-integration-runtime-ip-addresses

# 追記

Firewallの範囲を絞りたいときは、Self-Hosted IRを利用して、IRが稼働するサーバのPublic IPをFire Wallに登録しましょう（2020/7/9 動作確認済み）
