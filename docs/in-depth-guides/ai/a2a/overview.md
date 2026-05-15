---
title: A2A (Agent-to-Agent) Protocol
description: Overview of the experimental A2A (Agent-to-Agent) protocol for enabling programmatic communication between AI agents.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 05/15/2026
---
# A2A (Agent-to-Agent) Protocol

::: zone pivot="csharp,python"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="typescript"
> [!NOTE]
> This package wraps the official [A2A SDK](https://github.com/a2aproject/a2a-js) for both server and client.
::: zone-end

::: zone pivot="typescript"
[What is A2A?](https://a2a-protocol.org/latest/)

A2A (Agent-to-Agent) is a protocol designed to enable agents to communicate and collaborate programmatically. This package allows you to integrate the A2A protocol into your Teams app, making your agent accessible to other A2A clients and enabling your app to interact with other A2A servers.
::: zone-end

::: zone pivot="typescript"
Install the package:

```bash
npm install @microsoft/teams.a2a
```
::: zone-end

::: zone pivot="typescript"
## What does this package do?

- **A2A Server**: Enables your Teams agent to act as an A2A server, exposing its capabilities to other agents through the `/a2a` endpoint and serving an agent card at `/a2a/.well-known/agent-card.json`.
- **A2A Client**: Allows your Teams app to proactively reach out to other A2A servers as a client, either through direct `AgentManager` usage or integrated with `ChatPrompt` for LLM-driven interactions.

## High-level Architecture

### A2A Server

:::image type="content" source="~/assets/diagrams/a2a-overview.png" alt-text="Flowchart showing A2A server architecture with TeamsApp and A2APlugin handling task/send messages from an external client" lightbox="~/assets/diagrams/a2a-overview.png":::


### A2A Client

:::image type="content" source="~/assets/diagrams/a2a-overview-2.png" alt-text="Flowchart showing A2A client architecture with TeamsApp and A2AClientPlugin communicating with an external A2A server" lightbox="~/assets/diagrams/a2a-overview-2.png":::


## Protocol Details

For detailed information about the A2A protocol, including agent card structure, message formats, and protocol specifications, see the official [A2A Protocol Documentation](https://a2a-protocol.org/latest/specification/).
::: zone-end