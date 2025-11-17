---
sidebar_label: Quickstart
title: Quickstart
zone_pivot_groups: dev-lang
description: Quick start guide for Teams SDK using the Teams CLI to create and run your first agent.
---
# Quickstart

Get started with Teams SDK quickly using the Teams CLI.

## Set up a new project

### Prerequisites


::: zone pivot="csharp"
- **.NET** v.8 or higher. Install or upgrade from [dotnet.microsoft.com](https://dotnet.microsoft.com/download).
::: zone-end

::: zone pivot="python"
- **Python** v3.12 or higher. Install or upgrade from [python.org/downloads](https://www.python.org/downloads/).
- **UV** v0.8.11 or higher. Install or upgrade from [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

import Admonition from '@theme/Admonition';

<Admonition type="info">
UV is a fast Python package installer and resolver. While you can use other package managers like pip, UV provides better performance and dependency resolution for Teams SDK projects.
</Admonition>
::: zone-end

::: zone pivot="typescript"
- **Node.js** v.20 or higher. Install or upgrade from [nodejs.org](https://nodejs.org/).
::: zone-end


## Instructions

### Use the Teams CLI

Use your terminal to run the Teams CLI using npx:

```sh
npx @microsoft/teams.cli --version
```

> [!NOTE]
> _The [Teams CLI](/developer-tools/cli) is a command-line tool that helps you create and manage Teams applications. It provides a set of commands to simplify the development process._<br /><br />
> Using `npx` allows you to run the Teams CLI without installing it globally. You can verify it works by running the version command above.

## Creating Your First Agent

Let's begin by creating a simple echo agent that responds to messages. Run:


::: zone pivot="csharp"
```sh
npx @microsoft/teams.cli@latest new csharp quote-agent --template echo
```
::: zone-end

::: zone pivot="python"
```sh
npx @microsoft/teams.cli@latest new python quote-agent --template echo
```
::: zone-end

::: zone pivot="typescript"
```sh
npx @microsoft/teams.cli@latest new typescript quote-agent --template echo
```
::: zone-end


This command:


::: zone pivot="csharp"
1. Creates a new directory called `Quote.Agent`.
2. Bootstraps the echo agent template files into your project directory.
3. Creates your agent's manifest files, including a `manifest.json` file and placeholder icons in the `Quote.Agent/appPackage` directory. The Teams [app manifest](/microsoftteams/platform/resources/schema/manifest-schema) is required for [sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload) the app into Teams.
::: zone-end

::: zone pivot="python,typescript"
1. Creates a new directory called `quote-agent`.
2. Bootstraps the echo agent template files into it under `quote-agent/src`.
3. Creates your agent's manifest files, including a `manifest.json` file and placeholder icons in the `quote-agent/appPackage` directory. The Teams [app manifest](/microsoftteams/platform/resources/schema/manifest-schema) is required for [sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload) the app into Teams.
::: zone-end


> The `echo` template creates a basic agent that repeats back any message it receives - perfect for learning the fundamentals.

## Running your agent


::: zone pivot="csharp"
1. Navigate to your new agent's directory:

```sh
cd Quote.Agent/Quote.Agent
```

2. Install the dependencies:

```sh
dotnet restore
```

3. Start the development server:

```sh
dotnet run
```
::: zone-end

::: zone pivot="python"
Navigate to your new agent's directory:

```sh
cd quote-agent
```

Start the development server:

```sh
uv run src\main.py
```
::: zone-end

::: zone pivot="typescript"
1. Navigate to your new agent's directory:

```sh
cd quote-agent
```

2. Install the dependencies:

```sh
npm install
```

3. Start the development server:

```sh
npm run dev
```
::: zone-end



::: zone pivot="csharp"
4. In the console, you should see a similar output:

```sh
[INFO] Microsoft.Hosting.Lifetime Now listening on: http://localhost:3978
[WARN] Echo.Microsoft.Teams.Plugins.AspNetCore.DevTools ⚠️  Devtools are not secure and should not be used production environments ⚠️
[INFO] Echo.Microsoft.Teams.Plugins.AspNetCore.DevTools Available at http://localhost:3979/devtools
[INFO] Microsoft.Hosting.Lifetime Application started. Press Ctrl+C to shut down.
[INFO] Microsoft.Hosting.Lifetime Hosting environment: Development
```
::: zone-end

::: zone pivot="python"
In the console, you should see a similar output:

```sh
[INFO] @teams/app Successfully initialized all plugins
[WARNING] @teams/app.DevToolsPlugin ⚠️ Devtools is not secure and should not be used in production environments ⚠️
[INFO] @teams/app.HttpPlugin Starting HTTP server on port 3978
INFO:     Started server process [6436]
INFO:     Waiting for application startup.
[INFO] @teams/app.DevToolsPlugin available at http://localhost:3979/devtools
[INFO] @teams/app.HttpPlugin listening on port 3978 🚀
[INFO] @teams/app Teams app started successfully
[INFO] @teams/app.DevToolsPlugin listening on port 3979 🚀
INFO:     Application startup complete..
INFO:     Uvicorn running on http://0.0.0.0:3979 (Press CTRL+C to quit)
```
::: zone-end

::: zone pivot="typescript"
4. In the console, you should see a similar output:

```sh
> quote-agent@0.0.0 dev
> npx nodemon -w "./src/**" -e ts --exec "node -r ts-node/register -r dotenv/config ./src/index.ts"

[nodemon] 3.1.9
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): src/**
[nodemon] watching extensions: ts
[nodemon] starting `node -r ts-node/register -r dotenv/config ./src/index.ts`
[WARN] @teams/app/devtools ⚠️  Devtools are not secure and should not be used production environments ⚠️
[INFO] @teams/app/http listening on port 3978 🚀
[INFO] @teams/app/devtools available at http://localhost:3979/devtools
```
::: zone-end


When the application starts, you'll see:

1. An HTTP server starting up (on port `3978`). This is the main server which handles incoming requests and serves the agent application.
2. A devtools server starting up (on port `3979`). This is a developer server that provides a web interface for debugging and testing your agent quickly, without having to deploy it to Teams.

> [!NOTE]
> The DevTools server runs on a separate port to avoid conflicts with your main application server. This allows you to test your agent locally while keeping the main server available for Teams integration.

Now, navigate to the devtools server by opening your browser and navigating to [http://localhost:3979/devtools](http://localhost:3979/devtools). You should see a simple interface where you can interact with your agent. Try sending it a message!

![Screenshot of DevTools showing user prompt 'hello!' and agent response 'you said hello!'.](~/assets/screenshots/devtools-echo-chat.png)

## Next steps

After creating and running your first agent, read about [the code basics](code-basics.md) to better understand its components and structure.

Otherwise, if you want to run your agent in Teams, you can check out the [Running in Teams](running-in-teams.md) guide.

## Resources

- [Teams CLI documentation](/developer-tools/cli)
- [Teams DevTools documentation](/developer-tools/devtools)
- [Teams manifest schema](/microsoftteams/platform/resources/schema/manifest-schema)
- [Teams sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload)
