---
title: MCP Server
description: Learn about MCP Server
ms.topic: how-to
ms.date: 05/17/2025
---
# MCP Server

You are able to convert any `App` into an MCP server by using the `McpPlugin`. This plugin adds the necessary endpoints to your application to serve as an MCP server. The plugin allows you to define tools, resources, and prompts that can be exposed to other MCP applications. 

Install it to your application:

```bash
npm install @microsoft/teams.mcp@preview
```

Your plugin can be configured as follows:

```ts
const mcpServerPlugin = new McpPlugin({
  // Describe the MCP server with a helpful name and description
  // for MCP clients to discover and use it.
  name: 'test-mcp',
  description: 'Allows you to test the mcp server',
  // Optionally, you can provide a URL to the mcp dev-tools
  // during development
  inspector: 'http://localhost:5173?proxyPort=9000',
}).tool(
  // Describe the tools with helpful names and descriptions
  'echo',
  'echos back whatever you said',
  {
    input: z.string().describe('the text to echo back'),
  },
  async ({ input }) => {
    return {
      content: [
        {
          type: 'text',
          text: `you said "${input}"`,
        },
      ],
    };
  }
);
```

:::note
> By default, the MCP server will be available at `/mcp` on your application. You can change this by setting the `transport.path` property in the plugin configuration.
:::

And included in the app like any other plugin:

```ts
const app = new App({
  plugins: [
    new DevtoolsPlugin(),
    // Add this plugin
    mcpServerPlugin,
  ],
});
```

:::tip
Enabling mcp request inspection and the `DevtoolsPlugin` allows you to see all the requests and responses to and from your MCP server (similar to how the **Activities** tab works).
:::

![MCP Server in Devtools](/screenshots/mcp-devtools.gif)

## Piping messages to the user

Since your agent is provisioned to work on Teams, one very helpful feature is to use this server as a way to send messages to the user. This can be helpful in various scenarios:

1. Human in the loop - if the server or an MCP client needs to confirm something with the user, it is able to do so.
2. Notifications - the server can be used as a way to send notifications to the user.

Here is an example of how to do this. Configure your plugin so that:
1. It can validate if the incoming request is allowed to send messages to the user
2. It fetches the correct conversation ID for the given user. 
3. It sends a proactive message to the user. See [Proactive Messaging](../../../essentials/sending-messages/proactive-messaging) for more details.

<FileCodeBlock
    lang="typescript"
    src="/generated-snippets/ts/index.snippet.mcp-server-alert-tool.ts"
/>

<FileCodeBlock
    lang="typescript"
    src="/generated-snippets/ts/index.snippet.mcp-server-message-handler-store-conversation-id.ts"
/>

