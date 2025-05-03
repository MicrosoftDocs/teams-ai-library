---
title: Use the API Client
ms.topic: reference
description: Learn how to use the API client to add support for web API and graph API.
ms.date: 05/02/2025
---

# Using the API Client (preview)

[This article is prerelease documentation and is subject to change.]

An instance of the web api client is passed to handlers that can be used to fetch team/meeting/conversation/etc... details.

> Example: we use the api client to fetch the conversations array of members.

```typescript
app.on('message', async ({ activity, api }) => {
  const members = await api.conversations.members(activity.conversation.id).get();
});
```

## Graph

The api also comes with graph support built in which can be easily accessed.

```typescript
app.on('message', async ({ activity, api }) => {
  const res = await api.user.chats.getAllMessages.get();
});
```

## Proactive

The api client can also be accessed from outside a handler via the app instance.

```typescript
const res = await app.api.graph.chats.getAllMessages.get();
```