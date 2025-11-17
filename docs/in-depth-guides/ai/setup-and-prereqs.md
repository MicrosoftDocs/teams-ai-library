---
sidebar_label: Setup & Prerequisites
title: Setup & Prerequisites
zone_pivot_groups: dev-lang
description: Prerequisites and setup guide for integrating LLMs into Teams SDK applications, including API keys and configuration.
---
# Setup & Prerequisites

There are a few prerequisites to getting started with integrating LLMs into your application:

- LLM API Key - To generate messages using an LLM, you will need to have an API Key for the LLM you are using.
  - [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
  - [OpenAI](https://platform.openai.com/)


::: zone pivot="csharp"
**NuGet Package** - Install the Microsoft Teams SDK:

```bash
dotnet add package Microsoft.Teams.AI
```
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
<!-- Not applicable -->
::: zone-end


::: zone pivot="csharp"
- In your application, you should include your keys in a secure way. You should include your keys securely using `appsettings.json` or environment variables
::: zone-end

::: zone pivot="python,typescript"
- In your application, you should include your keys in a secure way. We recommend putting it in an .env file at the root level of your project
::: zone-end


::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
```
my-app/
|── appPackage/       # Teams app package files
├── src/
│   └── main.py      # Main application code
|── .env              # Environment variables
```
::: zone-end

::: zone pivot="typescript"
```
my-app/
|── appPackage/       # Teams app package files
├── src/
│   └── index.ts      # Main application code
|── .env              # Environment variables
```
::: zone-end


### Azure OpenAI

You will need to deploy a model in Azure OpenAI. View the [resource creation guide](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model 'Azure OpenAI Model Deployment Guide') for more information on how to do this.


::: zone pivot="csharp"
Once you have deployed a model, configure your application using `appsettings.json` or `appsettings.Development.json`:

**appsettings.Development.json**

```json
{
  "AzureOpenAIKey": "your-azure-openai-api-key",
  "AzureOpenAIModel": "your-azure-openai-model-deployment-name",
  "AzureOpenAIEndpoint": "https://your-resource.openai.azure.com/"
}
```

**Using configuration in your code:**

```csharp
var azureOpenAIModel = configuration["AzureOpenAIModel"] ??
    throw new InvalidOperationException("AzureOpenAIModel not configured");
var azureOpenAIEndpoint = configuration["AzureOpenAIEndpoint"] ??
    throw new InvalidOperationException("AzureOpenAIEndpoint not configured");
var azureOpenAIKey = configuration["AzureOpenAIKey"] ??
    throw new InvalidOperationException("AzureOpenAIKey not configured");

var azureOpenAI = new AzureOpenAIClient(
    new Uri(azureOpenAIEndpoint),
    new ApiKeyCredential(azureOpenAIKey)
);

var aiModel = new OpenAIChatModel(azureOpenAIModel, azureOpenAI);
```

:::tip
Use `appsettings.Development.json` for local development and keep it in `.gitignore`. For production, use environment variables or Azure Key Vault.
:::
::: zone-end

::: zone pivot="python"
Once you have deployed a model, include the following key/values in your `.env` file:

```env
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_MODEL=your-azure-openai-model-deployment-name
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_API_VERSION=your-azure-openai-api-version
```
::: zone-end

::: zone pivot="typescript"
Once you have deployed a model, include the following key/values in your `.env` file:

```env
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_MODEL_DEPLOYMENT_NAME=your-azure-openai-model
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_API_VERSION=your-azure-openai-api-version
```
::: zone-end



::: zone pivot="csharp"
:::info
The Azure OpenAI SDK handles API versioning automatically. You don't need to specify an API version manually.
:::
::: zone-end

::: zone pivot="python,typescript"
:::info
The `AZURE_OPENAI_API_VERSION` is different from the model version. This is a common point of confusion. Look for the API Version [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference?WT.mc_id=AZ-MVP-5004796 'Azure OpenAI API Reference')
:::
::: zone-end


### OpenAI

You will need to create an OpenAI account and get an API key. View the [OpenAI Quickstart Guide](https://platform.openai.com/docs/quickstart/build-your-application 'OpenAI Quickstart Guide') for how to do this.


::: zone pivot="csharp"
Once you have your API key, configure your application:

**appsettings.Development.json**

```json
{
  "OpenAIKey": "sk-your-openai-api-key",
  "OpenAIModel": "gpt-4o"
}
```

**Using configuration in your code:**

```csharp
var openAIKey = configuration["OpenAIKey"] ??
    throw new InvalidOperationException("OpenAIKey not configured");
var openAIModel = configuration["OpenAIModel"] ?? "gpt-4o";

var aiModel = new OpenAIChatModel(openAIModel, openAIKey);
```

:::tip
Use `appsettings.Development.json` for local development and keep it in `.gitignore`. For production, use environment variables or Azure Key Vault.
:::
::: zone-end

::: zone pivot="python"
Once you have your API key, include the following key/values in your `.env` file:

```env
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4  # Optional: defaults to gpt-4o if not specified
```
::: zone-end

::: zone pivot="typescript"
Once you have your API key, include the following key/values in your `.env` file:

```env
OPENAI_API_KEY=sk-your-openai-api-key
```
::: zone-end

::: zone pivot="python"
:::note
**Automatic Environment Variable Loading**: The AI models automatically read these environment variables when initialized. You can also pass these values explicitly as constructor parameters if needed for advanced configurations.

```python
# Automatic (recommended)
model = OpenAICompletionsAIModel(model="your-model-name")

# Explicit (for advanced use cases)
model = OpenAICompletionsAIModel(
    key="your-api-key",
    model="your-model-name",
    azure_endpoint="your-endpoint",  # Azure only
    api_version="your-api-version"   # Azure only
)
```

:::
::: zone-end
