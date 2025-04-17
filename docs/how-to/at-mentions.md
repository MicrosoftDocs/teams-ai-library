---
title: At-mentions
description: At-mentions
ms.topic: how-to
ms.date: 05/15/2025
---

# At-mentions


Sending a message at `@mentions` a user is as simple as:

```
    app.on('message', async ({ send, activity }) > {
        await send(MessageSendActivity('hi!').mention(activity.from));
    });
```