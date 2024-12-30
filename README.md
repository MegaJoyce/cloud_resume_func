# Cloud Resume backend
This repository hosts Yue's Cloud Resume Challenge - Backend: a function app serving as the API to CosmoDB.

I created a funcion app that receives the HTTP request from the frontend. When the HTTP trigger was activated, the function will connect to the database (CosmoDB) to select the target item, and then return the right result as a string in a HTTP response. 

Below is the process of how I realized it.

## Azure Cosmos DB
First of all, I need to have an existing database. I could not create the database over and over again, because it stores the permanent data. So I created a seperate resource group to host the database, and then just leave them alone. The resson why I use Cosmo DB is that I do not need a complex database. My need is simple, and I want to try No-SQL database that I have never tried before.

For convenience I created the database on Portal, following this guide: [Create an Azure Cosmos DB for NoSQL account using the Azure portal](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/quickstart-portal). I could definitely create it using Terraform, but I will be applying and destroying the resources for multiple times. So I decide not to touch it any more. 

The structure of the database is:
Cosmo DB account > database > container > items. I created the item I need, and all works for DB is done. 

## Azure Funtion
I leveraged the Azure Funtion as the backend. It serves as two roles:
1. receive the HTTP request from the frontend and return the HTTP response to the frontend.
2. fetch, update, and save the data in the database.

### HTTP Request and Response
I created a http trigger for the function ([Create your first function in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal?pivots=programming-language-python#create-function), [Azure Functions HTTP trigger](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=python-v2%2Cisolated-process%2Cnodejs-v4%2Cfunctionsv2&pivots=programming-language-python#decorators)).  This HTTP trigger will receive the HTTP request and then return response. For simplicity, I did not use any information from the HTTP request. Once the function is triggered, the code will run, and then return the response. 

To realize this function, I did not use the normal Request Python module but the `azure-functions` module. It has `.HttpResponse` method for such cases. 

### fetch, update, and save the data in the database
To access to the database, there are a very important concept for Azure Functions: _Bindings_ ([Triggers and Bindings - Azure Funcions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings?tabs=isolated-process%2Cnode-v4%2Cpython-v2&pivots=programming-language-csharp)). 

If I want to fetch the data in the database, I need to establish a output binding to the database; if I want to save data to the database, I need to establish a input binding. In Function V1, such bindings are built through configuration files, but in V2, it could be realized through decorators. I write the code using Python, so I decided to use decorators. 

See the reference links at the end for more information.

## Python code and test
This backend is a simple visit counter, so it has only one method in the Python file. However, I still considered the expection process and used `pytest` to ensure the integrity of the API function. 

For scalability, I decided to develop the Python code in local VS code and test there. So I built the project in VS Code, and push it to GitHub repository (yes, this repo), and integrate the repository with the Azure Function so that it will automatially deploy to Azure if this repository receives a `push` action. A better option is to deploy through a `pull request`. 

Besides, I could also deploy to Azure on VS Code. But the problem is that through this way I could not modify the code on Portal, because such a deployment is a zip file stored in corresponding storage account. Rememeber to delete the previous zip packages. Azure storage is really expensive. Or you could delete the blobs by setting the blob life cycle. It is another topic. 

## Azure Monitor
Now I have functional API. I need to monitor this API if it is down or attacked. So I set matrix alerts. When the alerts are fired, it will notify the action group, then the action group will act to send me email. 

To build a robust alert system, I decided to use logic app workflow. When the alert is fired, it notifies the action group, the action group will send a http request to logic app and trigger the workflow. I only do a simple workflow so it will only notify my teams and email again. But I could add more actions to it if needed. 

## Tips
Below are some questions or issues I encountered during the backend deployment. I attached the resolution that I found for them. Hope it helps you as well.
### What are bindings in Auzre Functions. How to use it in this project?

I have to 

### CORS issue.
When I had successfully deployed all the resources manually, I could get access to the function API via the function url smoothly. But the website failed to get the correct response from the function.

I opened the browser console and found the error message below:
```text
Access to fetch at 'https://FUNCTIONNAME.azurewebsites.net/api/hello' from origin 'null' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.
```

This error is caused by the CORS policy. See more on [What is CORS?](https://aws.amazon.com/what-is/cross-origin-resource-sharing/)

To resolve this issue, I have two options: 
1. Switch on the CORS policy for the Function app and add the allowed origins (domains)
2. In the HTTP response from the backend, add `"Access-Control-Allow-Origin": "*"` in headers, which basically means that allow all origins to access the API. 

The first option requires me to have extra settings when creating the function, you could see it here: [cloud_resume_iac: CORS](https://github.com/MegaJoyce/cloud_resume_iac?tab=readme-ov-file#cors-allow-all-origins). I also adopt the second solution in case I forget to add that setting. 

```python
headers={
"Access-Control-Allow-Origin": "*",  # Allow all origins
"Access-Control-Allow-Methods": "GET, POST, OPTIONS",
"Access-Control-Allow-Headers": "*"
}
```

### Successfully deploy to Azure but HTTP response failed with code 500
It occurred several times that I successfully deployed the function to Azure from local VSCode, but it failed test with code 500 Internal Server Error. Of course the error code did not help at all. I locally ran the function and it worked well. 

I checked the connection string and found that it was not in the right format. It should be like: `"AccountEndpoint=...;AccountKey=...=="`. 

And then I should wait for a longer time to check the health of the API address. Sometimes it is just under processing. 

### Where to save the Cosmo DB account connection string
At first I intended to save the connection string and store it somewhere for me to connect to it. Later I found it insecure. During my whole process I cannot expose the connection string to any one. Therefore, I decided to retrieve the connection string when needed. 

The function app need to connect to the database. I could store the connection string as the environment variable of the funcion. Therefore, I retrieve the primary connection string when creating the function app and then store it as the environment variable. See how I configure it in Terraform configuration files: [Yue He - cloud_resume_iac](https://github.com/MegaJoyce/cloud_resume_iac)

## Useful links
### Azure Function
[Create your first function in the Azure portal](https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal?pivots=programming-language-python#create-function)\
[Azure Functions HTTP trigger](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=python-v2%2Cisolated-process%2Cnodejs-v4%2Cfunctionsv2&pivots=programming-language-python#decorators)\
[Azure for Python Developers](https://learn.microsoft.com/en-us/azure/developer/python/?view=azure-python)\
[functions Package](https://learn.microsoft.com/en-us/python/api/azure-functions/azure.functions?view=azure-python)\
[Azure Functions Python developer guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=get-started%2Casgi%2Capplication-level&pivots=python-mode-decorators#connect-to-a-database)\
[Azure Functions Python HTTP Trigger using Azure Developer CLI](https://learn.microsoft.com/en-us/samples/azure-samples/functions-quickstart-python-http-azd/functions-quickstart-python-azd/)\
[Connect Azure Functions to Azure Cosmos DB using Visual Studio Code](https://learn.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-cosmos-db-vs-code?pivots=programming-language-python)\
[Azure Function input bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-cosmosdb-v2-input?tabs=python-v1%2Cisolated-process%2Cnodejs-v4%2Cextensionv4&pivots=programming-language-python#queue-trigger-look-up-id-from-json-python)\
[Azure Function output bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-cosmosdb-v2-output?tabs=python-v2%2Cisolated-process%2Cnodejs-v4%2Cextensionv4&pivots=programming-language-pythone)\
[Triggers and Bindings - Azure Funcions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings?tabs=isolated-process%2Cnode-v4%2Cpython-v2&pivots=programming-language-csharp)\

### Pipeline workflow
[Use GitHub Actions workflow to deploy your static website in Azure Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-static-site-github-actions?tabs=userlevel)

### Cosmo DB
[Create an Azure Cosmos DB for NoSQL account using the Azure portal](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/quickstart-portal)\

### Monitor
[Receive and respond to inbound HTTPS calls to workflows in Azure Logic Apps](https://learn.microsoft.com/en-us/azure/connectors/connectors-native-reqres?tabs=consumption)

### Security
[Securing Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts?tabs=v4)