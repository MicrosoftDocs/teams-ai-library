---
title: Send Activity
ms.topic: reference
description: Learn how to send activity or to stream chunks of an activity.
ms.date: 04/30/2025
---

# Sending Activities (preview)

[This article is prerelease documentation and is subject to change.]

[This article is prerelease documentation and is subject to change.]

To send an activity you can either use the `send` or `reply` methods. You can also `stream` chunks of an activity.

## Send

> Example: a bot that listens for when a member is added to the conversation and sends a greeting.

```typescript
app.on('conversationUpdate', async ({ activity, send }) => {
  for (const account of activity.membersAdded || []) {
    await send(`👋 welcome ${account.name}!`);
  }
});
```

> [!TIP]
> This shows an example of sending a text message. Additionally, you are able to send back things like [adaptive cards](../in-depth-guides/cards/overview.md).

## Reply

> Example: an echo bot that listens for messages sent to it and responds.

```typescript
app.on('message', async ({ activity, reply, send }) => {
  await send({ type: 'typing' }); // send typing indicator...
  await reply(`you said: "${activity.text}"`);
});
```

## Streaming

```typescript
app.on('message', async ({ activity, stream }) => {
  stream.emit('hello');
  stream.emit(', ');
  stream.emit('world!');

  // result message: "hello, world!"
});
```

![Streaming Activity](https://github.com/microsoft/teams.ts/blob/main/assets/screenshots/streaming.gif?raw=true)