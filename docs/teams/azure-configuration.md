---
title: Azure Configuration
description: Manually create the Entra App Registration and Azure Bot Service resource for cases where the Teams Developer CLI is not the right fit.
ms.topic: how-to
ms.date: 07/27/2026
---

# Azure Configuration

This page walks through creating the Entra App Registration and Azure Bot Service resource by hand. As described in [Core Concepts](./core-concepts.md), those two pieces are what every Azure-managed Teams bot needs.

> [!TIP]
>
> Most readers should use the Teams Developer CLI instead
> For almost everything, `teams app create --azure --subscription <id> --resource-group <rg>` is the right answer a it provisions the Entra app, the Azure Bot resource, the Teams channel, and writes credentials in one command. See the [Quickstart: Register your app](../get-started/quickstart-register.md).
>
> Or use the [`teams-dev` agent skill](../developer-tools/agent-skills.md) a tell your AI assistant to set up your Teams bot and it handles everything automatically.
>
> **Use this page when:**
>
> - You have an existing Entra app you can't recreate (and want to point an Azure Bot at it)
> - Your tenant policy requires Azure resources be created with specific naming, tags, or networking the CLI doesn't expose
> - You're working in a locked-down environment where the CLI can't run (e.g., audited CI without Node, restricted service accounts)
> - You want to understand exactly what `teams app create --azure` does under the hood

## Requirements

1. An Azure subscription
2. Permissions to create Entra ID App Registrations (if you don't have permissions in your tenant, ask your admin to create the App Registration and share the `Application Id`)
3. Permissions to create Azure Bot Service resources
4. (Optional) The [Azure CLI](https://aka.ms/azcli) installed and authenticated to your Azure subscription

## Create the Entra App Registration

After a successful App Registration you'll have the `TenantId`, `ClientId`, and `ClientSecret` values, which you'll use later.

> [!TIP]
>
> This guide uses Client Secrets. To use other authentication types, see the [App Authentication](./app-authentication/overview.md) setup guide.

# [Azure Portal](#tab/portal)

1. Navigate to [Entra ID App Registrations](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps).
2. Select **New App Registration** and provide a name. Take note of the assigned `Application Id` (also known as `ClientId`) and `TenantId`.
3. Navigate to **Certificates & secrets** and create a **New client secret**.

---

# [Azure CLI](#tab/cli)

> [!NOTE]
>
> The Azure CLI snippets on this page use bash syntax (line continuations with `\`, command substitution with `$(...)`, `IFS read`). On Windows, run them in **WSL** or **Git Bash**, or adapt to PowerShell (use `` ` `` for line continuations and `$(...)` works the same way).

```bash

botName="My App"
appId=$(az ad app create --display-name "$botName" --sign-in-audience "AzureADMyOrg" --query appId -o tsv)
az ad sp create --id "$appId"
IFS=$'\t' read -r tenantId clientSecret <<< "$(az ad app credential reset --id "$appId" --query "[tenant, password]" -o tsv)"
```

---

## Create the Azure Bot Service resource

> [!TIP]
>
> You can create the Azure Bot Service resource and the Entra App Registration from the same screen, then create a new client secret afterward.

# [Azure Portal - Create Azure Bot Service](#tab/portal)

1. Create or select the resource group where you want to create the Azure Bot resource.
2. In the resource group, click **Create** and search for `bot`.
3. Select **Azure Bot** and click **Create**.
4. Provide the bot handle (for example, `MyBot`), data residency, and pricing tier.
   1. Under **Microsoft App ID**, select **Single Tenant**.
   2. In **Creation type**, select **Use existing app registration** and provide the `Application Id` from the previous step.

---

# [Azure CLI - Create Azure Bot Service](#tab/cli)

This step uses the `resourceGroup`, `tenantId`, and `appId` variables from the previous step.

```bash

az bot create \
   --name "$botName" \
   --app-type SingleTenant \
   --appid $appId \
   --tenant-id $tenantId \
   --resource-group $resourceGroup
```

---

## Configure the messaging endpoint

Once the Azure Bot resource exists, point it at your public HTTPS endpoint. Use [DevTunnels](/azure/developer/dev-tunnels/overview) (or another tunnel like ngrok) to expose your local server during development.

# [Azure Portal - Configure Messaging Endpoint](#tab/portal)

1. Under **Settings a Configuration**, set the **Messaging endpoint** URL.
   - Local development with DevTunnels: `https://<tunnel-host>/api/messages`
   - Deployed to App Services / Container Apps / other cloud: `https://<your-host>/api/messages`
2. Under **Settings a Channels**, enable the **Microsoft Teams** channel.

---

# [Azure CLI - Configure Messaging Endpoint](#tab/cli)

```bash

endpointUrl=<your-public-url>
az bot update \
   --name "$botName" \
   --resource-group $resourceGroup \
   --endpoint $endpointUrl

az bot msteams create \
    --name "$botName" \
    --resource-group $resourceGroup
```

## Save the credentials

```bash

echo "TENANT_ID=$tenantId" > .env
echo "CLIENT_ID=$appId" >> .env
echo "CLIENT_SECRET=$clientSecret" >> .env
```

For C# projects, write the credentials to `appsettings.json` under a `Teams` section using PascalCase keys (`ClientId`, `ClientSecret`, `TenantId`).

## Resources

- [Quickstart: Register your app](../get-started/quickstart-register.md) an automated setup with the Teams Developer CLI
- [Teams Developer CLI](../developer-tools/cli.md)
- [Teams App Publishing overview](/microsoftteams/platform/concepts/deploy-and-publish/apps-publish-overview)


