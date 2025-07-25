---
title: Agent-to-Agent Protocol (preview) (TypeScript)
description: Overview of the experimental A2A (Agent-to-Agent) protocol for enabling programmatic communication between AI agents.
ms.topic: overview
ms.date: 07/16/2025
---

# A2A (Agent-to-Agent) Protocol (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

> [!CAUTION]
> This package is experimental and the A2A protocol is still in early development. Use with caution in production environments.

[What is A2A?](https://a2a-protocol.org/)

A2A (Agent-to-Agent) is a protocol designed to enable agents to communicate and collaborate programmatically. This package allows you to integrate the A2A protocol into your Teams app, making your agent accessible to other A2A clients and enabling your app to interact with other A2A servers.

Install the package:

```bash
npm install @microsoft/teams.a2a@preview
```

## What does this package do?

-   Enables your Teams agent to act as an A2A server, exposing its capabilities to other agents.
-   Allows your Teams app to proactively reach out to other A2A servers as a client.

## High-level Architecture

### A2A Server
:::image type="content" source="~/assets/diagrams/overview-1.png" alt-text="alt-text for overview-1.png":::

### A2A Client

:::image type="content" source="~/assets/diagrams/overview-2.png" alt-text="alt-text for overview-2.png":::