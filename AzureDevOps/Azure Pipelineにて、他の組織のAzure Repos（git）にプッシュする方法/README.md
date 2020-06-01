# Azure Pipelineにて、他の組織のAzure Repos（git）にプッシュする方法
<!-- TOC -->

- [Azure Pipelineにて、他の組織のAzure Repos（git）にプッシュする方法](#azure-pipelineにて他の組織のazure-reposgitにプッシュする方法)
  - [概要](#概要)
  - [事前準備](#事前準備)
  - [手順](#手順)

<!-- /TOC -->
## 概要

下記図に示すようにAzure DevOpsの機能であるAzure Pipelineにて、別の組織にあるAzure Reps（Git）にプッシュする方法を共有します。同様の手順にて、異なるテナントのAzure DevOpsに対しても適応可能です。

![image-20200529164940227](.media/README/image-20200529164940227.png)



## 事前準備

-   2つのAzure DevOps組織を作成すること
-   それぞれの組織にて、プロジェクトを作成すること



## 手順

1.  プッシュ先のプロジェクト（上記図における組織B）にて、"User Setting"→"Personal access tokens"を選択。

![image-20200529161716057](.media/README/image-20200529161716057.png)



2.  "New Token"を選択

![image-20200529162049045](.media/README/image-20200529162049045.png)



3.  下記表の通りに入力し、"OK"を選択。表示されるアクセスキーを控えておいてください。

| 項目         | 設定値                  |
| ------------ | ----------------------- |
| Name         | ※わかりやすい名称を入力 |
| Organization | ※プッシュ先組織名を選択 |
| Code         | "Read & wire"をチェック |

![image-20200529162445880](.media/README/image-20200529162445880.png)



4.  "Pipelines"を選択後、"Create Pipeline"を選択。

![image-20200529162624309](.media/README/image-20200529162624309.png)



5.  "Azure Repos Git"を選択。

![image-20200529162706324](.media/README/image-20200529162706324.png)



6.  プッシュするレポジトリーを選択。

![image-20200529162827992](.media/README/image-20200529162827992.png)



7.  "Stater pipeline"を選択。

![image-20200529162852358](.media/README/image-20200529162852358.png)



8.  下記コードを張りつけ、変数の値を設定

| 変数             | 値                          |
| ---------------- | --------------------------- |
| TmpRepoDir       | _repo                       |
| UserName         | ※コミットするユーザー名     |
| OrganizationName | ※プッシュ先の組織名         |
| ProjectName      | ※プッシュ先のプロジェクト名 |
| RepositoryName   | ※プッシュ先のレポジトリー名 |

```yaml
# Starter pipeline
# Start with a minimal pipeline that you can customize to build and deploy your code.
# Add steps that build, run tests, deploy, and more:
# https://aka.ms/yaml
variables:
  TmpRepoDir: _repo
  UserName: ryoma.nagata
  OrganizationName: import-git
  ProjectName: import-git
  RepositoryName: repository-from-otherorganizationname

trigger:
- master

pool:
  vmImage: 'ubuntu-latest'
 
steps:
- script: |
     cd /tmp && rm -rf /tmp/$(TmpRepoDir)
     git -c http.extraheader="AUTHORIZATION: bearer $(System.AccessToken)" clone --mirror $(Build.Repository.Uri) $(TmpRepoDir)
     git -C /tmp/$(TmpRepoDir) push --mirror https://$(UserName):$(secreat_repos)@dev.azure.com/$(OrganizationName)/$(ProjectName)/_git/$(RepositoryName)
  displayName: 'Copy to Azure DevOps Repos'
```



9.  右上にある"Variables"を選択。

![image-20200529163526650](.media/README/image-20200529163526650.png)



10.  "New variable"を選択。

![image-20200529163552752](.media/README/image-20200529163552752.png)



11.  下記の入力を行い、"OK"→"Save"を選択。

| 項目                   | 値                                         |
| ---------------------- | ------------------------------------------ |
| Name                   | secreat_repos                              |
| Value                  | ※3の手順で取得したトークンキーを入力する。 |
| Keep this value secret | チェックする。                             |

![image-20200529163722193](.media/README/image-20200529163722193.png)



12.  右上にある"Save and run"を選択。

![image-20200529163526650](.media/README/image-20200529163526650.png)



13.  適切な入力を行い、"Save and run"を選択。

![image-20200529164104193](.media/README/image-20200529164104193.png)



14.  ジョブ完了後、プッシュ先のレポジトリーにコードが配置されていることを確認。

![image-20200529164304741](.media/README/image-20200529164304741.png)