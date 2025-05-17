---
title: Proactive Messaging (C#)
description: Learn about Proactive Messaging (C#)
ms.topic: how-to
ms.date: 05/17/2025
---
# Proactive Messaging (C#) (preview)

[This article is prerelease documentation and is subject to change.]

In [Sending Messages](overview.md), we show how we can respond to an event when it happens. However, there are times when you want to send a message to the user without them sending a message first. This is called proactive messaging. You can do this by using the `send` method in the `app` instance. This is useful for sending notifications or reminders to the user.

The main thing to note is that you need to have the `conversationId` of the chat or channel you want to send the message to. It's a good idea to store this value somewhere from an activity handler so you can use it for proactive messaging later.
# [Controller](#tab/controller)
```csharp
    // Installation is just one place to get the conversation id. All activities
    // have the conversation id, so you can use any activity to get it.
    [Install]
    public async Task OnInstall([Context] InstallUpdateActivity activity, [Context] IContext.Client client, [Context] IStorage<string, object> storage)
    {
        // Save the conversation id in 
        storage.Set(activity.From.AadObjectId!, activity.Conversation.Id);
        await client.Send("Hi! I am going to remind you to say something to me soon!");
        notificationQueue.AddReminder(activity.From.AadObjectId!, Notifications.SendProactive, 10_000);
    }
```
# [Minimal](#tab/minimal)
```csharp 
    app.OnInstall(async context =>
    {
        // Save the conversation id in 
        context.Storage.Set(activity.From.AadObjectId!, activity.Conversation.Id);
        await context.Send("Hi! I am going to remind you to say something to me soon!");
        notificationQueue.AddReminder(activity.From.AadObjectId!, Notifications.SendProactive, 10_000);
    });
```
---

Then, when you want to send a proactive message, you can retrieve the `conversationId` from storage and use it to send the message.

```csharp
public static class Notifications
{
    public static async Task SendProactive(string userId)
    {
        var conversationId = (string?)storage.Get(userId);

        if (conversationId is null) return;

        await app.Send(conversationId, "Hey! It's been a while. How are you?");
    }
}
```

> [!TIP]
> In this example, we show that we get the conversation id using one of the activity handlers. This is a good place to store the conversation id, but you can also do this in other places like when the user installs the app or when they sign in. The important thing is that you have the conversation id stored somewhere so you can use it later.