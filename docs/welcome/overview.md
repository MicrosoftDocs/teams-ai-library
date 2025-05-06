---
title: Teams AI Library v2 overview (preview)
description: Learn about Teams AI Library v2 (preview)
ms.topic: how-to
ms.date: 05/05/2025
---
# Teams AI Library v2

Teams AI Library v2 is a suite of packages used to develop on Microsoft Teams. Rebuilt from the ground up with improved developer experience in mind, it's never been easier to build powerful agents and applications for the hundreds of millions Microsoft Teams users.

:::image type="content" source="~/assets/teams-ai-library-v1-vs-v2.png" alt-text="Comparison of Teams AI Library v1 vs. v2 showing that the v2 version encapsulates Botbuilder, Teams AI v1, Grpah, Adaptive Cards, MSAL, and Teams JS functionality":::

## Quickstart

The Teams CLI makes it easy to bootstrap your first agent. First, install the CLI via NPM:

<!-- langtabs-start -->
```sh
npm install -g @microsoft/teams.cli@preview
```
<!-- langtabs-end -->

Next, use the CLI to create your agent:

<!-- langtabs-start -->
```sh
teams new quote-agent --template echo
```
<!-- langtabs-end -->

For more information, follow our [quick start guide](../getting-started/quickstart.md).

## Overview

Microsoft Teams has a robust developer ecosystem with a broad suite of capabilities, now unified via Teams AI v2. Whether you are building [AI-powered agents](../in-depth-guides/ai/overview.md), [message extensions](../in-depth-guides/message-extensions/overview.md), embedded web applications, or Graph, Teams AI v2 has you covered.

Here is a simple example, which responds to incoming messages with information retrieved from Graph.

<!-- langtabs-start -->
```typescript
import { App } from '@microsoft/teams.apps';
import { DevtoolsPlugin } from '@microsoft/teams.dev';

const app = new App({
  plugins: [new DevtoolsPlugin()],
});

// Listen for incoming messages
app.on('message', async ({ api, isSignedIn, send, signin }) => {
  if (!isSignedIn) {
    await signin(); // initiates Entra login flow
    return;
  }
  const me = await api.user.me.get();
  await send(`Hello, ${me.displayName} from Earth!`);
});

// Start your application
(async () => {
  await app.start();
})();
```
<!-- langtabs-end -->

## ⭐ What's new?

### Streamlined Developer Experience

We’ve refined the developer experience so you can concentrate on building your app’s logic — not wrestling with integrations.

### Effortless Integration

We’ve simplified complex integration workflows to help you deliver a richer, more seamless user experience.

### Accelerate Your Workflow

Get your application up and running in under 30 seconds with our lightning-fast CLI—so you can spend more time on what really matters.

## 🔎 Navigation Tips

We encourage you to use the left sidebar to navigate to your desired section.

Can't find what you're searching for? Use the search button above.