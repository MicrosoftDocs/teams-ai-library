---
title: Proactive Messaging
description: Learn how to send proactive messages to users without waiting for them to initiate the conversation, including storing conversation IDs and sending notifications.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 05/15/2026
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

# [Minimal](#tab/minimal)


    ```csharp
    app.OnInstall(async (context, cancellationToken) =>
    {
        // Save the conversation id in
        context.Storage.Set(activity.From.AadObjectId!, activity.Conversation.Id);
        await context.Send("Hi! I am going to remind you to say something to me soon!", cancellationToken);
        notificationQueue.AddReminder(activity.From.AadObjectId!, Notifications.SendProactive, 10_000);
    });
    ```

---

::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api import InstalledActivity, MessageActivityInput
from microsoft_teams.apps import ActivityContext
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
from microsoft_teams.api import MessageActivityInput
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

## Targeted Proactive Messages

:::info[Coming Soon]
Targeted messages are coming soon in May 2026.
:::

Targeted messages, also known as ephemeral messages, are delivered to a specific user in a shared conversation. From a single user's perspective, they appear as regular inline messages in a conversation. Other participants won't see these messages.

When sending targeted messages proactively, you must explicitly specify the recipient account.


::: zone pivot="csharp"
```csharp
// When sending proactively, you must provide an explicit recipient account
public static async Task SendTargetedNotification(string conversationId, Account recipient)
{
    var teams = app.UseTeams();
    await teams.Send(
        conversationId,
        new MessageActivity("This is a private notification just for you!")
            .WithRecipient(recipient, isTargeted: true)
    );
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api import MessageActivityInput, Account

# When sending proactively, you must provide an explicit recipient account
async def send_targeted_notification(conversation_id: str, recipient: Account):
    await app.send(
        conversation_id,
        MessageActivityInput(text="This is a private notification just for you!")
            .with_recipient(recipient, is_targeted=True)
    )
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { MessageActivity, Account } from '@microsoft/teams.api';

// When sending proactively, you must provide an explicit recipient account
const sendTargetedNotification = async (conversationId: string, recipient: Account) => {
  await app.send(
    conversationId,
    new MessageActivity('This is a private notification just for you!')
      .withRecipient(recipient, true)
  );
};
```
::: zone-end


## Proactive Threading

Threads are only rendered visibly in Teams channels. In 1:1 chats, group chats, and meetings, messages appear flat; passing a thread root message ID has no visible effect in those scopes.

::: zone pivot="csharp"
To proactively send a message as a reply to a thread, use `app.Reply()` with the conversation ID and thread root message ID. The SDK constructs the threaded conversation ID for you.
::: zone-end

::: zone pivot="python,typescript"
To proactively send a message as a reply to a thread, use `app.reply()` with the conversation ID and thread root message ID. The SDK constructs the threaded conversation ID for you.
::: zone-end


::: zone pivot="csharp"
```csharp
// Send to a specific thread proactively
await app.Reply(conversationId, messageId, "Thread update!");

// Send to a flat conversation (1:1, group chat)
await app.Reply(conversationId, "Hello!");
```
::: zone-end

::: zone pivot="python"
```python
# Send to a specific thread proactively
await app.reply(conversation_id, message_id, "Thread update!")

# Send to a flat conversation (1:1, group chat)
await app.reply(conversation_id, "Hello!")
```
::: zone-end

::: zone pivot="typescript"
```typescript
// Send to a specific thread proactively
await app.reply(conversationId, messageId, 'Thread update!');

// Send to a flat conversation (1:1, group chat)
await app.reply(conversationId, 'Hello!');
```
::: zone-end


::: zone pivot="csharp"
You can also pass just a conversation ID to `app.Reply()` for non-threaded conversations such as 1:1 chats and group chats. To target a specific thread, include the thread root message ID as shown above.
::: zone-end

::: zone pivot="python,typescript"
You can also pass just a conversation ID to `app.reply()` for non-threaded conversations such as 1:1 chats and group chats. To target a specific thread, include the thread root message ID as shown above.
::: zone-end

For reactive threading (within a handler), see [Threading](./overview.md#threading).

### Thread ID Helper

::: zone pivot="csharp"
For advanced scenarios, the `Conversation.ToThreadedConversationId()` helper constructs the threaded conversation ID directly. Use it with `app.Send()` when you need full control.
::: zone-end

::: zone pivot="python"
For advanced scenarios, the `to_threaded_conversation_id()` helper constructs the threaded conversation ID directly. Use it with `app.send()` when you need full control.
::: zone-end

::: zone pivot="typescript"
For advanced scenarios, the `toThreadedConversationId()` helper constructs the threaded conversation ID directly. Use it with `app.send()` when you need full control.
::: zone-end


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Api;

var threadId = Conversation.ToThreadedConversationId(conversationId, messageId);
await app.Send(threadId, "Sent via helper");
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.apps import to_threaded_conversation_id

thread_id = to_threaded_conversation_id(conversation_id, message_id)
await app.send(thread_id, "Sent via helper")
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { toThreadedConversationId } from '@microsoft/teams.apps';

const threadId = toThreadedConversationId(conversationId, messageId);
await app.send(threadId, 'Sent via helper');
```
::: zone-end
