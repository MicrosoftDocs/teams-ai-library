---
title: Feedback
description: PLACEHOLDER
ms.topic: how-to
ms.date: 05/15/2025
---

# Feedback


If enabled, feedback buttons will be present in messages that allow the user to provide an indication of whether the message was useful/correct or not. This feature can be used with LLM's for training.

## Enable Message Feedback

```
    app.on('message', async ({ send }) > {
        await send(MessageSendActivity('hi!').addFeedback());
    });
```

![Feedback Message](../assets/images/feedback_message.png?rawtrue)

## Handling Message Feedback

Return a status: 200 upon receiving `message.submit.feedback`.

```
    app.on('message.submit.feedback', ({ log, activity }) > {
        // Your storage logic here...
        log.debug(activity);
        return { status: 200 };
    });
```

![Feedback Dialog](../assets/images/feedback_dialog.png?rawtrue)