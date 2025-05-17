---
title: Chat Generation
description: Learn about Chat Generation
ms.topic: how-to
ms.date: 05/17/2025
---
# Chat Generation

Before going through this guide, please make sure you have completed the [setup and prerequisites](./setup-and-prereqs.md) guide.
# Setup

The basic setup involves creating a `ChatPrompt` and giving it the `Model` you want to use.

![alt-text for chat-1.png](~/assets/diagrams/chat-1.png)

## Simple chat generation

Chat generation is the the most basic way of interacting with an LLM model. It involves setting up your ChatPrompt, the Model, and sending it the message.

Import the relevant objects:

<FileCodeBlock
    lang="typescript"
    src="/generated-snippets/ts/index.snippet.ai-imports.ts"
/>

<FileCodeBlock
    lang="typescript"
    src="/generated-snippets/ts/index.snippet.simple-chat.ts"
/>

:::note
The current `OpenAIChatModel` implementation uses chat-completions API. The responses API is coming soon.
:::

## Streaming chat responses

LLMs can take a while to generate a response, so often streaming the response leads to a better, more responsive user experience.

:::warning
Streaming is only currently supported for single 1:1 chats, and not for groups or channels.
:::

<FileCodeBlock
    lang="typescript"
    src="/generated-snippets/ts/index.snippet.streaming-chat.ts"
/>

![Streaming the response](/screenshots/streaming-chat.gif)
