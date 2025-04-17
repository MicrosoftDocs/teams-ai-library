---
title: Activity - Installation update event
description: Activity - Installation update event
ms.topic: how-to
ms.date: 05/15/2025
---

# Activity: Installation update event


The `installationUpdate` event is sent to the bot when a bot is added or removed from a conversation thread

## Installation add event

```
    app.on('install.add', async ({ activity }) > {});
```

*   `install.add` - A user has installed the app.

## Installation remove event

```
    app.on('install.remove', async ({ activity }) > {});
```

*   `install.remove` - A user has uninstalled the app.

## Resources

* [Microsoft Learn: Installation Events](/microsoftteams/platform/bots/how-to/conversations/subscribe-to-conversation-events#installation-update-event)