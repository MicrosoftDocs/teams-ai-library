---
title: Microsoft 365 Agents Toolkit (preview)
description: Microsoft 365 Agents Toolkit simplifies building and deploying AI agents for Microsoft Teams. Learn how to use the toolkit to streamline your Teams AI development workflow.
ms.topic: how-to
ms.date: 07/16/2025
---

# Microsoft 365 Agents Toolkit (preview)

[This article is prerelease documentation and is subject to change.]

Agents Toolkit is a powerful extension and CLI app that helps automate important tasks like manifest management, sideloading, deployment, and provisioning - if you encounter any issues while using it (such as problems with the extension, running apps, deployment and provisioning, or debugging via F5), please file them in the [Agents Toolkit GitHub repository](https://github.com/OfficeDev/microsoft-365-agents-toolkit).

## Installing Agents Toolkit

Agents Toolkit can be installed as an extension and CLI. Please see the documentation linked below.

- [Installing Agents Toolkit extension](/microsoftteams/platform/toolkit/install-teams-toolkit)
- [Installing Agents Toolkit CLI](/microsoftteams/platform/toolkit/microsoft-365-agents-toolkit-cli)

> [!NOTE]
> * [Teams AI v2 CLI](../developer-tools/cli.md) - helper for the new v2 library. It scaffolds agents, wires in deep Teams features (Adaptive Cards, Conversation History, Memory...etc), and adds all the config files you need while you're coding.
> * Agents Toolkit CLI - app deployment helper. It sideloads, provisions Azure resources, handles manfiest/tenant plumbing, and keeps your dev, test, and prod environments in sync.

## Official documentation

- Official [Agents Toolkit documentation](/microsoft-365/developer/overview-m365-agents-toolkit?toc=%2Fmicrosoftteams%2Fplatform%2Ftoc.json&bc=%2Fmicrosoftteams%2Fplatform%2Fbreadcrumb%2Ftoc.json)

## Deployment and provisioning

Generally, you can use the toolkit to add required resources to Azure based on your app manifest setup. Agents Toolkit documents that in their documentation.

- [Add cloud resources and API connection](/microsoftteams/platform/toolkit/add-resource)

## Resources

- [Agents Toolkit Overview](/microsoftteams/platform/toolkit/teams-toolkit-fundamentals) - these extensive docs cover many topics related to Agents Toolkit, so please explore their documentation at your convenience.
- [Teams AI v2 CLI documentation](../developer-tools/cli.md) - includes instructions on adding toolkit configurations to your Teams AI v2 agent.