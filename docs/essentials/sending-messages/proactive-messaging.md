---
sidebar_label: Proactive Messaging
title: Proactive Messaging
zone_pivot_groups: dev-lang
description: Learn how to send proactive messages to users without waiting for them to initiate the conversation, including storing conversation IDs and sending notifications.
---
# Proactive Messaging

In [Sending Messages](./overview.md), you were shown how to respond to an event when it happens. However, there are times when you want to send a message to the user without them sending a message first. This is called proactive messaging. You can do this by using the `send` method in the `app` instance. This approach is useful for sending notifications or reminders to the user.

::: zone pivot="csharp,typescript"
The main thing to note is that you need to have the `conversationId` of the chat or channel that you want to send the message to. It's a good idea to store this value somewhere from an activity handler so that you can use it for proactive messaging later.
::: zone-end

::: zone pivot="python"
The main thing to note is that you need to have the `conversation_id` of the chat or channel that you want to send the message to. It's a good idea to store this value somewhere from an activity handler so that you can use it for proactive messaging later.
::: zone-end


::: zone pivot="csharp"
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

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


::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.api import InstalledActivity, MessageActivityInput
from microsoft.teams.apps import ActivityContext
# ...

# This would be some persistent storage
storage = dict[str, str]()

# Installation is just one place to get the conversation_id. All activities have this field as well.
@app.on_install_add
async def handle_install_add(ctx: ActivityContext[InstalledActivity]):
    # Save the conversation_id
    storage[ctx.activity.from_.aad_object_id] = ctx.activity.conversation.id
    await ctx.send("Hi! I am going to remind you to say something to me soon!")
    # This queues up the proactive notifaction to be sent in 1 minute
    notication_queue.add_reminder(ctx.activity.from_.aad_object_id, send_proactive_notification, 60000)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { MessageActivity } from '@microsoft/teams.api';
import { App } from '@microsoft/teams.apps';
// ...

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
::: zone-end


::: zone pivot="csharp,typescript"
Then, when you want to send a proactive message, you can retrieve the `conversationId` from storage and use it to send the message.
::: zone-end

::: zone pivot="python"
Then, when you want to send a proactive message, you can retrieve the `conversation_id` from storage and use it to send the message.
::: zone-end


::: zone pivot="csharp"
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
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.api import MessageActivityInput
# ...

async def send_proactive_notification(user_id: str):
    conversation_id = storage.get(user_id, "")
    if not conversation_id:
        return
    activity = MessageActivityInput(text="Hey! It's been a while. How are you?")
    await app.send(conversation_id, activity)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { MessageActivity } from '@microsoft/teams.api';
import { App } from '@microsoft/teams.apps';
// ...

const sendProactiveNotification = async (userId: string) => {
  const conversationId = myConversationIdStorage.get(userId);
  if (!conversationId) {
    return;
  }
  const activity = new MessageActivity('Hey! It\'s been a while. How are you?');
  await app.send(conversationId, activity);
};
```
::: zone-end


::: zone pivot="csharp,typescript"
> [!TIP]
> In this example, you see how to get the `conversationId` using one of the activity handlers. This is a good place to store the conversation id, but you can also do this in other places like when the user installs the app or when they sign in. The important thing is that you have the conversation id stored somewhere so you can use it later.
::: zone-end

::: zone pivot="python"
> [!TIP]
> In this example, you see how to get the `conversation_id` using one of the activity handlers. This is a good place to store the conversation id, but you can also do this in other places like when the user installs the app or when they sign in. The important thing is that you have the conversation id stored somewhere so you can use it later.
::: zone-end
