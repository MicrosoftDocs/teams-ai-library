---
title: 'Teams Manifest'
description: 'Learn about Teams app manifest requirements, permissions, and sideloading process for app installation.'
ms.topic: how-to
ms.date: 06/29/2026
---

# Teams Manifest

Every app or agent installed on Teams requires an app manifest json file, which provides important information and permissions to that app. When sideloading the app, you are required to provide the app manifest via zip which also includes the icons for the app.

## Manifest

There are many permissions and details that an app manifest may have added to the `manifest.json`, including the app ID, url, and much more. Please review the comprehensive documentation on the [manifest schema](/microsoft-365/extensibility/schema/).

## Sideloading

Sideloading is the ability to install and test your app before it is published to your organization's app catalog. For more on sideloading, see [Upload your apps to Teams](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload/).

To sideload, ensure the manifest includes all required information (such as the app ID, tenant details, and permissions). Place the manifest and icons at the root of a zip file.

The [Teams Developer CLI](../developer-tools/cli.md) handles manifest scaffolding, validation, and updates as part of `teams app create`. To work with the manifest directly:

- [`teams app manifest download`](https://microsoft.github.io/teams-sdk/cli/commands/app/manifest-download/) pull the current manifest from a registered app
- [`teams app manifest upload`](https://microsoft.github.io/teams-sdk/cli/commands/app/manifest-upload/) apply a local manifest.json to an existing app
- [`teams app package download`](https://microsoft.github.io/teams-sdk/cli/commands/app/package-download/) get a sideload-ready zip (manifest + icons)

