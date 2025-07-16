# A2A Client (preview)

[This article is prerelease documentation and is subject to change.]

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
      apiKey: process.env.OPENAI_API_KEY,
      model: 'gpt-4o-mini',
    }),
  },
  // Add the A2AClientPlugin to the prompt
  [new A2AClientPlugin()]
)
  // Provide the agent's server URL
  .usePlugin('a2a', {
    key: 'my-weather-agent',
    url: 'http://localhost:4000/a2a',
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

```mermaid
sequenceDiagram
    participant User
    participant ChatPrompt
    participant A2AClientPlugin
    participant AgentManager
    participant AgentClient
    participant LLM
    participant TargetAgent

    alt config
        User->>ChatPrompt: "use" with A2A server details
        ChatPrompt->>A2AClientPlugin: configure usable a2a server
        A2AClientPlugin->>AgentManager: register new potential client
    end
    alt send
        User->>ChatPrompt: Send initial message
        ChatPrompt->>A2AClientPlugin: configure system prompt
        A2AClientPlugin->>AgentManager: get agent cards
        AgentManager->>AgentClient: for each get agent card
        AgentClient-->>AgentManager: agent card
        AgentManager-->>A2AClientPlugin: all agent cards
        A2AClientPlugin-->>ChatPrompt: updated system prompt
        ChatPrompt->>A2AClientPlugin: configure tool-calls (onBuildFunctions)
        A2AClientPlugin-->>ChatPrompt: Configured tool calls
        ChatPrompt->>LLM: send-message
        LLM-->>ChatPrompt: Call A2A TargetAgent
        ChatPrompt->>A2AClientPlugin: Handler for calling A2A TargetAgent
        A2AClientPlugin->>AgentManager: Call TargetAgent with message
        AgentManager->>AgentClient: Call TargetAgent with message
        TargetAgent-->>AgentClient: Return task (e.g., completed, input-required)
        AgentClient->>AgentManager: Result task
        AgentManager->>A2AClientPlugin: Result task
        A2AClientPlugin->>ChatPrompt: Result task
        ChatPrompt-->>User: Respond with final result or follow-up
    end
```

## Notes

-   This package and the A2A protocol are experimental.
-   Ensure you handle errors and edge cases when interacting with remote agents.

## Further Reading

-   [A2A Protocol](https://google.github.io/A2A) 