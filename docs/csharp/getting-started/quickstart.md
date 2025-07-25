---
title: Quickstart (preview) (C#)
description: Quickly build your first Teams application with the Microsoft Teams AI Library for C#.
ms.topic: get-started
ms.date: 07/16/2025
---

# Quickstart (preview) (C#)

[This article is prerelease documentation and is subject to change.]

Get started with Teams AI Library (v2) quickly using the Teams CLI.

## Set up a new project

### Prerequisites

- **.NET** v.8 or higher. Install or upgrade from [dotnet.microsoft.com](https://dotnet.microsoft.com/download).

## Instructions

### Install the Teams CLI

Use your terminal to install the Teams CLI globally using npm:


```sh
npm install -g @microsoft/teams.cli@preview
```


> [!NOTE]
> _The [Teams CLI](../../developer-tools/cli.md) is a command-line tool that helps you create and manage Teams applications. It provides a set of commands to simplify the development process._<br /><br />
> After installation, you can run `teams --version` to verify the installation.

## Creating Your First Agent

Let's create a simple echo agent that responds to messages. Run:


```sh
teams new csharp quote-agent --template echo
```


This command:

1. Creates a new directory called `Quote.Agent`.
2. Bootstraps the echo agent template files into your project directory.
3. Creates your agent's manifest files, including a `manifest.json` file and placeholder icons in the `Quote.Agent/appPackage` directory. The Teams [app manifest](/microsoft-365/extensibility/schema) is required for [sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload) the app into Teams.

> The `echo` template creates a basic agent that repeats back any message it receives - perfect for learning the fundamentals.

## Running your agent

Navigate to your new agent's directory:


```sh
cd Quote.Agent/Quote.Agent
```


Install the dependencies:


```sh
dotnet restore
```


Start the development server:


```sh
dotnet run
```


In the console, you should see a similar output:


```sh
[INFO] Microsoft.Hosting.Lifetime Now listening on: http://localhost:3978
[WARN] Echo.Microsoft.Teams.Plugins.AspNetCore.DevTools ⚠️  Devtools are not secure and should not be used production environments ⚠️
[INFO] Echo.Microsoft.Teams.Plugins.AspNetCore.DevTools Available at http://localhost:3978/devtools
[INFO] Microsoft.Hosting.Lifetime Application started. Press Ctrl+C to shut down.
[INFO] Microsoft.Hosting.Lifetime Hosting environment: Development
```


When the application starts, you'll see:

1. An http server starting up (on port 3978). This is the main server which handles incoming requests and serves the agent application.
2. A devtools server starting up. This is a developer server that provides a web interface for debugging and testing your agent quickly, without having to deploy it to Teams.

Let's navigate to the devtools server. Open your browser and head to [http://localhost:3978/devtools](http://localhost:3978/devtools). You should see a simple interface where you can interact with your agent. Send it a message!

:::image type="content" source="~/assets/screenshots/devtools-echo-chat.png" alt-text="devtools":::

## Next steps

Now that you have your first agent running, learn about [the code basics](code-basics.md) to understand its components and structure.

Otherwise, if you want to run your agent in Teams, check out the [Running in Teams](running-in-teams.md) guide.

## Resources

- [Teams CLI documentation](../../developer-tools/cli.md)
- [Teams DevTools documentation](../../developer-tools/devtools/overview.md)
- [Teams manifest schema](/microsoft-365/extensibility/schema)
- [Teams sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload)