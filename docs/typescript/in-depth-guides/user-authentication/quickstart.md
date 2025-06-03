---
title: User authentication quickstart (TypeScript)
description: Learn how to get started quickly with user authentication (TypeScript)
ms.topic: how-to
ms.date: 06/03/2025
---

# User authentication quickstart (TypeScript) (preview)

[This article is prerelease documentation and is subject to change.]

In this section we will walk through creating an app that can access the [Microsoft Graph APIs](/graph/overview) on behalf of the user by authenticating them with the [Microsoft Entra ID](https://www.microsoft.com/security/business/identity-access/microsoft-entra-id) oauth provider. 

> [!NOTE]
> It is possible to authenticate the user into [other auth providers](/azure/bot-service/bot-builder-concept-identity-providers?view=azure-bot-service-4.0&preserve-view=true&tabs=adv2%2Cga2#other-identity-providers) like Facebook, Github, Google, Dropbox, and so on.

> [!WARNING]
> User authentication does not work with the developer tools setup. You have to run the app in Teams. Follow these [instructions](../../getting-started/running-in-teams.md#debugging-in-teams) to run your app in Teams.

## Setup Instructions

### Create an app with the `graph` template

> [!TIP]
> Skip this step if you want to add the auth configurations to an existing app.

> [!NOTE]
> In this template, `graph` is the default name of the OAuth connection, but you can change that by supplying `defaultOauthConnectionName` in the `app`.

Use your terminal to run the following command: 


```sh
teams new oauth-app --template graph
```


This command:
1. Creates a new directory called `oauth-app`.
2. Bootstraps the graph agent template files into it under `oauth-app/src`.
3. Creates your agent's manifest files, including a `manifest.json` file and placeholder icons in the `oauth-app/appPackage` directory. The Teams [app manifest](/microsoftteams/platform/resources/schema/manifest-schema) is required for [sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload) the app into Teams.

### Add Microsoft 365 Agents Toolkit auth configuration

Open your terminal with the `oauth-app/` folder set as the current working directory and run the following command:


```sh
teams config add atk.oauth
```


This will add relevant Agents Toolkit files to your project.

> [!TIP]
> See [App Setup](./setup.md#using-m365-agents-toolkit-with-the-teams-cli) to learn more about what this command does.

## Interacting with the app in Teams

Once you have successfully sideloaded the app into Teams you can now interact with it and sign the user in. 

### Signing the user in

> [!NOTE]
> This is the Single Sign-On (SSO) authentication flow. To learn more about all the available flows and their differences see the [How Auth Works](auth-sso.md) guide.

When the user sends a message to the user a consent form will popup:

:::image type="content" source="~/assets/screenshots/auth-consent-popup.png" alt-text="Consent popup":::

This will ask the user to consent to the `User.ReadBasic.All` Microsoft Graph scope:

> [!NOTE]
> The `atk.oauth` configuration explicitly requests the `User.ReadBasic.All` permission. It is possible to request other permissions by modifying the App Registration for the bot on Azure.

:::image type="content" source="~/assets/screenshots/auth-entra-id-signin.png" alt-text="Entra ID signin":::

Once the user signs in and grants the app access, they will be redirected back to the Teams client and the app will send back the user's information as retrieved from the graph client:

:::image type="content" source="~/assets/screenshots/auth-graph-message.png" alt-text="Graph message":::

The user can then signout by sending the `signout` command to the app:

:::image type="content" source="~/assets/screenshots/auth-signout-message.png" alt-text="Signout message":::