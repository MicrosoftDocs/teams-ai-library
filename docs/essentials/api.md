---
title: Using the API Client (preview)
description: Learn about Using the API Client (preview)
ms.topic: how-to
ms.date: 05/05/2025
---

# Using the API Client (preview)

[This article is prerelease documentation and is subject to change.]

An instance of the web api client is passed to handlers that can be used
to fetch team/meeting/conversation/etc... details.

> Example: we use the api client to fetch the conversations array of members.

<!-- langtabs-start -->
```typescript
app.on('message', async ({ activity, api }) => {
  const members = await api.conversations.members(activity.conversation.id).get();
});
```
<!-- langtabs-end -->

## Graph

The api also comes with graph support built in which can be easily accessed.

<!-- langtabs-start -->
```typescript
app.on('message', async ({ activity, api }) => {
  const res = await api.user.chats.getAllMessages.get();
});
```
<!-- langtabs-end -->

## Proactive

The api client can also be accessed from outside a handler via the app instance.

<!-- langtabs-start -->
```typescript
const res = await app.api.graph.chats.getAllMessages.get();
```
<!-- langtabs-end -->