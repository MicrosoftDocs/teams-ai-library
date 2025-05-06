---
title: Activity - Installation Updates (preview)
description: Learn about Activity - Installation Updates (preview)
ms.topic: reference
ms.date: 05/05/2025
---

# Activity: Installation Updates (preview)

[This article is prerelease documentation and is subject to change.]

The `installationUpdate` event is sent to the bot when a bot is added or removed from a conversation thread

## Installation add event

<!-- langtabs-start -->
```typescript
app.on('install.add', async ({ activity }) => {});
```
<!-- langtabs-end -->

- `install.add` - A user has installed the app.

## Installation remove event

<!-- langtabs-start -->
```typescript
app.on('install.remove', async ({ activity }) => {});
```
<!-- langtabs-end -->

- `install.remove` - A user has uninstalled the app.

## Resources

- [Microsoft Learn: Installation Events](/microsoftteams/platform/bots/how-to/conversations/subscribe-to-conversation-events#installation-update-event)