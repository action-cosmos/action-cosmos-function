var location = resourceGroup().location
param app_name string

resource storage_account 'Microsoft.Storage/storageAccounts@2020-08-01-preview' = {
name: 'sa0${app_name}'
  location: location
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
    tier: 'Standard'
  }
}

resource hosting_plan 'Microsoft.Web/serverfarms@2020-06-01' = {
  name: 'asp-${app_name}'
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
}

resource function_app 'Microsoft.Web/sites@2020-06-01' = {
  name: 'functionapp-${app_name}'
  location: location
  kind: 'functionapp'
  properties: {
    httpsOnly: true
    serverFarmId: hosting_plan.id
    clientAffinityEnabled: true
    siteConfig: {
      appSettings: [
        {
          'name': 'FUNCTIONS_EXTENSION_VERSION'
          'value': '~3'
        }
        {
          'name': 'FUNCTIONS_WORKER_RUNTIME'
          'value': 'python'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storage_account.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${listKeys(storage_account.id, storage_account.apiVersion).keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: '${substring(uniqueString(resourceGroup().id), 3)}-azeus-functionapp-dev01'
        }
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storage_account.name};AccountKey=${listKeys(storage_account.id, storage_account.apiVersion)};EndpointSuffix=core.windows.net'
        }
      ]
    }
  }

  dependsOn: [
    hosting_plan
    storage_account
  ]
}
