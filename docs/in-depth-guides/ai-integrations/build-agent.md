---
title: Build an agent in Teams
description: Create an agent, add a local clarification tool and remote MCP tool servers, stream responses into Teams, and preserve conversation history across turns.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 07/27/2026
---

# Build an agent in Teams

::: zone pivot="csharp"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="typescript"

> [!WARNING]
>
> Our AI libraries are deprecated
> The Teams SDK has deprecated its own AI libraries a the `@microsoft/teams.ai` packages (`ChatPrompt`, `Model`, and the older `@microsoft/teams.mcp` / `@microsoft/teams.a2a` plugins) a in favor of dedicated AI frameworks. Use the pattern shown in these guides instead: bring the OpenAI SDK (or any framework you like), and wire MCP and A2A directly into your Teams app.

::: zone-end

::: zone pivot="python"
This guide walks through building a Teams agent with [Microsoft Agent Framework](/agent-framework/) (MAF) a Microsoft's open-source SDK for AI agents. MAF gives you typed primitives a `Agent`, `tool`, `AgentSession`, `FunctionMiddleware` a that wrap the underlying model API, the tool-dispatch loop, and conversation history into composable pieces, so you don't hand-roll chat completions or thread tool calls yourself. It works against multiple model backends (OpenAI, Azure OpenAI, and others) and scales from a single chat agent up to coordinated multi-agent workflows.

In a Teams app, MAF runs the agent loop (model calls, tool invocations, and per-conversation memory) while the Teams SDK handles activity routing, streaming, and Teams-native affordances like Adaptive Cards and feedback controls.

Full source: [examples/ai-mcp](https://github.com/microsoft/teams.py/tree/main/examples/ai-mcp).
::: zone-end

::: zone pivot="typescript"

The agent loop here is driven by the OpenAI SDK's `runTools()` helper, which auto-executes each tool's `function` callback and feeds the result back to the model until it produces final text a so you don't hand-roll the tool-dispatch loop yourself.

> [!NOTE]
>
> This sample is bound to the OpenAI chat-completions wire protocol a Azure OpenAI and vanilla OpenAI both work; non-OpenAI providers do not.

Full source: [examples/ai-mcp](https://github.com/microsoft/teams.ts/tree/main/examples/ai-mcp).
::: zone-end

::: zone pivot="python,typescript"


## Defining the agent

An agent is composed of three core elements: a **client** (model backend), **instructions** (system prompt), and **tools** (capabilities beyond text generation). A minimal setup starts with just a chat-enabled agent:
::: zone-end

::: zone pivot="python"
```python

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient(
    model=getenv("AZURE_OPENAI_MODEL"),
    azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=getenv("AZURE_OPENAI_API_KEY"),
)

agent = Agent(
    client=client,
    instructions="You are a helpful Teams assistant.",
)
```
::: zone-end

::: zone pivot="typescript"
The "agent" is the model client plus a system prompt. The OpenAI SDK's `AzureOpenAI` client is the model backend, and `runTools()` (shown below) is the loop that drives instructions and tools together.

```typescript

import { AzureOpenAI } from 'openai';

const client = new AzureOpenAI({
  endpoint: process.env.AZURE_OPENAI_ENDPOINT!,
  apiKey: process.env.AZURE_OPENAI_API_KEY!,
  deployment: process.env.AZURE_OPENAI_MODEL_DEPLOYMENT_NAME!,
  apiVersion: process.env.AZURE_OPENAI_API_VERSION || '2024-10-21',
});

const SYSTEM_PROMPT = 'You are a helpful Teams assistant.';
```
::: zone-end

::: zone pivot="python,typescript"
## Adding a local tool

Tools extend the agent with executable capabilities. They are regular functions the model can decide to invoke. Anything that runs in your process a database lookups, business logic, or Teams-specific actions like attaching an Adaptive Card to the reply a belongs here.

A good example is **clarification**: when a request is ambiguous, the agent asks the user to pick between interpretations instead of guessing. The tool builds an Adaptive Card and stashes it in a per-turn bucket the handler inspects after the run completes; the user's choice comes back as the next turn.
::: zone-end

::: zone pivot="python"
Tools are declared with the `@tool` decorator from Agent Framework. The function name, docstring, and type annotations tell the model when and how to call the tool.

```python

from typing import Annotated

from agent_framework import tool
from microsoft_teams.cards import AdaptiveCard, Choice, ChoiceSetInput, ExecuteAction, SubmitData, TextBlock
from pydantic import Field

CLARIFICATION_VERB = "clarification"
CLARIFICATION_INPUT_ID = "clarificationChoice"

@tool
async def request_clarification(
    question: Annotated[str, Field(description="The clarification question to ask the user.")],
    options: Annotated[list[str], Field(description="2-4 candidate interpretations the user can pick between.")],
) -> str:
    """Show an Adaptive Card asking the user to clarify their ambiguous request."""
    cards = pending_cards.get()
    if cards is None:
        return "No active turn context; card could not be attached."
    card = AdaptiveCard(version="1.6").with_body([
        TextBlock(text=question, weight="Bolder", size="Medium", wrap=True),
        ChoiceSetInput(
            id=CLARIFICATION_INPUT_ID,
            choices=[Choice(title=o, value=o) for o in options],
            is_required=True,
        ),
    ]).with_actions([
        ExecuteAction(title="Submit")
        .with_data(SubmitData(CLARIFICATION_VERB, {CLARIFICATION_INPUT_ID: ""}))
        .with_associated_inputs("auto"),
    ])
    cards.append(card)
    return "Clarification card attached."
```

See [clarification cards](./teams-enhancements.md#clarification-cards) for how the user's choice flows back in.
::: zone-end

::: zone pivot="typescript"
Tools are declared as `RunnableToolFunction`s a the OpenAI SDK runs each tool's `function` callback during the tool loop. The callback pushes the card into a per-turn bucket the handler inspects after the run completes, and returns a short placeholder string.

```typescript

import type { RunnableToolFunction } from 'openai/lib/RunnableFunction';
import { AdaptiveCard, ChoiceSetInput, ExecuteAction, SubmitData, TextBlock } from '@microsoft/teams.cards';

type ClarificationArgs = { question: string; options: string[] };

export const CLARIFICATION_VERB = 'clarification';
export const CLARIFICATION_INPUT_ID = 'clarificationChoice';

function buildClarificationTool(pendingCards: AdaptiveCard[]): RunnableToolFunction<ClarificationArgs> {
  return {
    type: 'function',
    function: {
      name: 'request_clarification',
      description: 'Show an Adaptive Card asking the user to clarify their request when ambiguous.',
      parameters: {
        type: 'object',
        properties: {
          question: { type: 'string', description: 'The clarification question to ask the user.' },
          options: {
            type: 'array',
            items: { type: 'string' },
            description: '2-4 candidate interpretations the user can pick between.',
          },
        },
        required: ['question', 'options'],
        additionalProperties: false,
      },
      function: async (args: ClarificationArgs) => {
        pendingCards.push(buildClarificationCard(args));
        return 'Clarification card attached.';
      },
      parse: (raw: string) => JSON.parse(raw) as ClarificationArgs,
    },
  };
}

function buildClarificationCard(args: ClarificationArgs): AdaptiveCard {
  return new AdaptiveCard(
    new TextBlock(args.question, { weight: 'Bolder', size: 'Medium', wrap: true }),
    new ChoiceSetInput(...args.options.map((opt) => ({ title: opt, value: opt })))
      .withId(CLARIFICATION_INPUT_ID)
      .withIsRequired(true)
  ).withActions(
    new ExecuteAction({ title: 'Submit' })
      .withData(new SubmitData(CLARIFICATION_VERB))
      .withAssociatedInputs('auto')
  );
}
```

See [clarification cards](./teams-enhancements.md#clarification-cards) for how the user's choice flows back in.
::: zone-end

::: zone pivot="python,typescript"
<img
  src={ClarificationCardImgUrl}
  alt="Screenshot of a clarification Adaptive Card in a Teams chat, asking the user to pick between candidate interpretations of an ambiguous question."
  style={{ width: '100%', maxWidth: 700 }}
/>

## Adding remote MCP tools

Remote tools are exposed via [MCP](https://modelcontextprotocol.io/introduction) servers and live behind a network boundary. The agent discovers their schemas at runtime and invokes them over HTTP. From the model's perspective, they behave like any other tool.
::: zone-end

::: zone pivot="python"
Remote tools are declared using MCP tool wrappers from Agent Framework and passed to the agent just like local tools:

```python

from agent_framework import MCPStreamableHTTPTool

mcp_tools = [
    MCPStreamableHTTPTool(name="MSLearn", url="https://learn.microsoft.com/api/mcp"),
]

agent = Agent(
    client=client,
    instructions="You are a helpful Teams assistant with access to local tools and remote MCP servers.",
    tools=[request_clarification, *mcp_tools],
)
```
::: zone-end

::: zone pivot="typescript"
Connect to the MCP server once at startup, list its tools, and wrap each one as a `RunnableToolFunction`. The callback invokes the server and returns the result text to the model.

```typescript

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import type { RunnableToolFunction } from 'openai/lib/RunnableFunction';

const client = new Client({ name: 'ai-mcp-sample', version: '0.0.0' });
await client.connect(new StreamableHTTPClientTransport(new URL('https://learn.microsoft.com/api/mcp')));

const { tools } = await client.listTools();

const mcpTools: RunnableToolFunction<Record<string, unknown>>[] = tools.map((tool) => ({
  type: 'function',
  function: {
    name: tool.name,
    description: tool.description ?? '',
    parameters: (tool.inputSchema as Record<string, unknown>) ?? { type: 'object' },
    function: async (args: Record<string, unknown>) => {
      const result = await client.callTool({ name: tool.name, arguments: args });
      return stringifyResult(result.content);
    },
    parse: (raw: string) => JSON.parse(raw) as Record<string, unknown>,
  },
}));
```
::: zone-end

::: zone pivot="python,typescript"
## Running the agent in Teams

Integrate with Teams by forwarding incoming messages to the agent and streaming the response back to the chat interface chunk by chunk.
::: zone-end

::: zone pivot="python"
```python

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    async for chunk in agent.run(ctx.activity.text or "", stream=True):
        if chunk.text:
            ctx.stream.emit(chunk.text)
```
::: zone-end

::: zone pivot="typescript"
`runTools()` sends the request with your tool definitions, auto-invokes any tool the model calls, re-prompts with the result, and repeats until the model produces final text. `content` events fire for each text delta; forward them straight to the Teams stream.

```typescript

const runner = client.chat.completions.runTools({
  model: deployment,
  messages: history,
  tools: [clarificationTool, ...mcpTools],
  stream: true,
});

runner.on('content', (delta: string) => stream.emit(delta));
await runner.done();
```
::: zone-end

::: zone pivot="python,typescript"
## Per-conversation memory

By default, each run starts with no history a the model only sees the current message. This works for one-shot interactions, but is insufficient for multi-turn conversations where users refer back to earlier context. Keep a per-conversation buffer and reuse it across turns:
::: zone-end

::: zone pivot="python"
A **session** provides a conversation buffer that maintains state across turns. Create one per Teams conversation and reuse it for subsequent messages:

```python

from agent_framework import AgentSession

_sessions: dict[str, AgentSession] = {}

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    conversation_id = ctx.activity.conversation.id
    session = _sessions.setdefault(conversation_id, agent.create_session())

    async for chunk in agent.run(ctx.activity.text or "", session=session, stream=True):
        if chunk.text:
            ctx.stream.emit(chunk.text)
```
::: zone-end

::: zone pivot="typescript"
Keep one `ChatCompletionMessageParam[]` per Teams conversation. After each run, sync the runner's view a it includes the system, user, and every tool-call / tool-result / assistant message added during the loop a back into your map so the next turn sees the full prior context.

```typescript

import type { ChatCompletionMessageParam } from 'openai/resources/chat/completions';

const histories = new Map<string, ChatCompletionMessageParam[]>();

function getOrCreateHistory(convId: string): ChatCompletionMessageParam[] {
  let history = histories.get(convId);
  if (!history) {
    history = [{ role: 'system', content: SYSTEM_PROMPT }];
    histories.set(convId, history);
  }
  return history;
}

// after runner.done():
const ran = runner.messages as ChatCompletionMessageParam[];
history.splice(0, history.length, ...ran);
```
::: zone-end

::: zone pivot="python,typescript"
In production, push conversation history into Redis, Cosmos DB, or whatever you already use for state.

## Grounding responses with citations

When a tool returns search results, you usually want the model to cite its sources. The pattern: intercept each tool result, assign every source a stable 1-based index, and hand that index back to the model so it can reference it inline as `[1]`, `[2]`, and so on. The collected citations are attached to the final reply in [Enhancing the Teams Experience](./teams-enhancements.md#citations).
::: zone-end

::: zone pivot="python"
In Agent Framework this is a `FunctionMiddleware` a it sits between tool execution and the model response, letting you inspect and transform results without coupling that logic to the agent. Override `process`, run the wrapped tool with `call_next()`, then post-process its result.

```python

import json
from typing import Any

from agent_framework import FunctionInvocationContext, FunctionMiddleware

class CitationMiddleware(FunctionMiddleware):
    citations: dict[str, Any]

    async def process(self, context: FunctionInvocationContext, call_next) -> None:
        # Run the wrapped tool first, then post-process its result.
        await call_next()

        parsed = json.loads(context.result)
        for item in parsed.get("results", []):
            url = item.get("contentUrl") or item.get("link")
            if not url:
                continue
            # setdefault dedupes by URL — the same source returned by multiple
            # tool calls keeps a single, stable position.
            entry = self.citations.setdefault(url, {
                "position": len(self.citations) + 1,
                "url": url,
                "title": item.get("title") or "",
                "snippet": (item.get("content") or item.get("description") or "")[:160],
            })
            # Hand the marker back to the model so it can cite this source inline.
            item["citation"] = f"[{entry['position']}]"
        context.result = json.dumps(parsed)


tool_logger = CitationMiddleware()
agent = Agent(
    client=client,
    instructions=(
        "You are a helpful Teams assistant with access to local tools and remote MCP servers. "
        'When you use information from a search tool, cite your sources inline using the "citation" value.'
    ),
    tools=[request_clarification, *mcp_tools],
    middleware=[tool_logger],
)
```
::: zone-end

::: zone pivot="typescript"
The extraction lives in a small `CitationCollector`. Each MCP tool callback feeds its raw result into `tryExtract`, which parses the search payload and assigns every source a stable 1-based position. The same collector instance is captured by every tool call on a turn.

```typescript

type CitationEntry = { position: number; url: string; title: string; snippet: string };

export class CitationCollector {
  private readonly entries = new Map<string, CitationEntry>();

  tryExtract(result: string): void {
    let doc: any;
    try {
      doc = JSON.parse(result);
    } catch {
      return; // non-JSON tool results are ignored
    }
    for (const item of doc?.results ?? []) {
      const url = item.contentUrl ?? item.link;
      if (!url || this.entries.has(url)) continue;
      const snippet = (item.content ?? item.description ?? '').slice(0, 160);
      this.entries.set(url, {
        position: this.entries.size + 1,
        url,
        title: item.title ?? '',
        snippet,
      });
    }
  }
}
```

To wire it in, call `citations.tryExtract(text)` inside each MCP tool's callback before returning the result. The collected entries are attached to the final reply in [Enhancing the Teams Experience](./teams-enhancements.md#citations).
::: zone-end

::: zone pivot="python,typescript"
For Teams-specific enhancements a continue to [Enhancing the Teams Experience](./teams-enhancements.md).
::: zone-end

