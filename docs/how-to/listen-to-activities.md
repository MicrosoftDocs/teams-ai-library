---
title: Listening To Activities
description: PLACEHOLDER
ms.topic: how-to
ms.date: 05/15/2025
---

# Listening To Activities

To listen/subscribe to different activity types, you can use the `on()` method. Handlers will be called in the order they are added.

Example: an echo bot that listens for messages sent to it and responds.

```
    app.on('message', async ({ activity, send }) > {
        await send(`you said: "${activity.text}"`);
    });
```