---
title: MCP Client (C#)
description: Learn about MCP Client (C#)
ms.topic: how-to
ms.date: 05/17/2025
---
# MCP Client (C#)

You are able to leverage other MCP servers that expose tools via the SSE protocol as part of your application. This allows your AI agent to use remote tools to accomplish tasks.

> [!NOTE]
> Take a look at [Function calling](../function-calling.md) to understand how the `ChatPrompt` leverages tools to enhance the LLM's capabilities. MCP extends this functionality by allowing remote tools, that may or may not be developed or maintained by you, to be used by your application.

## Remote MCP Server

The first thing that's needed is access to a **remote** MCP server. MCP Servers (at present) come using two main types protocols:

1. StandardIO - This is a _local_ MCP server, which runs on your machine. An MCP client may connect to this server, and use standard input and outputs to communicate with it. Since our application is running remotely, this is not something that we want to use
2. SSE - This is a _remote_ MCP server. An MCP client may send it requests and the server responds in the expected MCP protocol.

For hooking up to your a valid SSE server, you will need to know the URL of the server, and if applicable, and keys that must be included as part of the header.

## MCP Client Plugin

The `MCPClientPlugin` (from `@microsoft/teams.mcpclient` package) integrates directly with the `ChatPrompt` object as a plugin. When the `ChatPrompt`'s `send` function is called, it calls the external MCP server and loads up all the tools that are available to it.

Once loaded, it treats these tools like any functions that are available to the `ChatPrompt` object. If the LLM then decides to call one of these remote MCP tools, the MCP Client plugin will call the remote MCP server and return the result back to the LLM. The LLM can then use this result in its response.

```typescript
const logger = new ConsoleLogger('mcp-client', { level: 'debug' });
const prompt = new ChatPrompt(
  {
    instructions:
      "You are a helpful assistant. You MUST use tool calls to do all your work.",
    model: new OpenAIChatModel({
      model: "gpt-4o-mini",
      apiKey: process.env.OPENAI_API_KEY,
    }),
    logger
  },
  // Tell the prompt that the plugin needs to be used
  // Here you may also pass in additional configurations such as
  // a tool-cache, which can be used to limit the tools that are used
  // or improve performance
  [new McpClientPlugin({ logger })],
)
  // Here we are saying you can use any tool from localhost:3000/mcp
  // (that is the URL for the server we built using the mcp plugin)
  .usePlugin("mcpClient", { url: "http://localhost:3000/mcp" })
  // Alternatively, you can use a different server hosted somewhere else
  // Here we are using the mcp server hosted on an Azure Function
  .usePlugin("mcpClient", {
    url: "https://aiacceleratormcp.azurewebsites.net/runtime/webhooks/mcp/sse",
    params: {
      headers: {
        // If your server requires authentication, you can pass in Bearer or other
        // authentication headers here
        "x-functions-key": process.env.AZURE_FUNCTION_KEY!,
      },
    },
  });

app.on("message", async ({ send, activity }) => {
  await send({ type: "typing" });

  const result = await prompt.send(activity.text);
  if (result.content) {
    await send(result.content);
  }
});

```

In this example, we augment the `ChatPrompt` with a few remote MCP Servers.

> [!NOTE]
> Feel free to build an MCP Server in a different agent using the [MCP Server Guide](./mcp-server.md). Or you can quickly set up an MCP server using [Azure Functions](https://techcommunity.microsoft.com/blog/appsonazureblog/build-ai-agent-tools-using-remote-mcp-with-azure-functions/4401059).

:::image type="content" source="~assets/screenshots/mcp-client-pokemon.gif" alt-text="MCP Client in Devtools":::

In this example, our MCP server is a Pokemon API and our client knows how to call it. The LLM is able to call the `getPokemon` function exposed by the server and return the result back to the user.