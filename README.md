# Cloud Resume backend
This is a repository for Yue's Cloud Resume Challenge - Backend. I seperate the frontend and backend into different repos.
Here is basically what I have done for backend. 

## Introduction

## Azure Cosmos DB

## Azure Funtion

## Python code on Azure Function

## FAQ
Below are some questions or issues I encountered during the backend deployment. I attached the resolution that I found for them. Hope it helps you as well.
1. What are bindings in Auzre Functions. How to use it in this project?

I hate to 

2. CORS issue.

```text
Access to fetch at 'https://joycefunc.azurewebsites.net/api/hello' from origin 'null' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.
```

## Useful links
[Create your first function in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal?pivots=programming-language-python#create-function)

[Azure Functions HTTP trigger](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=python-v2%2Cisolated-process%2Cnodejs-v4%2Cfunctionsv2&pivots=programming-language-python#decorators)

[Azure for Python Developers](https://learn.microsoft.com/en-us/azure/developer/python/?view=azure-python)

[functions Package](https://learn.microsoft.com/en-us/python/api/azure-functions/azure.functions?view=azure-python)

[Azure Functions Python developer guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=get-started%2Casgi%2Capplication-level&pivots=python-mode-decorators#connect-to-a-database)

[Azure Functions Python HTTP Trigger using Azure Developer CLI](https://learn.microsoft.com/en-us/samples/azure-samples/functions-quickstart-python-http-azd/functions-quickstart-python-azd/)

[Connect Azure Functions to Azure Cosmos DB using Visual Studio Code](https://learn.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-cosmos-db-vs-code?pivots=programming-language-python)

[Azure Function input bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-cosmosdb-v2-input?tabs=python-v1%2Cisolated-process%2Cnodejs-v4%2Cextensionv4&pivots=programming-language-python#queue-trigger-look-up-id-from-json-python)

[Azure Function output bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-cosmosdb-v2-output?tabs=python-v2%2Cisolated-process%2Cnodejs-v4%2Cextensionv4&pivots=programming-language-pythone)

[Triggers and Bindings - Azure Funcions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings?tabs=isolated-process%2Cnode-v4%2Cpython-v2&pivots=programming-language-csharp)

[Cloud Resume Challenge - GitHub](https://github.com/cloudresumechallenge/projects/tree/main/projects)

### Pipeline workflow
[Use GitHub Actions workflow to deploy your static website in Azure Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-static-site-github-actions?tabs=userlevel)