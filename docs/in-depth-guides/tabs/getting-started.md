---
title: Getting started
description: Set up new tab app projects or add Teams client capabilities to existing tab applications.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 05/15/2026
---
# Getting started

::: zone pivot="csharp,python"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="typescript"
To use this package, you can either set up a new project using the Teams Developer CLI, or add it to an existing tab app project.

## Setting up a new project

The Teams Developer CLI ships a `tab` template that scaffolds a new tab app with a callable remote function. First install the Teams Developer CLI as outlined in the [Quickstart](../../getting-started/quickstart.md) guide, then create the app:

```sh
teams project new typescript my-first-tab-app --template tab
```

Once the project is created, follow [Quickstart: Register your app](../../getting-started/quickstart.md) to register and sideload it into Teams.

## Adding to an existing project

This package is set up to integrate well with existing Tab apps. The main consideration is that the AAD app must be configured to support Nested App Authentication (NAA). Otherwise it will not be possible to acquire the bearer token needed to call Microsoft Graph APIs or remote agent functions.

After verifying that the app is configured for NAA, simply use your package manager to add a dependency on `@microsoft/teams.client` and then proceed with [Starting the app](./using-the-app.md).

If you're already using a current version of TeamsJS, that's fine. This package works well with TeamsJS.

If you're already using Microsoft Authentication Library (MSAL) in an NAA enabled app, that's great! The [App options](./app-options.md) page shows how you can use a single common MSAL instance.

## Resources

- [Quickstart: Register your app](../../getting-started/quickstart.md)
- [Configuring an app for Nested App Authentication](/microsoftteams/platform/concepts/authentication/nested-authentication#configure-naa)
::: zone-end