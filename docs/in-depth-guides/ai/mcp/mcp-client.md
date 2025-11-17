---
sidebar_position: 2
sidebar_label: MCP Client
title: MCP Client
summary: How to implement an MCP client to leverage remote MCP servers and their tools in your AI agent application.
zone_pivot_groups: dev-lang
---

# MCP Client

::: zone pivot="csharp,python"
You are able to leverage other MCP servers that expose tools via the SSE protocol as part of your application. This allows your AI agent to use remote tools to accomplish tasks.
::: zone-end

::: zone pivot="typescript"
You are able to leverage other MCP servers that expose tools via the Streamable HTTP protocol as part of your application. This allows your AI agent to use remote tools to accomplish tasks.
::: zone-end


::: zone pivot="csharp"
Install it to your application:

```bash
dotnet add package Microsoft.Teams.Plugins.External.McpClient --prerelease
```
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
Install it to your application:

```bash
npm install @microsoft/teams.mcpclient
```
::: zone-end


:::info
Take a look at [Function calling](../function-calling) to understand how the `ChatPrompt` leverages tools to enhance the LLM's capabilities. MCP extends this functionality by allowing remote tools, that may or may not be developed or maintained by you, to be used by your application.
:::

## Remote MCP Server

The first thing that's needed is access to a **remote** MCP server. MCP Servers (at present) come using two main types protocols:

::: zone pivot="csharp"
1. StandardIO - This is a _local_ MCP server, which runs on your machine. An MCP client may connect to this server, and use standard input and outputs to communicate with it. Since our application is running remotely, this is not something that we want to use
2. SSE - This is a _remote_ MCP server. An MCP client may
   send it requests and the server responds in the expected MCP protocol.
::: zone-end

::: zone pivot="python"
1. StandardIO - This is a _local_ MCP server, which runs on your machine. An MCP client may connect to this server, and use standard input and outputs to communicate with it. Since our application is running remotely, this is not something that we want to use
2. StreamableHttp/SSE - This is a _remote_ MCP server. An MCP client may
   send it requests and the server responds in the expected MCP protocol.
::: zone-end

::: zone pivot="typescript"
1. StandardIO - This is a _local_ MCP server, which runs on your machine. An MCP client may connect to this server, and use standard input and outputs to communicate with it. Since our application is running remotely, this is not something that we want to use
2. Streamable HTTP/SSE - This is a _remote_ MCP server. An MCP client may
   send it requests and the server responds in the expected MCP protocol.
::: zone-end

::: zone pivot="csharp,python"
For hooking up to your a valid SSE server, you will need to know the URL of the server, and if applicable, <LanguageInclude section="auth-requirements" /> that must be included as part of the header.
::: zone-end

::: zone pivot="typescript"
For hooking up to your valid remote server, you will need to know the URL of the server, and if applicable, <LanguageInclude section="auth-requirements" /> that must be included as part of the header.
::: zone-end

For hooking up to your <LanguageInclude section="server-setup" /> server, you will need to know the URL of the server, and if applicable, <LanguageInclude section="auth-requirements" /> that must be included as part of the header.

::: zone pivot="csharp,typescript"
For hooking up to your <LanguageInclude section="server-setup" /> server, you will need to know the URL of the server, and if applicable, and keys that must be included as part of the header.
::: zone-end

::: zone pivot="python"
For hooking up to your <LanguageInclude section="server-setup" /> server, you will need to know the URL of the server, and if applicable, any keys that must be included as part of the header.
::: zone-end

## MCP Client Plugin

::: zone pivot="csharp"
The `MCPClientPlugin` (from `Microsoft.Teams.Plugins.External.McpClient` package) integrates directly with the `ChatPrompt` <LanguageInclude section="integration-method" />. When the `ChatPrompt`'s <LanguageInclude section="send-method" /> function is called, it calls the external MCP server and loads up all the tools that are available to it.
::: zone-end

::: zone pivot="python"
The `McpClientPlugin` integrates directly with the `ChatPrompt` <LanguageInclude section="integration-method" />. When the `ChatPrompt`'s <LanguageInclude section="send-method" /> function is called, it calls the external MCP server and loads up all the tools that are available to it.
::: zone-end

::: zone pivot="typescript"
The `MCPClientPlugin` (from `@microsoft/teams.mcpclient` package) integrates directly with the `ChatPrompt` <LanguageInclude section="integration-method" />. When the `ChatPrompt`'s <LanguageInclude section="send-method" /> function is called, it calls the external MCP server and loads up all the tools that are available to it.
::: zone-end

The <LanguageInclude section="plugin-class" /> integrates directly with the `ChatPrompt` <LanguageInclude section="integration-method" />. When the `ChatPrompt`'s <LanguageInclude section="send-method" /> function is called, it calls the external MCP server and loads up all the tools that are available to it.

::: zone pivot="csharp,typescript"
The <LanguageInclude section="plugin-class" /> integrates directly with the `ChatPrompt` object as a plugin. When the `ChatPrompt`'s <LanguageInclude section="send-method" /> function is called, it calls the external MCP server and loads up all the tools that are available to it.
::: zone-end

::: zone pivot="python"
The <LanguageInclude section="plugin-class" /> integrates directly with the `ChatPrompt` as a plugin. When the `ChatPrompt`'s <LanguageInclude section="send-method" /> function is called, it calls the external MCP server and loads up all the tools that are available to it.
::: zone-end

The <LanguageInclude section="plugin-class" /> integrates directly with the `ChatPrompt` <LanguageInclude section="integration-method" />. When the `ChatPrompt`'s <LanguageInclude section="send-method" /> function is called, it calls the external MCP server and loads up all the tools that are available to it.

::: zone pivot="csharp,python,typescript"
The <LanguageInclude section="plugin-class" /> integrates directly with the `ChatPrompt` <LanguageInclude section="integration-method" />. When the `ChatPrompt`'s `send` function is called, it calls the external MCP server and loads up all the tools that are available to it.
::: zone-end

Once loaded, it treats these tools like any functions that are available to the `ChatPrompt` object. If the LLM then decides to call one of these remote MCP tools, the MCP Client plugin will call the remote MCP server and return the result back to the LLM. The LLM can then use this result in its response.


::: zone pivot="csharp"
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# [Controller](#tab/controller)
```csharp
// DocsPrompt.cs

using Microsoft.Teams.AI;
using Microsoft.Teams.AI.Annotations;
using Microsoft.Teams.Plugins.External.McpClient;

[Prompt]
[Prompt.Description("helpful assistant")]
[Prompt.Instructions(
    "You are a helpful assistant that can help answer questions using Microsoft docs.",
    "You MUST use tool calls to do all your work."
)]
public class DocsPrompt(McpClientPlugin mcpClientPlugin)
{
    [ChatPlugin]
    public readonly IChatPlugin Plugin = mcpClientPlugin;
}

// Controller.cs
using Microsoft.Teams.AI.Models.OpenAI;
using Microsoft.Teams.Api.Activities;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities;
using Microsoft.Teams.Apps.Annotations;

[TeamsController]
public class TeamsController(Func<OpenAIChatPrompt> _promptFactory)
{
    [Message]
    public async Task OnMessage(IContext<MessageActivity> context)
    {
        await context.Send(new TypingActivity());
        var prompt = _promptFactory();
        var result = await prompt.Send(context.Activity.Text);
        await context.Send(result.Content);
    }
}

// Program.cs
using Microsoft.Teams.AI.Models.OpenAI.Extensions;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;
using Microsoft.Teams.Plugins.External.McpClient;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddTransient<TeamsController>().AddHttpContextAccessor();
builder.Services.AddSingleton((sp) => new McpClientPlugin().UseMcpServer("https://learn.microsoft.com/api/mcp"));
builder.AddTeams().AddOpenAI<DocsPrompt>();


var app = builder.Build();

app.UseTeams();
app.Run();

```

# [Minimal](#tab/minimal)
```csharp
using Microsoft.Teams.AI.Models.OpenAI;
using Microsoft.Teams.AI.Prompts;
using Microsoft.Teams.Api.Activities;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;
using Microsoft.Teams.Plugins.External.McpClient;

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);
builder.AddTeams();
WebApplication webApp = builder.Build();

OpenAIChatPrompt prompt = new(
        new OpenAIChatModel(
            model: "gpt-4o",
            apiKey: Environment.GetEnvironmentVariable("OPENAI_API_KEY")!),
            new ChatPromptOptions()
                .WithDescription("helpful assistant")
                .WithInstructions(
                    "You are a helpful assistant that can help answer questions using Microsoft docs.",
                    "You MUST use tool calls to do all your work.")
                );
prompt.Plugin(new McpClientPlugin().UseMcpServer("https://learn.microsoft.com/api/mcp"));

App app = webApp.UseTeams();
app.OnMessage(async context =>
{
    await context.Send(new TypingActivity());
    var result = await prompt.Send(context.Activity.Text);
    await context.Send(result.Content);
});
webApp.Run();
```

---


::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.ai import ChatPrompt
from microsoft.teams.mcpplugin import McpClientPlugin
from microsoft.teams.openai import OpenAICompletionsAIModel
# ...

# Set up AI model
completions_model = OpenAICompletionsAIModel(model="gpt-4")

# Configure MCP Client Plugin with multiple remote servers
mcp_plugin = McpClientPlugin()

# Add multiple MCP servers
mcp_plugin.use_mcp_server("https://learn.microsoft.com/api/mcp")
mcp_plugin.use_mcp_server("https://example.com/mcp/weather")
mcp_plugin.use_mcp_server("https://example.com/mcp/pokemon")

# ChatPrompt with MCP tools
chat_prompt = ChatPrompt(
    completions_model,
    plugins=[mcp_plugin]
)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { ChatPrompt } from '@microsoft/teams.ai';
import { App } from '@microsoft/teams.apps';
import { ConsoleLogger } from '@microsoft/teams.common';
import { McpClientPlugin } from '@microsoft/teams.mcpclient';
import { OpenAIChatModel } from '@microsoft/teams.openai';
// ...

const logger = new ConsoleLogger('mcp-client', { level: 'debug' });
const prompt = new ChatPrompt(
  {
    instructions: 'You are a helpful assistant. You MUST use tool calls to do all your work.',
    model: new OpenAIChatModel({
      model: 'gpt-4o-mini',
      apiKey: process.env.OPENAI_API_KEY,
    }),
  },
  [new McpClientPlugin({ logger })]
).usePlugin('mcpClient', {
  url: 'https://learn.microsoft.com/api/mcp',
});

const app = new App();

app.on('message', async ({ send, activity }) => {
  await send({ type: 'typing' });

  const result = await prompt.send(activity.text);
  if (result.content) {
    await send(result.content);
  }
});
app.start().catch(console.error);
```
::: zone-end



::: zone pivot="csharp"
### Custom Headers

Some MCP servers may require custom headers to be sent as part of the request. You can customize the headers when calling the `UseMcpServer` function:

```csharp
new McpClientPlugin()
    .UseMcpServer("https://learn.microsoft.com/api/mcp",
        new McpClientPluginParams()
        {
               HeadersFactory = () => new Dictionary<string, string>()
               { { "HEADER_KEY", "HEADER_VALUE" } }
        }
    );
```
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
### Customize Headers

Some MCP servers may require custom headers to be sent as part of the request. You can customize the headers when calling the `usePlugin` function:

```typescript
import { ChatPrompt } from '@microsoft/teams.ai';
import { McpClientPlugin } from '@microsoft/teams.mcpclient';
// ...

.usePlugin('mcpClient', {
    url: 'https://<your-mcp-server>/mcp'
    params: {
      headers: {
        'x-header-functions-key': '<custom-headers>',
      }
    }
});
```
::: zone-end



::: zone pivot="csharp"
In this example, we augment the `ChatPrompt` with a remote MCP Server.
::: zone-end

::: zone pivot="python"
In this example, we augment the `ChatPrompt` with multiple remote MCP Servers.

## Authentication with Headers

Many MCP servers require authentication via headers (such as API keys or Bearer tokens). You can pass these headers when configuring your MCP server:

```python
from os import getenv
from microsoft.teams.mcpplugin import McpClientPlugin, McpClientPluginParams
# ...

# This example uses a PersonalAccessToken, but you may get
# the user's oauth token as well by getting them to sign in
# and then using app.sign_in to get their token.
GITHUB_PAT = getenv("GITHUB_PAT")

# MCP server with authentication headers
if GITHUB_PAT:
    mcp_plugin.use_mcp_server(
        "https://api.githubcopilot.com/mcp/",
        McpClientPluginParams(headers={
            "Authorization": f"Bearer {GITHUB_PAT}",
        })
    )

# Other authentication examples:
mcp_plugin.use_mcp_server(
    "https://example.com/api/mcp",
    McpClientPluginParams(headers={
        "X-API-Key": getenv('API_KEY'),
        "Custom-Header": "custom-value"
    })
)
```

Headers are passed with every request to the MCP server, enabling secure access to authenticated APIs.

## Using MCP Client in Message Handlers

```python
from microsoft.teams.ai import ChatPrompt
from microsoft.teams.api import MessageActivity, MessageActivityInput
from microsoft.teams.apps import ActivityContext
# ...

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    """Handle messages using ChatPrompt with MCP tools"""

    result = await chat_prompt.send(
        input=ctx.activity.text,
        instructions="You are a helpful assistant with access to remote MCP tools."
    )

    if result.response.content:
        message = MessageActivityInput(text=result.response.content).add_ai_generated()
        await ctx.send(message)
```
::: zone-end

::: zone pivot="typescript"
In this example, we augment the `ChatPrompt` with a few remote MCP Servers.
::: zone-end


:::note
Feel free to build an MCP Server in a different agent using the [MCP Server Guide](./mcp-server). Or you can quickly set up an MCP server using [Azure Functions](https://techcommunity.microsoft.com/blog/appsonazureblog/build-ai-agent-tools-using-remote-mcp-with-azure-functions/4401059).
:::


::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python,typescript"
![Animated image of user typing a prompt ('Tell me about Charizard') to DevTools Chat window and multiple paragraphs of information being returned.](/screenshots/mcp-client-pokemon.gif)
::: zone-end



::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python,typescript"
In this example, our MCP server is a Pokemon API and our client knows how to call it. The LLM is able to call the `getPokemon` function exposed by the server and return the result back to the user.
::: zone-end
