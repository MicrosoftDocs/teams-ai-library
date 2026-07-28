---
title: YZ Microsoft 365 Agents Playground
description: Test your Teams agent locally with the Microsoft 365 Agents Playground CLI.
ms.topic: how-to
ms.date: 07/27/2026
---

# YZ Microsoft 365 Agents Playground

The Microsoft 365 Agents Playground is a local testing tool for agents built with the Teams SDK. It lets you chat with your agent, mock activities, and inspect requests and responses without sideloading into Teams.

:::image type="content" source="~/assets/screenshots/agents-playground-blank.png" alt-text="Microsoft 365 Agents Playground showing the welcome page with a sidebar listing Personal Chat, Group Chat, and Teams Channels, and a 'Type a message' compose box at the bottom." lightbox="~/assets/screenshots/agents-playground-blank.png" :::

## Install

### Option 1: npm (recommended)

```bash

npm install -g @microsoft/m365agentsplayground
```

### Option 2: Standalone binary

```bash

winget install agentsplayground
```

For other platforms and full install options, see the [Microsoft Learn guide](/microsoft-365/agents-sdk/test-with-toolkit-project).

## Migrating from DevTools

If your agent previously used `DevtoolsPlugin` from `@microsoft/teams.dev`, remove it from your `App` configuration. The Playground is a separate CLI tool and does not need a plugin in your code.

You can also remove `@microsoft/teams.dev` from your `package.json` after deleting `DevtoolsPlugin`. The Playground is installed separately as a CLI tool, not as a project dependency.

The Playground sends requests without a Bot Framework JWT, so your agent needs to accept unauthenticated requests on `/api/messages`.

By default the SDK **rejects** unauthenticated requests, so a freshly scaffolded agent rejects every request the Playground sends and logs:

> [!WARNING]
>
> No credentials configured and skipAuth is not enabled. All incoming requests will be rejected. Configure client authentication to securely receive messages, or set skipAuth for local development.

To accept the Playground's requests during local development, enable `skipAuth` on your app:

# [TypeScript](#tab/typescript)
```typescript
title="src/index.ts"
const app = new App({ skipAuth: true });
```

---

# [C#](#tab/csharp)
```csharp
title="Program.cs"
builder.AddTeams(skipAuth: true);
```

---

# [Python](#tab/python)
```python
title="src/main.py"
app = App(skip_auth=True)
```

> [!WARNING]
>
> Only use `skipAuth` for local development a never in production, as it disables inbound request authentication.

### Why this is needed

`DevtoolsPlugin` previously bypassed JWT validation implicitly because it ran in-process and never went through `/api/messages` over HTTP. The Playground sends real HTTP requests, so the bot's JWT validator runs unless `skipAuth` is enabled.

## Launch

Start your agent locally (default port `3978`), then run:

```bash

agentsplayground -e http://localhost:3978/api/messages -c msteams
```

The playground opens at [http://localhost:56150](http://localhost:56150).

### Common flags

- `-e, --app-endpoint` - your agent's endpoint, e.g. `http://localhost:3978/api/messages`
- `-c, --channel-id` a `emulator`, `webchat`, `msteams`, `directline`, or `agents`
- `--client-id`, `--client-secret`, `--tenant-id` a credentials when your agent requires authentication
- `-p, --port` a port for the playground UI (default `56150`)

Run `agentsplayground --help` for the full list.

## Test your agent

Type a message in the compose box and send it. Your agent's reply renders inline.

:::image type="content" source="~/assets/screenshots/agents-playground-echo-chat.png" alt-text="Microsoft 365 Agents Playground showing a user message hello and an agent reply you said hello." lightbox="~/assets/screenshots/agents-playground-echo-chat.png" :::

Use the **Mock an Activity** menu to send custom activity types (membership changes, invokes, message reactions, and more). Use the **Debug Options** menu to control delivery mode and logging. The **Log Panel** (toggle from the top right) shows the HTTP exchange between the playground and your agent.

## Learn more

- [Test your agent locally in Microsoft 365 Agents Playground](/microsoft-365/agents-sdk/test-with-toolkit-project) a full Microsoft Learn guide
- [Microsoft 365 Agents SDK](/microsoft-365/agents-sdk/)

