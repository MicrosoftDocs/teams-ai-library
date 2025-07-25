---
title: Getting started (preview) (TypeScript)
description: Get started building Teams tab applications with the Microsoft Teams AI Library for TypeScript.
ms.topic: how-to
ms.date: 07/16/2025
---
# Getting started (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

To use this package, you can either set up a new project using the Teams CLI, or add it to an existing tab app project.

## Setting up a new project
The Teams CLI contains a Microsoft 365 Agents Toolkit configuration and a template to easily scaffold a new tab app with a callable remote function. To set this up, first install the Teams CLI as outlined in the [Quickstart](../../getting-started/quickstart.md) guide. Then, create the app by running:


```sh
teams new my-first-tab-app --tk embed --template tab
```


When the app is created, you can use the Agents Toolkit to run and debug it inside of Teams from your local machine, same as for any other Agents Toolkit tab app.

## Adding to an existing project
This package is set up to integrate well with existing Tab apps. The main consideration is that the AAD app must be configured to support Nested App Authentication (NAA). Otherwise it will not be possible to acquire the bearer token needed to call Microsoft Graph APIs or remote agent functions.

After verifying that the app is configured for NAA, simply use your package manager to add a dependency on `@microsoft/teams.client` and then proceed with [Starting the app](./using-the-app.md).

If you're already using a current version of TeamsJS, that's fine. This package works well with TeamsJS.

If you're already using Microsoft Authentication Library (MSAL) in an NAA enabled app, that's great! The [App options](./app-options.md) page shows how you can use a single common MSAL instance.

## Resources
 - [Running and debugging local apps in Agents Toolkit](/microsoftteams/platform/toolkit/debug-local?tabs=Windows)
 - [Configuring an app for Nested App Authentication](/microsoftteams/platform/concepts/authentication/nested-authentication#configure-naa)