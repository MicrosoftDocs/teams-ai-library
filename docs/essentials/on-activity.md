---
title: 👂 Listening To Activities (preview)
description: Learn about 👂 Listening To Activities (preview)
ms.topic: how-to
ms.date: 04/30/2025
---

# 👂 Listening To Activities (preview)

[This article is prerelease documentation and is subject to change.]

To listen/subscribe to different activity types, you can use the `on()` method.
Handlers will be called in the order they are added.

> Example: an echo bot that listens for messages sent to it and responds.

```typescript
app.on('message', async ({ activity, send }) => {
  await send(`you said: "${activity.text}"`);
});
```

Teams exposes a variety of [activities](../activity/) that your agent can listen to and react to if it chooses. In the above example, the agent is listening to message events. However, it can listen to events such as dialog events, card actions, installation events, conversation updates and more. These events serve as the entrypoint to your application from a Teams agent point of view.