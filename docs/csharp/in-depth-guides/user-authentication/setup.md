---
title: App Setup (C#)
description: Learn about App Setup (C#)
ms.topic: how-to
ms.date: 05/17/2025
---
# App Setup (C#) (preview)

[This article is prerelease documentation and is subject to change.]

There are a few ways you can enable your application to access secured external services on the user's behalf.

> [!NOTE]
> This is an advanced guide. It is highly recommended that you are familiar with [Teams Core Concepts](../../../teams/core-concepts.md) before attempting this guide.

## Authenticate the user to Entra ID to access Microsoft Graph APIs
A very common use case is to access enterprise related information about the user, which can be done through Microsoft Graph's APIs. To do that the user will have to be authenticated to Entra ID. 

> [!NOTE]
> See [How Auth Works](auth-sso.md) to learn more about how authentication works. 

### Manual Setup

In this step you will have to tweak your Azure Bot service and App registration to add authentication configurations and enable Single Sign-On (SSO).

> [!NOTE]
> [Single Sign-On (SSO)](../user-authentication/auth-sso.md) in Teams allows users to access your app seamlessly by using their existing Teams account credentials for authentication. A user who has logged into Teams doesn't need to log in again to your app within the Teams environment.

You can follow the [Enable SSO for bot and message extension app using Entra ID](/microsoftteams/platform/bots/how-to/authentication/bot-sso-register-aad?tabs=botid) guide in the Microsoft Learn docs.

### Using Teams Toolkit with the `teams` CLI

Open your terminal and navigate to the root folder of your app and run the following command:

```sh
teams config add ttk.oauth
```

The `ttk.oauth` configuration is a basic setup for Teams Toolkit along with configurations to authenticate the user with Microsoft Entra ID to access Microsoft Graph APIs.

This [CLI](../../../developer-tools/cli.md) command adds configuration files required by Teams Toolkit, including:

- Azure Application Entra ID manifest file `aad.manifest.json`.
- Azure bicep files to provision Azure bot in `infra/` folder.

> [!NOTE]
> Teams toolkit, in the debugging flow, will deploy the `aad.manifest.json` and `infra/azure.local.bicep` file to provision the Application Entra ID and Azure bot with oauth configurations.

## Authenticate the user to third-party identity provider

You can follow the [Add authentication to bot app](/microsoftteams/platform/bots/how-to/authentication/add-authentication?tabs=dotnet%2Cdotnet-sample) Microsoft Learn guide.

## Configure the OAuth Connection Name in the `App` instance

In the [Using Teams Toolkit with `teams` CLI](#using-teams-toolkit-with-the-teams-cli) guide, you will notice that the OAuth Connection Name that was created in the Azure Bot configuration is `graph`. This is arbitrary and you can even create more than one configuration. You can specify which configuration to use by defining it in the app options on intialization:

```typescript
const app = new App({ 
  oauth: { // oauth configurations
    /**
     * The name of the auth connection to use.
     * It should be the same as the OAuth connection name defined in the Azure Bot configuration.
     */
    defaultConnectionName: 'graph' 
  },
  logger: new ConsoleLogger('@tests/auth', { level: 'debug' })
});

```

## Resources

- [User Authentication Basics](/azure/bot-service/bot-builder-concept-authentication)
- [User Authentication in Teams](/microsoftteams/platform/concepts/authentication/authentication)