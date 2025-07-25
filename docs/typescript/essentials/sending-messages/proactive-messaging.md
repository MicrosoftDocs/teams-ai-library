---
title: Proactive Messaging (preview) (TypeScript)
description: Implement proactive messaging and communication features in Teams applications using the Teams AI Library for TypeScript.
ms.topic: how-to
ms.date: 07/16/2025
---
# Proactive Messaging (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

In [Sending Messages](./overview.md), we show how we can respond to an event when it happens. However, there are times when you want to send a message to the user without them sending a message first. This is called proactive messaging. You can do this by using the `send` method in the `app` instance. This is useful for sending notifications or reminders to the user.

The main thing to note is that you need to have the `conversationId` of the chat or channel you want to send the message to. It's a good idea to store this value somewhere from an activity handler so you can use it for proactive messaging later.

```ts
// This would be some persistent storage
const myConversationIdStorage = new Map<string, string>();

// Installation is just one place to get the conversation id. All activities
// have the conversation id, so you can use any activity to get it.
app.on('install.add', async ({ activity, send }) => {
  // Save the conversation id in 
  myConversationIdStorage.set(activity.from.aadObjectId!, activity.conversation.id);

  await send('Hi! I am going to remind you to say something to me soon!');
  notificationQueue.addReminder(activity.from.aadObjectId!, sendProactiveNotification, 10_000);
});
```

Then, when you want to send a proactive message, you can retrieve the `conversationId` from storage and use it to send the message.

```ts
const sendProactiveNotification = async (userId: string) => {
  const conversationId = myConversationIdStorage.get(userId);
  if (!conversationId) {
    return;
  }
  const activity = new MessageActivity('Hey! It\'s been a while. How are you?');
  await app.send(conversationId, activity);
};
```

> [!TIP]
> In this example, we show that we get the conversation id using one of the activity handlers. This is a good place to store the conversation id, but you can also do this in other places like when the user installs the app or when they sign in. The important thing is that you have the conversation id stored somewhere so you can use it later.