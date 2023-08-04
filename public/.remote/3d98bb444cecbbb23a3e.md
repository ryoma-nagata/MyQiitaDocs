---
title: Azure Data Factoryの環境反映パターン【自動（承認付き）、小規模】
tags:
  - Microsoft
  - Azure
  - AzureDataFactory
  - DataFactory
  - 環境反映
private: false
updated_at: '2022-03-28T09:57:56+09:00'
id: 3d98bb444cecbbb23a3e
organization_url_name: null
slide: false
---
## はじめに

Data Factoryの開発環境から本番環境への反映方法についてまとめます。

今回は大規模なDataFactory向けのパターンである、**自動（承認付き）**、**小規模向け**となります。

注意事項：
- Synapse では利用できません。SynapseはARM上に成果物を保持していないため


2022/03時点の情報です。

## 他パターン

[Azure Data Factoryの環境反映パターン【手動、小規模】](https://qiita.com/ryoma-nagata/items/5fa5ef1d7f5f8029cfa4)
[Azure Data Factoryの環境反映パターン【手動、大規模対応】](https://qiita.com/ryoma-nagata/items/fe4b3cce0b5f013b200c)


## 参考記事

[Azure Data FactoryのCI/CDをAzure DevOpsで実装する](https://qiita.com/whata/items/7cad0c01e76d2f22e257#prepost%E3%83%87%E3%83%97%E3%83%AD%E3%82%A4%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88)

[Azure Pipelines リリースを使用して継続的インテグレーションを自動化する](https://docs.microsoft.com/ja-jp/azure/data-factory/continuous-integration-delivery-automate-azure-pipelines)

※今回は従来のリリース方式となるPublishボタンでのパイプライン起動となります。ブランチ戦略、リリース戦略、および運用によって、使い分けてください。

[サンプルの配置前と配置後スクリプト](https://docs.microsoft.com/ja-jp/azure/data-factory/continuous-integration-delivery-sample-script)


## 手順

### 準備

以下のような状態だとします。
#### 開発環境

リンクサービス：

![2022-03-06-11-40-49.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/6f30b750-0893-5675-6ed4-21176843cbe2.png)


データセット：
![2022-03-06-11-41-13.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/ba59d79e-6ecb-a2fd-cac2-e3f967e11701.png)


#### 本番環境

作成した時点のデフォルト状態です。

リンクサービス：

![2022-03-06-11-44-28.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/16b3acb0-1818-d880-8b6b-d923b601c608.png)


データセット：

![2022-03-06-11-44-41.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/8ccc17af-0ac3-c35b-63fb-55f200bea129.png)


### 1. DevOps統合の設定

[Azure Repos Git 統合を使用した作成](https://docs.microsoft.com/ja-jp/azure/data-factory/source-control#author-with-azure-repos-git-integration)を参考に、Data FactoryとDevOpsのgit構成を設定します。

レポジトリの新規作成は今はできないようなので、Azure Repos側で作成します。

![2022-03-08-11-48-49.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/a23ab7c3-0b6a-6bc6-f2aa-16359d422287.png)


**開発済みのADFがある場合にDevOps統合を設定する場合** には、以下のように、既存のリソースのインポートを設定します。今回はすでに作ったものを使うので、これを設定します。
ルートフォルダーもdatafactoryなどのフォルダを指定するのがおすすめです。

![2022-03-08-11-49-45.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/da58dba9-4ff7-f87a-1ec0-f3b287b086b7.png)

設定後の画面では、作業ブランチは適宜作成してください。今回はリソース反映のデモをしたいだけなので、mainで作業します。

![2022-03-08-11-51-59.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/df968a80-65bb-93ef-05d7-7c3fd3eb41b9.png)


設定が済んだ段階で、Azure Repos側でData Facotryのjson定義が配置されます。

![2022-03-08-11-52-34.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/14836f10-7a29-67d5-dbf3-1c830ef4e9b8.png)



### 2. CICDパイプラインの作成、実行

コラボレーションブランチで作業（今回はmain）でADFを開いていると発行ボタンが押せます。

![2022-03-08-11-56-10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/2dba9135-8062-46c0-6f74-ba1d50ba2f9c.png)


これを押すと、以下のようにadf_publishというブランチがAzure Reposに作成され、ARMテンプレートが配置されます。
※[Azure Data Factoryの環境反映パターン【手動、小規模】](https://qiita.com/ryoma-nagata/items/5fa5ef1d7f5f8029cfa4)で利用したものと同じものです。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/8e390fdf-7845-08cd-3a75-873176f94f2a.png)


このadf_publishが更新されたら＝発行ボタンを押したらパイプラインがトリガーされるように作成したいと思います。

#### 環境の設定

devopsに移動して、environment画面で、**prod** を作成します。
今回用意しているものは運用環境想定ですが、これをTESTや、QA、DEVとしてもいいです（後述のyamlを編集する必要があります。

![2022-03-08-12-03-28.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/ff8bdc45-9424-f467-ecd8-27fa15f16457.png)


作成した環境をクリックし、**・・・**から**Approvals and checks** をクリックします。

![2022-03-08-12-08-18.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/e875cad4-9962-aad5-cdb5-6edb8037781e.png)


**Approvals** をクリックします。

![2022-03-08-12-09-28.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/cb8174a5-bb7d-b548-555c-92d788f5930f.png)


承認をしてもらうDevOps上のメンバーを指定して**Create** します。

![2022-03-08-12-10-01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/87180a55-5581-a7d6-bb7b-5d6f7400726d.png)


#### サービス接続の作成

[サービス接続を作成する](https://docs.microsoft.com/ja-jp/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml#create-a-service-connection) を参考に、サービス接続を作成します。
※リンク先では、サービスプリンシパルを自動作成していますが、**該当のリソースグループに権限をもつサービスプリンシパル** をあらかじめ作成し、manualで作成することを推奨します。

今回は **azure-devops-service-connection** という名前で作成しました。

![2022-03-08-13-13-01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/48c036c5-624f-8d39-a096-450ae0ed1531.png)



#### 必要ファイルのアップロード

1. 配置前後スクリプトをアップします。これにより、トリガーの停止、削除の反映が実施されます

Azure Reposで、adf_publishブランチを選択した状態で、ファイル作成に進みます。

![2022-03-08-13-01-27.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/e7fa138e-3d30-c4a7-3f81-230b096226d0.png)

ファイル名を **PrePostDeploymentsScript.ps1** とします。


[参照元](https://docs.microsoft.com/ja-jp/azure/data-factory/continuous-integration-delivery-sample-script#pre--and-post-deployment-script) のスクリプトをコピーして、はりつけ後、commitします。

![2022-03-08-13-06-11.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/820917f4-5c61-a1c2-811e-efab30b4f033.png)

ルートに作成されるようにしてください。

![2022-03-08-13-14-04.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/5e68e2c7-2ad2-4536-478b-5920e49415f5.png)


2. パラメータファイルを作成してアップします。

ひな型（開発環境でのパラメータ）が ** ARMTemplateParametersForFactory.json ** という名称で作成されているので、

![2022-03-08-13-22-18.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/f7f586d3-882d-974a-4c77-69925c497c47.png)

これをダウンロードして、パラメータ内容を編集します。（以下は今回の例）

![2022-03-08-13-26-38.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/6b7de71f-6cb0-6fbb-eb79-8299b1593e96.png)




ファイル名を変更して、ルートにアップします。今回はファイル名を **ARMTemplateParametersForFactory_prod.json** としています。

![2022-03-08-13-27-44.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/9788851a-0c95-e224-b95d-d5a2655c9779.png)


3. 同様に **azure-pipelines.yaml** という名称で以下のyamlファイルを作成します。

<details>
<summary> **クリックで展開します** </summary>
<div>

```yaml:yaml

name: Data Factory Deployment-PublishBranch

trigger:
  branches:
    include:
      - 'adf_publish'
pr:
  none

variables:
  - name: AZURE_RESOURCE_MANAGER_CONNECTION_NAME
    value: "" # Update to '{your ResourceManagerConnectionName}'
  - name: AZURE_LOCATION
    value: "japaneast" # Update to '{your AZURE_LOCATION}'
  - name: SOURCE_FACTORY_NAME
    value: "" # Update to '{your SOURCE_FACTORY_NAME}'
  - name: TARGET_AZURE_SUBSCRIPTION_ID
    value: "" # Update to '{your TARGET_AZURE_SUBSCRIPTION_ID}'
  - name: TARGET_RESOURCE_GROUP_NAME
    value: "" # Update to '{your TARGET_RESOURCE_GROUP_NAME}'
  - name: TARGET_FACTORY_NAME
    value: "" # Update to '{your TARGET_FACTORY_NAME}'
  - name: PARAMETER_FILE_NAME
    value: "" # Update to '{your PARAMETER_FILE_NAME}'


stages:
  - stage: Validation
    displayName: "Validation of IaC templates"
    jobs:
      - job: Validation
        displayName: "Validation of IaC templates"
        continueOnError: false
        pool:
          vmImage: "ubuntu-latest"

        steps:
          # Checkout code
          - checkout: self
            name: checkout_repository
            displayName: Checkout repository
            submodules: true
            lfs: false
            clean: true
            continueOnError: false
            enabled: true

          # Deploy ARM - validation
          - task: AzureResourceManagerTemplateDeployment@3
            name: ARM_validation
            displayName: ARM - validation
            enabled: true
            continueOnError: false
            inputs:
              deploymentScope: "Resource Group"
              ConnectedServiceName: $(AZURE_RESOURCE_MANAGER_CONNECTION_NAME)
              subscriptionId: $(TARGET_AZURE_SUBSCRIPTION_ID) 
              resourceGroupName: $(TARGET_RESOURCE_GROUP_NAME)
              location: $(AZURE_LOCATION)
              templateLocation: "Linked artifact"
              csmFile: $(System.DefaultWorkingDirectory)/$(SOURCE_FACTORY_NAME)/ARMTemplateForFactory.json
              csmParametersFile: $(System.DefaultWorkingDirectory)/$(PARAMETER_FILE_NAME)
              deploymentMode: "Validation"

          # Deploy ARM - what-if
          - task: AzureCLI@2
            name: ARM_whatif
            displayName: Deploy ARM - what-if
            enabled: true
            continueOnError: false
            inputs:
              azureSubscription: $(AZURE_RESOURCE_MANAGER_CONNECTION_NAME)
              scriptType: pscore
              scriptLocation: inlineScript
              inlineScript: |
                az account set `
                  --subscription $(TARGET_AZURE_SUBSCRIPTION_ID)
                
                az deployment group what-if `
                  --resource-group $(TARGET_RESOURCE_GROUP_NAME) `
                  --subscription $(TARGET_AZURE_SUBSCRIPTION_ID) `
                  --exclude-change-types Ignore NoChange Unsupported `
                  --template-file $(System.DefaultWorkingDirectory)/$(SOURCE_FACTORY_NAME)/ARMTemplateForFactory.json `
                  --parameters  $(System.DefaultWorkingDirectory)/$(PARAMETER_FILE_NAME) `
                  --result-format "FullResourcePayloads"
                
              powerShellErrorActionPreference: "stop"
              addSpnToEnvironment: false
              useGlobalConfig: false
              failOnStandardError: false
              powerShellIgnoreLASTEXITCODE: false


          - publish: '$(System.DefaultWorkingDirectory)'
            displayName: 'Publish ARMtemplate'
            artifact: 'datafactory'

  - stage: Deployment_prod
    displayName: "Deployment Prod of IaC templates"

    # condition: and(succeeded(), in(variables['Build.Reason'], 'IndividualCI', 'BatchedCI'))
    jobs:
    - deployment: DeployToDev
      displayName: "Deployment of IaC templates"
      continueOnError: false
      pool:
        vmImage: "windows-latest"
      environment: prod #配置先環境により変更する
      strategy:
        runOnce:
          deploy:
            steps:
              # Download Artifact

              # - task: DownloadPipelineArtifact@2 #downloading artifacts created in build stage
              #   inputs:
              #     source: 'current'
              #     path: '$(Pipeline.Workspace)'
              # - download: current
              #   artifact: infra
              - task: AzurePowerShell@5
                displayName: ADF predeployment 
                inputs:
                  azureSubscription: $(AZURE_RESOURCE_MANAGER_CONNECTION_NAME)
                  ScriptType: 'FilePath'
                  ScriptPath: '$(Pipeline.Workspace)/datafactory/PrePostDeploymentsScript.ps1'
                  ScriptArguments: '$(Pipeline.Workspace)/datafactory/$(SOURCE_FACTORY_NAME)/ARMTemplateForFactory.json `
                                    -ResourceGroupName $(TARGET_RESOURCE_GROUP_NAME) `
                                    -DataFactoryName $(TARGET_FACTORY_NAME) `
                                    -predeployment $true -deleteDeployment $false'
                  azurePowerShellVersion: 'LatestVersion'

              # Deploy ARM
              - task: AzureResourceManagerTemplateDeployment@3
                name: ARM_deployment
                displayName: ARM Deployment
                enabled: true
                continueOnError: false
                inputs:
                  deploymentScope: "Resource Group"
                  ConnectedServiceName: $(AZURE_RESOURCE_MANAGER_CONNECTION_NAME)
                  subscriptionId: $(TARGET_AZURE_SUBSCRIPTION_ID) 
                  resourceGroupName: $(TARGET_RESOURCE_GROUP_NAME)
                  location: $(AZURE_LOCATION)
                  templateLocation: "Linked artifact"
                  csmFile: $(Pipeline.Workspace)/datafactory/$(SOURCE_FACTORY_NAME)/ARMTemplateForFactory.json
                  csmParametersFile: $(Pipeline.Workspace)/datafactory/$(PARAMETER_FILE_NAME)
                  deploymentMode: "Incremental"

              - script: echo $(armOutputs)
                displayName: 'Log armOutputs'

              - task: AzurePowerShell@5
                displayName: ADF postdeployment 
                inputs:
                  azureSubscription: $(AZURE_RESOURCE_MANAGER_CONNECTION_NAME)
                  ScriptType: 'FilePath'
                  ScriptPath: '$(Pipeline.Workspace)/datafactory/PrePostDeploymentsScript.ps1'
                  ScriptArguments: '$(Pipeline.Workspace)/datafactory/$(SOURCE_FACTORY_NAME)/ARMTemplateForFactory.json `
                                    -ResourceGroupName $(TARGET_RESOURCE_GROUP_NAME) `
                                    -DataFactoryName $(TARGET_FACTORY_NAME) `
                                    -predeployment $false -deleteDeployment $true'
                  azurePowerShellVersion: 'LatestVersion'

```
</div>

</details>


変数を変更する必要があり、私の環境の場合は以下のようになります。

![2022-03-08-13-10-03.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/359fe57d-df62-fe87-e843-1279b950b7db.png)


こちらはどこにおいてもいいですが、一旦ルートに配置します。

![2022-03-08-13-29-27.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/0103a2f2-d38c-0bed-1f80-07961a734325.png)


#### Azure Pipelineの設定

Azure Reposで、**Pipeline->New pipeline** で新規作成画面に進みます。

![2022-03-08-13-17-04.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/6ff238ce-03ac-b3be-aa02-e08309ec5a76.png)



**Azure Repos Git** を選択

![2022-03-08-13-17-50.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/8e743c10-60e6-01d5-41bd-96505b6384fd.png)


adf_publishを設定したレポジトリを選択（今回は **DataFactoryDEMO**

![2022-03-08-13-18-26.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/dee21769-8cdc-3bed-cbad-6cedba51be37.png)


**Exsisting Azure Pipeline YAML file** を選択

![2022-03-08-13-19-04.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/09ac3297-509b-3b93-ff2c-2e753aaf6309.png)


ブランチを **adf_publish** に切り替え、**/azure-pipeline.yaml**を選択します。

![2022-03-08-13-19-42.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/42b48711-73c3-2b0c-bcd2-2e69e29b377e.png)


先ほど作成したyaml定義が確認できるので、 **variables** の内容を確認したうえで、**Run** します。

パイプライン実行が進みますが、権限周りの承認が必要な場合は適宜承認してください。

![2022-03-08-13-31-47.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/47087ad2-879f-ce9d-08b6-e5c33a5074b0.png)



また、環境設定で承認を設定した場合は、**Approve** が必要です。

![2022-03-08-13-33-09.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/592112a8-a13f-7d80-c2fb-c327de4595d6.png)



本番環境にデプロイされました。

![2022-03-06-11-59-02.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/fa703836-7ba4-8a89-fdfe-226501f15cea.png)


![2022-03-08-13-38-04.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/36b65212-5361-cc11-4cff-f5d410e7abe9.png)



### 3. トリガーの確認と簡単な開発の流れ

開発Data Factoryに戻り、追加開発をしてみます（今回はデータセットを削除してみます。）

作業用のブランチを作成します。

![2022-03-08-13-36-36.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/436c42be-b792-c3ca-dfa8-d87f9f829c27.png)


ブランチ名は何らかのルールを作ることを推奨します。

![2022-03-08-13-37-04.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/327e0b00-dd36-f95b-f535-7c75b18c63dc.png)


データセットを削除してみます。

![2022-03-08-13-38-04.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/93311be7-6ffd-f18d-5368-fc6181ce152c.png)


削除の場合は、直接git上のファイルが削除されます。

![2022-03-08-13-38-40.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/fb03ce43-5a96-0bfa-bb9b-2acbfc40b62e.png)



ついでに、簡単なパイプラインも作ってみます。

![2022-03-08-13-39-19.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/3c07beef-f36b-f20d-59ce-8a4660d71c6e.png)


**すべてを保存** することで、git上に反映されます

![2022-03-08-13-40-05.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/a70b692a-61b3-60fa-96da-3f08837c410d.png)


![2022-03-08-13-40-23.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/b6df49bc-1608-ca53-6e5f-f78e09b9ad61.png)


これをmainに反映する（各自の作業を統合する）にはPull Requestを作成します。（Azure Reposからも作成可能です。

![2022-03-08-13-41-02.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/36706223-ea21-9f61-5010-0c9212595261.png)


今回はこのような感じ

![2022-03-08-13-41-53.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/77ab9775-50b8-9ae4-6ffe-9e88df1d431f.png)


**Approve** と **Complete** を実行してmainにマージします。

![2022-03-08-13-54-29.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/a53a6406-15bf-94d2-de6b-2ebbf44bafad.png)


Data Factoryに戻り、mainブランチを見ると反映が確認できます。

![2022-03-08-13-55-06.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/4a0e44a0-3de1-10dd-0bb8-80cecea3d8b8.png)


この状態で、発行ボタンを押すと、adf_publishが更新されます。

![2022-03-08-13-56-05.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/75e930b0-8c5a-a6d5-42eb-387944c83e68.png)



更新を検知して先ほど作成したパイプラインが実行されます。

![2022-03-08-13-56-36.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/f9ea4b31-e9f5-9822-87b3-eb52a96667ae.png)


本番Data Factoryでの反映が確認できます。配置スクリプトのおかげで削除も反映されています。

![2022-03-08-14-01-41.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/281819/cf5a0a03-3099-a77c-dc32-2bb21565aef6.png)
