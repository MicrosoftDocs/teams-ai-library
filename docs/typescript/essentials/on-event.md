---
title: Listening To Events (TypeScript)
description: Understanding how to listen to and handle events in Teams AI applications, including user actions and application server events.
ms.topic: how-to
ms.date: 09/29/2025
---

# Listening To Events (TypeScript)

An **event** is a foundational concept in building agents — it represents something noteworthy happening either on Microsoft Teams or within your application. These events can originate from the user (e.g. installing or uninstalling your app, sending a message, submitting a form), or from your application server (e.g. startup, error in a handler).

![alt-text for on-event-1.png](~/assets/diagrams/on-event-1.png)

The Teams AI Library makes it easy to subscribe to these events and respond appropriately. You can register event handlers to take custom actions when specific events occur — such as logging errors, triggering workflows, or sending follow-up messages.

Here are the events that you can start building handlers for:

| **Event Name**      | **Description**                                                                |
| ------------------- | ------------------------------------------------------------------------------ |
| `start`             | Triggered when your application starts. Useful for setup or boot-time logging. |
| `signin`            | Triggered during a sign-in flow via Teams.                                     |
| `error`             | Triggered when an unhandled error occurs in your app. Great for diagnostics.   |
| `activity`          | A catch-all for incoming Teams activities (messages, commands, etc.).          |
| `activity.response` | Triggered when your app sends a response to an activity. Useful for logging.   |
| `activity.sent`     | Triggered when an activity is sent (not necessarily in response).              |

### Example 1

We can subscribe to errors that occur in the app.

```typescript
app.event('error', ({ err, log }) => {
  log.error(err);
  // Or Alternatively, send it to an observability platform
});
```

### Example 2

When a user signs in using `OAuth` or `SSO`, use the graph api to fetch their profile and say hello.

```typescript

import * as endpoints from '@microsoft/teams.graph-endpoints';
app.event('signin', async ({ activity, send, userGraph }) => {
  const me = await userGraph.call(endpoints.me.get);
  await send(`👋 Hello ${me.name}`);
});
```
