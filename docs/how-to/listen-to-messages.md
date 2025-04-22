---
title: Listening To Message Activities
description: Listening To Message Activities
ms.topic: how-to
ms.date: 05/15/2025
---

# Listening To Message Activities


You can listen/subscribe to messages using static text or `Regexp`.

Example: when the user sends a message to the bot with the text `/logout` we send a message back.

```
    app.message('/logout', async ({ activity, send }) > {
        await send("ok, I'll sign you out!");
    });
```