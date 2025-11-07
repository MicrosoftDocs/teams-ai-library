---
title: Microsoft 365 Agents Toolkit
description: Automate Teams app development with Microsoft 365 Agents Toolkit for manifest management, sideloading, and deployment.
ms.topic: how-to
ms.date: 09/26/2025
---

# Microsoft 365 Agents Toolkit

Microsoft 365 Agents Toolkit provides a powerful VS Code extension and CLI tool that helps automate important tasks like manifest management, sideloading, deployment, and provisioning. If you encounter any issues while using it (such as problems with the extension, running apps, deployment and provisioning, or debugging via F5), please report them in the [Agents Toolkit GitHub repository](https://github.com/OfficeDev/microsoft-365-agents-toolkit).

## Installing Agents Toolkit

Agents Toolkit can be installed as an extension and CLI. Please see the documentation linked below.

- [Installing Agents Toolkit extension](/microsoftteams/platform/toolkit/install-teams-toolkit)
- [Installing Agents Toolkit CLI](/microsoftteams/platform/toolkit/microsoft-365-agents-toolkit-cli)

> [!NOTE]
> * [Teams SDK CLI](~/developer-tools/cli.md) - helper for the new v2 library. It scaffolds agents, wires in deep Teams features (Adaptive Cards, Conversation History, Memory...etc), and adds all the config files you need while you're coding.
> * Agents Toolkit CLI - app deployment helper. It sideloads, provisions Azure resources, handles manfiest/tenant plumbing, and keeps your dev, test, and prod environments in sync.

## Official documentation

Refer to the official [Microsoft 365 Agents Toolkit documentation](/microsoft-365/developer/overview-m365-agents-toolkit?toc=%2Fmicrosoftteams%2Fplatform%2Ftoc.json&bc=%2Fmicrosoftteams%2Fplatform%2Fbreadcrumb%2Ftoc.json) on Microsoft Learn.

## Deployment and provisioning

Generally, you can use the toolkit to add required resources to Azure based on your app manifest setup. For more, see [Add cloud resources and API connection](/microsoftteams/platform/toolkit/add-resource).

## Resources

- [Microsoft 365 Agents Toolkit](/microsoftteams/platform/toolkit/teams-toolkit-fundamentals): Extensive documentation covering usage and supported scenarios of Agents Toolkit.
- [Teams SDK CLI documentation](~/developer-tools/cli.md): Instructions on adding Agents Toolkit configurations to your Teams SDK agent.
