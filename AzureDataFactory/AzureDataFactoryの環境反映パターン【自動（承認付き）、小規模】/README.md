## はじめに

Data Factoryの開発環境から本番環境への反映方法についてまとめます。

今回は大規模なDataFactory向けのパターンである、**自動（承認付き）**、**小規模向け**となります。

注意事項：
- Synapse では利用できません。SynapseはARM上に成果物を保持していないため


2022/03時点の情報です。


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
![](.image/2022-03-06-11-40-49.png)

データセット：
![](.image/2022-03-06-11-41-13.png)

#### 本番環境

作成した時点のデフォルト状態です。

リンクサービス：
![](.image/2022-03-06-11-44-28.png)

データセット：
![](.image/2022-03-06-11-44-41.png)

### 1. DevOps統合の設定

[Azure Repos Git 統合を使用した作成](https://docs.microsoft.com/ja-jp/azure/data-factory/source-control#author-with-azure-repos-git-integration)を参考に、Data FactoryとDevOpsのgit構成を設定します。

レポジトリの新規作成は今はできないようなので、Azure Repos側で作成します。

![](.image/2022-03-08-11-48-49.png)



**開発済みのADFがある場合にDevOps統合を設定する場合** には、以下のように、既存のリソースのインポートを設定します。今回はすでに作ったものを使うので、これを設定します。
ルートフォルダーもdatafactoryなどのフォルダを指定するのがおすすめです。

![](.image/2022-03-08-11-49-45.png)

設定後の画面では、作業ブランチは適宜作成してください。今回はリソース反映のデモをしたいだけなので、mainで作業します。

![](.image/2022-03-08-11-51-59.png)

設定が済んだ段階で、Azure Repos側でData Facotryのjson定義が配置されます。

![](.image/2022-03-08-11-52-34.png)


### 2. CICDパイプラインの作成、実行

コラボレーションブランチで作業（今回はmain）でADFを開いていると発行ボタンが押せます。

![](.image/2022-03-08-11-56-10.png)

これを押すと、以下のようにadf_publishというブランチがAzure Reposに作成され、ARMテンプレートが配置されます。
※[Azure Data Factoryの環境反映パターン【手動、小規模】](https://qiita.com/ryoma-nagata/items/5fa5ef1d7f5f8029cfa4)で利用したものと同じものです。

![](.image/2022-03-08-15-24-55.png)

このadf_publishが更新されたら＝発行ボタンを押したらパイプラインがトリガーされるように作成したいと思います。

#### 環境の設定

devopsに移動して、environment画面で、**prod** を作成します。
今回用意しているものは運用環境想定ですが、これをTESTや、QA、DEVとしてもいいです（後述のyamlを編集する必要があります。

![](.image/2022-03-08-12-03-28.png)

作成した環境をクリックし、**・・・**から**Approvals and checks** をクリックします。

![](.image/2022-03-08-12-08-18.png)

**Approvals** をクリックします。

![](.image/2022-03-08-12-09-28.png)

承認をしてもらうDevOps上のメンバーを指定して**Create** します。

![](.image/2022-03-08-12-10-01.png)

#### サービス接続の作成

[サービス接続を作成する](https://docs.microsoft.com/ja-jp/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml#create-a-service-connection) を参考に、サービス接続を作成します。
※リンク先では、サービスプリンシパルを自動作成していますが、**該当のリソースグループに権限をもつサービスプリンシパル** をあらかじめ作成し、manualで作成することを推奨します。

今回は **azure-devops-service-connection** という名前で作成しました。

![](.image/2022-03-08-13-13-01.png)

#### 必要ファイルのアップロード

1. 配置前後スクリプトをアップします。これにより、トリガーの停止、削除の反映が実施されます

Azure Reposで、adf_publishブランチを選択した状態で、ファイル作成に進みます。

![](.image/2022-03-08-13-01-27.png)

ファイル名を **PrePostDeploymentsScript.ps1** とします。


[参照元](https://docs.microsoft.com/ja-jp/azure/data-factory/continuous-integration-delivery-sample-script#pre--and-post-deployment-script) のスクリプトをコピーして、はりつけ後、commitします。

![](.image/2022-03-08-13-06-11.png)

ルートに作成されるようにしてください。

![](.image/2022-03-08-13-14-04.png)

2. パラメータファイルを作成してアップします。

ひな型（開発環境でのパラメータ）が ** ARMTemplateParametersForFactory.json ** という名称で作成されているので、

![](.image/2022-03-08-13-22-18.png)

これをダウンロードして、パラメータ内容を編集します。（以下は今回の例）

![](.image/2022-03-08-13-26-38.png)


ファイル名を変更して、ルートにアップします。今回はファイル名を **ARMTemplateParametersForFactory_prod.json** としています。

![](.image/2022-03-08-13-27-44.png)

3. 同様に **azure-pipelines.yaml** という名称で以下のyamlファイルを作成します。

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


変数を変更する必要があり、私の環境の場合は以下のようになります。

![](.image/2022-03-08-13-10-03.png)

こちらはどこにおいてもいいですが、一旦ルートに配置します。

![](.image/2022-03-08-13-29-27.png)

#### Azure Pipelineの設定

Azure Reposで、**Pipeline->New pipeline** で新規作成画面に進みます。

![](.image/2022-03-08-13-17-04.png)

**Azure Repos Git** を選択

![](.image/2022-03-08-13-17-50.png)

adf_publishを設定したレポジトリを選択（今回は **DataFactoryDEMO**

![](.image/2022-03-08-13-18-26.png)

**Exsisting Azure Pipeline YAML file** を選択

![](.image/2022-03-08-13-19-04.png)

ブランチを **adf_publish** に切り替え、**/azure-pipeline.yaml**を選択します。

![](.image/2022-03-08-13-19-42.png)

先ほど作成したyaml定義が確認できるので、 **variables** の内容を確認したうえで、**Run** します。

パイプライン実行が進みますが、権限周りの承認が必要な場合は適宜承認してください。

![](.image/2022-03-08-13-31-47.png)

また、環境設定で承認を設定した場合は、**Permit** が必要です。

![](.image/2022-03-08-13-33-09.png)

本番環境にデプロイされました。

![](.image/2022-03-06-11-59-02.png)

![](.image/2022-03-08-13-38-04.png)


### 3. トリガーの確認と簡単な開発の流れ

開発Data Factoryに戻り、追加開発をしてみます（今回はデータセットを削除してみます。）

作業用のブランチを作成します。

![](.image/2022-03-08-13-36-36.png)

ブランチ名は何らかのルールを作ることを推奨します。

![](.image/2022-03-08-13-37-04.png)

データセットを削除してみます。

![](.image/2022-03-08-13-35-46.png)

削除の場合は、直接git上のファイルが削除されます。

![](.image/2022-03-08-13-38-40.png)


ついでに、簡単なパイプラインも作ってみます。

![](.image/2022-03-08-13-39-19.png)

**すべてを保存** することで、git上に反映されます

![](.image/2022-03-08-13-40-05.png)

![](.image/2022-03-08-13-40-23.png)

これをmainに反映する（各自の作業を統合する）にはPull Requestを作成します。（Azure Reposからも作成可能です。

![](.image/2022-03-08-13-41-02.png)

今回はこのような感じ

![](.image/2022-03-08-13-41-53.png)

**Approve** と **Complete** を実行してmainにマージします。

![](.image/2022-03-08-13-54-29.png)

Data Factoryに戻り、mainブランチを見ると反映が確認できます。

![](.image/2022-03-08-13-55-06.png)

この状態で、発行ボタンを押すと、adf_publishが更新されます。

![](.image/2022-03-08-13-56-05.png)


更新を検知して先ほど作成したパイプラインが実行されます。

![](.image/2022-03-08-13-56-36.png)

本番Data Factoryでの反映が確認できます。配置スクリプトのおかげで削除も反映されています。

![](.image/2022-03-08-14-01-41.png)