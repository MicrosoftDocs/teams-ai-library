---
title: Sending Messages
description: Guide to sending messages from your Teams SDK agent, including replies, proactive messages, and different message types.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 04/14/2026
---

# Sending Messages

Sending messages is a core part of an agent's functionality. With all activity handlers, a `send` method is provided which allows your handlers to send a message back to the user to the relevant conversation.


::: zone pivot="csharp"
```csharp
app.OnMessage(async context =>
{
    await context.Send($"you said: {context.activity.Text}");
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    await ctx.send(f"You said '{ctx.activity.text}'")
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ activity, send }) => {
  await send(`You said: ${activity.text}`);
});
```
::: zone-end


In the above example, the handler gets a `message` activity, and uses the `send` method to send a reply to the user.


::: zone pivot="csharp"
```csharp
  app.OnVerifyState(async context =>
  {
      await context.Send("You have successfully signed in!");
  });
  ```
::: zone-end

::: zone pivot="python"
```python
@app.event("sign_in")
async def handle_sign_in(event: SignInEvent):
    """Handle sign-in events."""
    await event.activity_ctx.send("You are now signed in!")
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('signin.verify-state', async ({ send }) => {
  await send('You have successfully signed in!');
});
```
::: zone-end


::: zone pivot="csharp"
You are not restricted to only replying to `message` activities. In the above example, the handler is listening to `SignIn.VerifyState` events, which are sent when a user successfully signs in.
::: zone-end

::: zone pivot="python"
You are not restricted to only replying to `message` activities. In the above example, the handler is listening to `sign_in` events, which are sent when a user successfully signs in.
::: zone-end

::: zone pivot="typescript"
You are not restricted to only replying to `message` activities. In the above example, the handler is listening to `signin.verify-state` events, which are sent when a user successfully signs in.
::: zone-end

> [!TIP]
> This shows an example of sending a text message. Additionally, you are able to send back things like [adaptive cards](../../in-depth-guides/adaptive-cards/overview.md) by using the same `send` method. Look at the [adaptive card](../../in-depth-guides/adaptive-cards/overview.md) section for more details.

## Streaming

You may also stream messages to the user which can be useful for long messages, or AI generated messages. The SDK makes this simple for you by providing a `stream` function which you can use to send messages in chunks.


::: zone pivot="csharp"
```csharp
app.OnMessage(async context =>
{
    context.Stream.Emit("hello");
    context.Stream.Emit(", ");
    context.Stream.Emit("world!");
    // result message: "hello, world!"
    return Task.CompletedTask;
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    ctx.stream.update("Stream starting...")
    await asyncio.sleep(1)

    # Stream messages with delays using ctx.stream.emit
    for message in STREAM_MESSAGES:
        # Add some randomness to timing
        await asyncio.sleep(random())

        ctx.stream.emit(message)
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ activity, stream }) => {
  stream.emit('hello');
  stream.emit(', ');
  stream.emit('world!');

  // result message: "hello, world!"
});
```
::: zone-end


> [!NOTE]
> Streaming is currently only supported in 1:1 conversations, not group chats or channels

:::image type="content" source="~/assets/screenshots/streaming-chat.gif" alt-text="Animated image showing agent response text incrementally appearing in the chat window." lightbox="~/assets/screenshots/streaming-chat.gif":::

## @Mention

::: zone pivot="csharp"
Sending a message at `@mentions` a user is as simple including the details of the user using the `AddMention` method
::: zone-end

::: zone pivot="python"
Sending a message at `@mentions` a user is as simple including the details of the user using the `add_mention` method
::: zone-end

::: zone pivot="typescript"
Sending a message at `@mentions` a user is as simple including the details of the user using the `addMention` method
::: zone-end


::: zone pivot="csharp"
```csharp
app.OnMessage(async context =>
{
    await context.Send(new MessageActivity("hi!").AddMention(activity.From));
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
  await ctx.send(MessageActivityInput(text='hi!').add_mention(account=ctx.activity.from_))
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ send, activity }) => {
  await send(new MessageActivity('hi!').addMention(activity.from));
});
```
::: zone-end


## Targeted Messages

> [!NOTE]
> Preview
> Targeted messages are currently in preview.

Targeted messages, also known as ephemeral messages, are delivered to a specific user in a shared conversation. From a single user's perspective, they appear as regular inline messages in a conversation. Other participants won't see these messages, making them useful for authentication flows, help or error responses, personal reminders, or sharing contextual information without cluttering the group conversation.

::: zone pivot="csharp"
To send a targeted message when responding to an incoming activity, use the `WithRecipient` method with the recipient account and set the targeting flag to true.
::: zone-end

::: zone pivot="python"
To send a targeted message when responding to an incoming activity, use the `with_recipient` method with the recipient account and set the targeting flag to true.
::: zone-end

::: zone pivot="typescript"
To send a targeted message when responding to an incoming activity, use the `withRecipient` method with the recipient account and set the targeting flag to true.
::: zone-end


::: zone pivot="csharp"
```csharp
app.OnMessage(async context =>
{
    // Using WithRecipient with isTargeted=true explicitly targets the specified recipient
    await context.Send(
        new MessageActivity("This message is only visible to you!")
            .WithRecipient(context.Activity.From, isTargeted: true)
    );
});
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api import MessageActivity, MessageActivityInput
from microsoft_teams.apps import ActivityContext

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    # Using with_recipient with is_targeted=True explicitly targets the specified recipient
    await ctx.send(
        MessageActivityInput(text="This message is only visible to you!")
            .with_recipient(ctx.activity.from_, is_targeted=True)
    )
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { MessageActivity } from '@microsoft/teams.api';

app.on('message', async ({ send, activity }) => {
  // Using withRecipient with isTargeted=true explicitly targets the specified recipient
  await send(
    new MessageActivity('This message is only visible to you!')
      .withRecipient(activity.from, true)
  );
});
```
::: zone-end

