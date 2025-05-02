---
title: at-mention (preview)
description: Learn about at-mention (preview)
ms.topic: how-to
ms.date: 04/30/2025
---

# `@mention` (preview)

[This article is prerelease documentation and is subject to change.]

Sending a message at `@mentions` a user is as simple as:

```typescript
app.on('message', async ({ send, activity }) => {
  await send(MessageSendActivity('hi!').mention(activity.from));
});
```