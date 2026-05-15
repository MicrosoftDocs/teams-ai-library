---
title: Sending Messages
description: Guide to sending messages from your Teams SDK agent, including replies, proactive messages, and different message types.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 05/15/2026
---

# Sending Messages

Sending messages is a core part of an agent's functionality. With all activity handlers, a `send` method is provided which allows your handlers to send a message back to the user to the relevant conversation.


::: zone pivot="csharp"
```csharp
app.OnMessage(async (context, cancellationToken) =>
{
    await context.Send($"you said: {context.activity.Text}", cancellationToken);
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
  app.OnVerifyState(async (context, cancellationToken) =>
  {
      await context.Send("You have successfully signed in!", cancellationToken);
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
app.OnMessage(async (context, cancellationToken) =>
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
app.OnMessage(async (context, cancellationToken) =>
{
    await context.Send(new MessageActivity("hi!").AddMention(activity.From), cancellationToken);
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

:::info[Coming Soon]
Targeted messages are coming soon in May 2026.
:::

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
app.OnMessage(async (context, cancellationToken) =>
{
    // Using WithRecipient with isTargeted=true explicitly targets the specified recipient
    await context.Send(
        new MessageActivity("This message is only visible to you!")
            .WithRecipient(context.Activity.From, isTargeted: true),
        cancellationToken
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



::: zone pivot="csharp"
> [!TIP]
> .NET
> In .NET, targeted message APIs are marked with `[Experimental("ExperimentalTeamsTargeted")]` and will produce a compiler error until you opt in. Suppress the diagnostic inline with `#pragma warning disable ExperimentalTeamsTargeted` or project-wide in your `.csproj`:
> 
> ```xml
> <PropertyGroup>
>   <NoWarn>$(NoWarn);ExperimentalTeamsTargeted</NoWarn>
> </PropertyGroup>
> ```
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
<!-- Not applicable -->
::: zone-end


## Reactions

Reactions allow your agent to add or remove emoji reactions on messages in a conversation, and to receive reactions added by users. See the [Message Reactions guide](../../in-depth-guides/message-reactions.md) for full coverage.

## Threading

In Teams channels, messages can be organized into threads. The SDK provides helpers to simplify working with threads.

### Reactive Threading (Within a Handler)

::: zone pivot="csharp"
When your agent receives a message in a thread, the conversation context already carries the thread ID. Use `Send()` to send a message in the same thread without quoting, or `Reply()` to send with a visual quote of the inbound message.
::: zone-end

::: zone pivot="python,typescript"
When your agent receives a message in a thread, the conversation context already carries the thread ID. Use `send()` to send a message in the same thread without quoting, or `reply()` to send with a visual quote of the inbound message.
::: zone-end


::: zone pivot="csharp"
```csharp
app.OnMessage(async (context, cancellationToken) =>
{
    // Send in the same thread, no quote
    await context.Send("Acknowledged", cancellationToken);

    // Send in the same thread with a visual quote of the inbound message
    await context.Reply("Got it!", cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    # Send in the same thread, no quote
    await ctx.send("Acknowledged")

    # Send in the same thread with a visual quote of the inbound message
    await ctx.reply("Got it!")
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ send, reply }) => {
  // Send in the same thread, no quote
  await send('Acknowledged');

  // Send in the same thread with a visual quote of the inbound message
  await reply('Got it!');
});
```
::: zone-end


For proactive threading (sending to a thread outside of a handler), see [Proactive Messaging](./proactive-messaging.md#proactive-threading).

## Quoted Replies

:::info[Coming Soon]
Quoted replies are coming soon in May 2026.
:::

Quoted replies let your agent reference a previous message in the conversation. When a user sends a message that quotes another message, your agent receives structured metadata about the quoted content. Your agent can also send messages that quote previous messages.

### Receiving Quoted Replies

::: zone pivot="csharp"
When a user quotes a message and sends it to your agent, the quoted reply metadata is available on the inbound activity. Use the `GetQuotedMessages()` method to access all quoted reply entities.
::: zone-end

::: zone pivot="python"
When a user quotes a message and sends it to your agent, the quoted reply metadata is available on the inbound activity. Use the `get_quoted_messages()` method to access all quoted reply entities.
::: zone-end

::: zone pivot="typescript"
When a user quotes a message and sends it to your agent, the quoted reply metadata is available on the inbound activity. Use the `getQuotedMessages()` method to access all quoted reply entities.
::: zone-end


::: zone pivot="csharp"
```csharp
app.OnMessage(async context =>
{
    var quotes = context.Activity.GetQuotedMessages();

    if (quotes.Count > 0)
    {
        var quote = quotes[0].QuotedReply;
        await context.Reply(
            $"You quoted message {quote.MessageId} from {quote.SenderName}: \"{quote.Preview}\"");
    }
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    quotes = ctx.activity.get_quoted_messages()

    if quotes:
        quote = quotes[0].quoted_reply
        await ctx.reply(
            f"You quoted message {quote.message_id} from {quote.sender_name}: \"{quote.preview}\""
        )
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ activity, reply }) => {
  const quotes = activity.getQuotedMessages();

  if (quotes.length > 0) {
    const quote = quotes[0].quotedReply;
    await reply(
      `You quoted message ${quote.messageId} from ${quote.senderName}: "${quote.preview}"`
    );
  }
});
```
::: zone-end


Each quoted reply entity contains the quoted message's ID, sender information, a preview of the quoted text, and whether the quoted message has been deleted.

### Sending a Quoted Reply

::: zone pivot="csharp"
When your agent calls `Reply()`, the SDK automatically stamps a quoted reply entity referencing the inbound message. The reply will appear as a quoted reply in Teams.
::: zone-end

::: zone pivot="python,typescript"
When your agent calls `reply()`, the SDK automatically stamps a quoted reply entity referencing the inbound message. The reply will appear as a quoted reply in Teams.
::: zone-end


::: zone pivot="csharp"
```csharp
app.OnMessage(async context =>
{
    // Reply() automatically quotes the inbound message
    await context.Reply("Got it!");
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    # reply() automatically quotes the inbound message
    await ctx.reply("Got it!")
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ reply }) => {
  // reply() automatically quotes the inbound message
  await reply('Got it!');
});
```
::: zone-end


::: zone pivot="csharp"
To quote a different message in the same conversation (not the inbound message), use the `Quote()` method with the message ID you want to quote.
::: zone-end

::: zone pivot="python,typescript"
To quote a different message in the same conversation (not the inbound message), use the `quote()` method with the message ID you want to quote.
::: zone-end


::: zone pivot="csharp"
```csharp
app.OnMessage(async context =>
{
    // Quote a specific message by its ID
    var parentMessageId = "1772050244572";
    await context.Quote(parentMessageId, "Referencing an earlier message");
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    # Quote a specific message by its ID
    parent_message_id = "1772050244572"
    await ctx.quote(parent_message_id, "Referencing an earlier message")
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ quote }) => {
  // Quote a specific message by its ID
  const parentMessageId = '1772050244572';
  await quote(parentMessageId, 'Referencing an earlier message');
});
```
::: zone-end


### Building Quoted Replies for Proactive Send

::: zone pivot="csharp"
For proactive scenarios (using `app.Send()`) or when quoting multiple messages, use the `AddQuote()` method on a message activity. Pass the message ID and an optional response text.
::: zone-end

::: zone pivot="python"
For proactive scenarios (using `app.send()`) or when quoting multiple messages, use the `add_quote()` method on a message activity. Pass the message ID and an optional response text.
::: zone-end

::: zone pivot="typescript"
For proactive scenarios (using `app.send()`) or when quoting multiple messages, use the `addQuote()` method on a message activity. Pass the message ID and an optional response text.
::: zone-end


::: zone pivot="csharp"
```csharp
var parentMessageId = "1772050244572";
var firstMessageId = "1772050244573";
var secondMessageId = "1772050244574";

// Single quote with response below it
var msg = new MessageActivity()
    .AddQuote(parentMessageId, "Here is my response");
await app.Send(conversationId, msg);

// Multiple quotes with interleaved responses
msg = new MessageActivity()
    .AddQuote(firstMessageId, "response to first")
    .AddQuote(secondMessageId, "response to second");
await app.Send(conversationId, msg);

// Grouped quotes — omit response to group quotes together
msg = new MessageActivity("see below for previous messages")
    .AddQuote(firstMessageId)
    .AddQuote(secondMessageId, "response to both");
await app.Send(conversationId, msg);
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api.activities.message import MessageActivityInput

parent_message_id = "1772050244572"
first_message_id = "1772050244573"
second_message_id = "1772050244574"

# Single quote with response below it
msg = (MessageActivityInput()
    .add_quote(parent_message_id, "Here is my response"))
await app.send(conversation_id, msg)

# Multiple quotes with interleaved responses
msg = (MessageActivityInput()
    .add_quote(first_message_id, "response to first")
    .add_quote(second_message_id, "response to second"))
await app.send(conversation_id, msg)

# Grouped quotes — omit response to group quotes together
msg = (MessageActivityInput(text="see below for previous messages")
    .add_quote(first_message_id)
    .add_quote(second_message_id, "response to both"))
await app.send(conversation_id, msg)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { MessageActivity } from '@microsoft/teams.api';

const parentMessageId = '1772050244572';
const firstMessageId = '1772050244573';
const secondMessageId = '1772050244574';

// Single quote with response below it
let msg = new MessageActivity()
  .addQuote(parentMessageId, 'Here is my response');
await app.send(conversationId, msg);

// Multiple quotes with interleaved responses
msg = new MessageActivity()
  .addQuote(firstMessageId, 'response to first')
  .addQuote(secondMessageId, 'response to second');
await app.send(conversationId, msg);

// Grouped quotes — omit response to group quotes together
msg = new MessageActivity('see below for previous messages')
  .addQuote(firstMessageId)
  .addQuote(secondMessageId, 'response to both');
await app.send(conversationId, msg);
```
::: zone-end



::: zone pivot="csharp"
> [!TIP]
> .NET
> In .NET, quoted reply APIs are marked with `[Experimental("ExperimentalTeamsQuotedReplies")]` and will produce a compiler error until you opt in. Suppress the diagnostic inline with `#pragma warning disable ExperimentalTeamsQuotedReplies` or project-wide in your `.csproj`:
> 
> ```xml
> <PropertyGroup>
>   <NoWarn>$(NoWarn);ExperimentalTeamsQuotedReplies</NoWarn>
> </PropertyGroup>
> ```
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
<!-- Not applicable -->
::: zone-end
