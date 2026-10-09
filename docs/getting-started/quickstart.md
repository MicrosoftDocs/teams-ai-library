---
title: Quickstart
description: Quick start guide for Teams SDK using the Teams Developer CLI to create and run your first agent.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---

# Quickstart

Get started with Teams SDK quickly using the Teams Developer CLI.

## Set up a new project

### Prerequisites


::: zone pivot="csharp"
- **.NET** v8 or higher. Install or upgrade from [dotnet.microsoft.com](https://dotnet.microsoft.com/en-us/download).
::: zone-end

::: zone pivot="python"
- **Python** v3.12 or higher. Install or upgrade from [python.org/downloads](https://www.python.org/downloads/).
::: zone-end

::: zone pivot="typescript"
- **Node.js** v.22.12 or higher. Install or upgrade from [nodejs.org](https://nodejs.org/).
::: zone-end


## Instructions

### Install the Teams Developer CLI

Install `teams` globally:

```sh
npm install -g @microsoft/teams.cli
teams --version
```

> [!NOTE]
> The [Teams Developer CLI](../developer-tools/cli.md) is the command-line tool for scaffolding, registering, and managing Teams apps.

## Creating Your First Agent

Let's begin by creating a simple echo agent that responds to messages. Run:


::: zone pivot="csharp"
```sh
teams project new csharp quote-agent --template echo
```
::: zone-end

::: zone pivot="python"
```sh
teams project new python quote-agent --template echo
```
::: zone-end

::: zone pivot="typescript"
```sh
teams project new typescript quote-agent --template echo
```
::: zone-end


This command:


::: zone pivot="csharp"
1. Creates a new directory called `QuoteAgent`.
2. Bootstraps the echo agent template files into your project directory.
::: zone-end

::: zone pivot="python,typescript"
1. Creates a new directory called `quote-agent`.
2. Bootstraps the echo agent template files into it under `quote-agent/src`.
::: zone-end


> The `echo` template creates a basic agent that repeats back any message it receives - perfect for learning the fundamentals.

## Running your agent


::: zone pivot="csharp"
1. Navigate to your new agent's directory:

```sh
cd QuoteAgent/QuoteAgent
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

Create and activate a virtual environment, then install the dependencies:

```sh
python -m venv .venv
# Activate it: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)
pip install -e .
```

Start the development server:

```sh
python src/main.py
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
1. In the console, you should see a similar output:


```sh
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:3978
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
```
::: zone-end

::: zone pivot="python"
In the console, you should see a similar output:

```sh
[INFO] @teams/app Successfully initialized all plugins
[INFO] @teams/app.HttpPlugin Starting HTTP server on port 3978
INFO:     Started server process [6436]
INFO:     Waiting for application startup.
[INFO] @teams/app.HttpPlugin listening on port 3978 🚀
[INFO] @teams/app Teams app started successfully
INFO:     Application startup complete..
INFO:     Uvicorn running on http://0.0.0.0:3978 (Press CTRL+C to quit)
```
::: zone-end

::: zone pivot="typescript"
4. In the console, you should see a similar output:

```sh
> quote-agent@0.0.0 dev
> tsx watch -r dotenv/config src/index.ts

[WARN] @teams/app No credentials configured and dangerouslyAllowUnauthenticatedRequests is not enabled. All incoming requests will be rejected. Configure client authentication to securely receive messages, or set dangerouslyAllowUnauthenticatedRequests: true for local development.
[INFO] @teams/app listening on port 3978 🚀
```
::: zone-end



::: zone pivot="csharp"
The HTTP server is now listening on port `3978`. To test your agent locally without sideloading it into Teams, use the **[Microsoft 365 Agents Playground](../developer-tools/agents-playground/overview.md)**.

# [SDK 2.0 (Legacy)](#tab/legacy)
The playground sends unauthenticated requests, which a default `builder.AddTeams()` rejects when no credentials are configured. For local testing, enable `skipAuth` so your agent accepts them:

```csharp title="Program.cs"
builder.AddTeams(skipAuth: true);
```

> [!WARNING]
> Only use `skipAuth` for local development — never in production, as it disables inbound request authentication.

---

# [SDK 2.1 (current)](#tab/core)
The playground sends unauthenticated requests, and SDK 2.1 rejects them by default. For local testing, enable `DangerouslyAllowUnauthenticatedRequests` in your launch settings:

```json title="Properties/launchSettings.json"
{
  "profiles": {
    "https": {
      "environmentVariables": {
        "AzureAd__DangerouslyAllowUnauthenticatedRequests": "true"
      }
    }
  }
}
```

> [!WARNING]
> Only use `DangerouslyAllowUnauthenticatedRequests` for local development — never in production, as it disables inbound request authentication.

Install the playground globally:

```sh
npm install -g @microsoft/m365agentsplayground
```

Then, with your agent still running, open a second terminal and launch the playground pointed at your agent:

```sh
agentsplayground -e http://localhost:3978/api/messages -c emulator
```

The playground opens at [http://localhost:56150](http://localhost:56150). Send a message in the compose box and your agent's reply renders inline.

:::image type="content" source="~/assets/screenshots/agents-playground-echo-chat.png" alt-text="Microsoft 365 Agents Playground showing a user message 'hello!' and an agent reply that says 'you said hello!'." lightbox="~/assets/screenshots/agents-playground-echo-chat.png" :::
::: zone-end

::: zone pivot="python"
The HTTP server is now listening on port `3978`. To test your agent locally without sideloading it into Teams, use the **[Microsoft 365 Agents Playground](../developer-tools/agents-playground/overview.md)**.

The playground sends unauthenticated requests, so a default `App()` will reject them (you'll see the `No credentials configured` warning above). For local testing, enable `dangerously_allow_unauthenticated_requests` so your agent accepts them:

```python title="src/main.py"
app = App(dangerously_allow_unauthenticated_requests=True)
```

> [!WARNING]
> Only use `dangerously_allow_unauthenticated_requests` for local development — never in production, as it disables inbound request authentication.

Install the playground globally:

```sh
npm install -g @microsoft/m365agentsplayground
```

Then, with your agent still running, open a second terminal and launch the playground pointed at your agent:

```sh
agentsplayground -e http://localhost:3978/api/messages -c emulator
```

The playground opens at [http://localhost:56150](http://localhost:56150). Send a message in the compose box and your agent's reply renders inline.

:::image type="content" source="~/assets/screenshots/agents-playground-echo-chat.png" alt-text="Microsoft 365 Agents Playground showing a user message 'hello!' and an agent reply that says 'you said hello!'." lightbox="~/assets/screenshots/agents-playground-echo-chat.png" :::
::: zone-end

::: zone pivot="typescript"
The HTTP server is now listening on port `3978`. To test your agent locally without sideloading it into Teams, use the **[Microsoft 365 Agents Playground](../developer-tools/agents-playground/overview.md)**.

The playground sends unauthenticated requests, so a default `new App()` will reject them (you'll see the `No credentials configured` warning above). For local testing, enable `dangerouslyAllowUnauthenticatedRequests` so your agent accepts them:

```typescript title="src/index.ts"
const app = new App({ dangerouslyAllowUnauthenticatedRequests: true });
```

> [!WARNING]
> Only use `dangerouslyAllowUnauthenticatedRequests` for local development — never in production, as it disables inbound request authentication.

Install the playground globally:

```sh
npm install -g @microsoft/m365agentsplayground
```

Then, with your agent still running, open a second terminal and launch the playground pointed at your agent:

```sh
agentsplayground -e http://localhost:3978/api/messages -c emulator
```

The playground opens at [http://localhost:56150](http://localhost:56150). Send a message in the compose box and your agent's reply renders inline.

:::image type="content" source="~/assets/screenshots/agents-playground-echo-chat.png" alt-text="Microsoft 365 Agents Playground showing a user message 'hello!' and an agent reply that says 'you said hello!'." lightbox="~/assets/screenshots/agents-playground-echo-chat.png" :::
::: zone-end


## Add to an Existing Project

If you already have a project and want to add Teams support, install the SDK directly:


::: zone pivot="csharp"
```sh
dotnet add package Microsoft.Teams.Apps
```
// Then register the Teams services on your existing app.
::: zone-end

::: zone pivot="python"
```sh
pip install microsoft-teams-apps
```
Then initialize the Teams app with your existing server:
::: zone-end

::: zone pivot="typescript"
```sh
npm i @microsoft/teams.apps
```
Then initialize the Teams app with your existing server:
::: zone-end



::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Apps;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddTeamsBotApplication();
var app = builder.Build();

// Maps POST /api/messages onto your existing ASP.NET Core app
TeamsBotApplication teams = app.UseTeamsBotApplication();

teams.OnMessage(async (context, cancellationToken) =>
{
    await context.SendAsync($"you said: {context.Activity.Text}", cancellationToken);
});

app.Run();
```
`app.UseTeamsBotApplication()` registers the Teams endpoint onto your existing ASP.NET Core app.
::: zone-end

::: zone pivot="python"
```python
import asyncio
import uvicorn
from fastapi import FastAPI
# highlight-next-line
from microsoft_teams.apps import App, FastAPIAdapter

# Your existing FastAPI app
my_fastapi = FastAPI()

# highlight-start
# Wrap your app in an adapter and create the Teams app
adapter = FastAPIAdapter(app=my_fastapi)
app = App(http_server_adapter=adapter)

@app.on_message
async def handle_message(ctx):
    await ctx.send(f"You said: {ctx.activity.text}")
# highlight-end

async def main():
    # highlight-next-line
    await app.initialize()  # Register the Teams endpoint (does not start a server)

    # Start your server as usual
    config = uvicorn.Config(app=my_fastapi, host="0.0.0.0", port=3978)
    server = uvicorn.Server(config)
    await server.serve()

asyncio.run(main())
```
`app.initialize()` registers the Teams endpoint on your server without starting a new one — you keep full control of your server lifecycle.
::: zone-end

::: zone pivot="typescript"
```typescript
import http from 'http';
import express from 'express';
// highlight-next-line
import { App, ExpressAdapter } from '@microsoft/teams.apps';

// Your existing Express server
const expressApp = express();
const server = http.createServer(expressApp);

// highlight-start
// Wrap your server in an adapter and create the Teams app
const adapter = new ExpressAdapter(server);
const app = new App({ httpServerAdapter: adapter });

app.on('message', async ({ send, activity }) => {
  await send(`You said: ${activity.text}`);
});

// Register the Teams endpoint on your server (does not start it)
await app.initialize();
// highlight-end

// Start your server as usual
server.listen(3978);
```
`app.initialize()` registers the Teams endpoint on your server without starting a new one — you keep full control of your server lifecycle.
::: zone-end



::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python,typescript"
See the [HTTP Server guide](../in-depth-guides/server/http-server.md) for full details on adapters and custom server setups.
::: zone-end


## Next steps

After creating and running your first agent, read about [the code basics](code-basics.md) to better understand its components and structure.

Otherwise, if you want to run your agent in Teams, you can check out the [Running in Teams](running-in-teams/overview.md) guide.

## Resources

- [Teams Developer CLI documentation](../developer-tools/cli.md)

::: zone pivot="csharp,python,typescript"
- [Microsoft 365 Agents Playground](../developer-tools/agents-playground/overview.md)
::: zone-end

- [Teams manifest schema](/microsoftteams/platform/resources/schema/manifest-schema)
- [Teams sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload)
