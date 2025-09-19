---
title: A2A Client (TypeScript)
description: Learn about A2A Client (TypeScript)
ms.topic: how-to
ms.date: 09/18/2025
---

# A2A Client (TypeScript)

## What is an A2A Client?

An A2A client is an agent or application that can proactively send tasks to A2A servers and interact with them using the A2A protocol.

## Using AgentManager to Call A2A Servers

You can use the `AgentManager` to register and send tasks to different A2A servers:

```ts
// import { AgentManager } from "@microsoft/teams.a2a";
const directlyUserAgentManager = async (message: string) => {
  const agentManager = new AgentManager();
  agentManager.use('my-agent', 'https://my-agent.com/a2a');

  const taskId = 'my-task-id'; // Generated or reused from previous task
  await agentManager.sendTask('my-agent', {
    id: taskId,
    message: {
      role: 'user',
      parts: [{ type: 'text' as const, text: message }],
    },
  });
};
```

## Using A2AClientPlugin with ChatPrompt

A2A is most effective when used with an LLM. The `A2AClientPlugin` can be added to your chat prompt to allow interaction with A2A agents. Once added, the plugin will automatically configure the system prompt and tool calls to determine if the a2a server is needed for a particular task, and if so, it will do the work of orchestrating the call to the A2A server.

```ts
// import { ChatPrompt } from "@microsoft/teams.ai";
// import { OpenAIChatModel } from "@microsoft/teams.openai";
// import { A2AClientPlugin } from "@microsoft/teams.a2a";
const prompt = new ChatPrompt(
  {
    logger,
    model: new OpenAIChatModel({
      apiKey: process.env.AZURE_OPENAI_API_KEY,
      model: process.env.AZURE_OPENAI_MODEL!,
      endpoint: process.env.AZURE_OPENAI_ENDPOINT,
      apiVersion: process.env.AZURE_OPENAI_API_VERSION
    }),
  },
  // Add the A2AClientPlugin to the prompt
  [new A2AClientPlugin()]
)
  // Provide the agent's card URL
  .usePlugin('a2a', {
    key: 'my-weather-agent',
    cardUrl: 'http://localhost:4000/a2a/.well-known/agent-card.json',
  });
```
```ts
// Now we can send the message to the prompt and it will decide if
// the a2a agent should be used or not and also manages contacting the agent
const result = await prompt.send(message);
return result;
```



## Sequence Diagram

To understand how the A2A client works with the `ChatPrompt`, `A2AClientPlugin`, and `AgentManager`, here is a sequence diagram that illustrates the flow of messages. The main thing to note is that the `A2AClientPlugin` has 3 main responsibilities:
1. Keep state of the A2A agents that it can call. It does so using the `AgentManager` described above.
2. Before sending a message to the LLM, it gets the agent cards for the required agents, and includes their descriptions in the system prompt.
3. It configures the tool calls for the LLM to decide if it needs to call a particular A2A agent.
4. If the LLM decides to call an A2A agent, the plugin will use the `AgentManager` to call the agent and return the result.

![alt-text for a2a-client-1.png](~/assets/diagrams/a2a-client-1.png)

## Notes

-   This package and the A2A protocol are experimental.
-   Ensure you handle errors and edge cases when interacting with remote agents.

## Further Reading

-   [A2A Protocol](https://google.github.io/A2A)
