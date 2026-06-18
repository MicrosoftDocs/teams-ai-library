---
title: 'AI Integrations'
description: 'Plug AI agents into Teams Python apps  Microsoft Agent Framework for reasoning, MCP for human-in-the-loop, and A2A for bot-to-bot collaboration.'
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 06/11/2026
---

# AI Integrations

::: zone pivot="csharp,typescript"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="python"
Microsoft Teams SDK provides the platform and conversational interface for your app while remaining agnostic to the underlying intelligence. You can choose any AI framework, model, or protocol that suits your scenario and integrate it into your message handlers. The samples below walk through a few common ways to do that, from a single bot reasoning with an agent to multiple bots collaborating with each other.

- **[Building an agent using Microsoft Agent Framework in Teams](./build-agent-maf.md)** - creates the core agent and basic Teams integration, adds local and remote MCP tools, streams responses into Teams, and maintains per-conversation memory using sessions.
- **[Enhancing the Teams Experience using Teams SDK](./teams-enhancements.md)** - builds on the base integration by adding richer conversational features such as suggested follow-up prompts, inline citations, Adaptive Cards, and structured feedback handling.
- **[Exposing Teams to AI Agents (MCP)](./mcp-server.md)**  turn your bot into an [MCP](https://modelcontextprotocol.io/introduction) server so external agents can reach real users through Teams chat with tools like `notify`, `ask`, and `request_approval`. Useful for human-in-the-loop workflows.
- **[Bot-to-Bot with A2A](./a2a.md)**  two Teams bots, each with its own agent and human operator, coordinate with each other over the [Agent2Agent](https://a2a-protocol.org/) protocol, with human-in-the-loop (HITL) support when peer requests require human input.

All samples are available in the [`microsoft/teams.py` examples](https://github.com/microsoft/teams.py/tree/main/examples).
::: zone-end
