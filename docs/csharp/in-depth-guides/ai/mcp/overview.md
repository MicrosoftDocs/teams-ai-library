---
title: MCP (preview) (C#)
description: Overview of MCP functionality in the Microsoft Teams AI Library for C#.
ms.topic: overview
ms.date: 07/16/2025
---
# MCP (preview) (C#)

[This article is prerelease documentation and is subject to change.]

Teams AI Library has optional packages which support the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) as a service or client. This allows you to use MCP to call functions and tools in your application. 

MCP servers and MCP clients dynamically load function definitions and tools.

When building Servers, this could mean that you can introduce new tools as part of your application, and the MCP clients that are connected to it will automatically start consuming those tools.

When building Clients, this could mean that you can connect to other MCP servers and your application has the flexibility to improve as the MCP servers its connected to evolve over time.

> [!TIP]
> The guides here can be used to build a server and a client that can leverage each other. That means you can build a server that has the ability to do complex things for the client agent.