---
title: Listening To Activities
description: Guide to handling Teams-specific activities like chat messages, card actions, and installs using the fluent router API.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---

# Listening To Activities

An **Activity** is the Teams‑specific payload that flows between the user and your bot.
Where _events_ describe high‑level happenings inside your app, _activities_ are the raw Teams messages such as chat text, card actions, installs, or invoke calls.


::: zone pivot="csharp"
The Teams SDK exposes a fluent router so you can subscribe to these activities with dedicated handler methods using minimal APIs.
::: zone-end

::: zone pivot="python"
The Teams SDK exposes a fluent router so you can subscribe to these activities with `@app.event("activity")`.
::: zone-end

::: zone pivot="typescript"
The Teams SDK exposes a fluent router so you can subscribe to these activities with `app.on('<route>', …)`.
::: zone-end


:::image type="content" source="~/assets/diagrams/essentials-on-activity-overview-1.png" alt-text="Flowchart showing Teams events reaching the app server, which sends an activity event to the activity router (app.on()) that invokes your activity handlers." lightbox="~/assets/diagrams/essentials-on-activity-overview-1.png" :::

Here is an example of a basic message handler:


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
Slash commands arrive as targeted messages. Check `Recipient.IsTargeted` and handle them explicitly:

```csharp
app.OnMessage(async (context, cancellationToken) =>
{
    await context.Send($"you said: {context.Activity.Text}", cancellationToken);
});
```

---

# [SDK 2.1 (current)](#tab/core)
```csharp
teams.OnMessage(async (context, cancellationToken) =>
{
    await context.SendAsync($"you said: {context.Activity.Text}", cancellationToken);
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



::: zone pivot="csharp"
In the above example, the `context.Activity` property is of type `MessageActivity`, which has a `Text` property. You'll notice that the handler here does not return anything, but instead handles the activity by `Send`ing a message back. For message activities, Teams does not expect your application to return anything (though it's usually a good idea to send some sort of friendly acknowledgment!).
::: zone-end

::: zone pivot="python"
In the above example, the `ctx.activity` parameter is of type `MessageActivity`, which has a `text` property. You'll notice that the handler here does not return anything, but instead handles it by `send`ing a message back. For message activities, Teams does not expect your application to return anything (though it's usually a good idea to send some sort of friendly acknowledgment!).
::: zone-end

::: zone pivot="typescript"
In the above example, the `activity` parameter is of type `MessageActivity`, which has a `text` property. You'll notice that the handler here does not return anything, but instead handles it by `send`ing a message back. For message activities, Teams does not expect your application to return anything (though it's usually a good idea to send some sort of friendly acknowledgment!).

[Other activity types](./activity-ref.md) have different properties and different required results. For a given handler, the SDK will automatically determine the type of `activity` and also enforce the correct return type.
::: zone-end


## Slash Commands

Slash commands are manifest-declared commands users run from the compose box. To enable slash commands, set `supportsTargetedMessages: true` in your app manifest under the `bots` section. You can opt in with an explicit command list by declaring specific commands using `commandLists` with `triggers: ["slash"]`, which Teams shows in the slash menu when a user types `/`. Without a command list, users can still invoke your agent via `/agent-name` and provide free-form input.

```json
{
  "bots": [
    {
      "botId": "{{BOT_ID}}",
      "scopes": ["personal", "team", "groupChat"],
      "supportsTargetedMessages": true,
      "commandLists": [
        {
          "scopes": ["team", "groupChat"],
          "triggers": ["slash"],
          "commands": [
            { "title": "Review", "description": "Review a document" }
          ]
        }
      ]
    }
  ]
}
```

When a user sends a slash command, it appears as a private message visible only to them. Your agent can reply privately or, when appropriate, share a response with the broader group or channel.

Slash commands arrive as normal message activities with the targeted flag set on the activity's recipient object.


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
Slash commands arrive as targeted messages. Check `Recipient.IsTargeted` and handle them explicitly:

```csharp
app.OnMessage(async (context, cancellationToken) =>
{
    if (context.Activity.Recipient?.IsTargeted == true)
    {
        await context.Send($"Received slash command: {context.Activity.Text}", cancellationToken);
    }
});
```

---

# [SDK 2.1 (current)](#tab/core)
Slash commands arrive as targeted messages. Check `Recipient.IsTargeted` and handle them explicitly:

```csharp
teams.OnMessage(async (context, cancellationToken) =>
{
    if (context.Activity.Recipient?.IsTargeted == true)
    {
        await context.SendAsync($"Received slash command: {context.Activity.Text}", cancellationToken);
    }
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    if ctx.activity.recipient and ctx.activity.recipient.is_targeted:
        await ctx.send(f"Received slash command: {ctx.activity.text}")
        return

    await ctx.next()
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ activity, send, next }) => {
  if (activity.recipient?.isTargeted) {
    await send(`Received slash command: ${activity.text}`);
    return;
  }

  await next();
});
```
::: zone-end


## Activity handler chaining


::: zone pivot="csharp"
In SDK 2.1, activity handlers no longer form a next()-style processing chain. Instead, every handler that matches an activity is invoked in the order it was registered, and one handler cannot prevent subsequent matching handlers from running. If you need to intercept, short-circuit, or wrap request processing (for example, to stop execution when a condition is met), implement `ITurnMiddleware` and control whether to call `nextTurn(...)`. See [turn middleware](../middleware-error-handling.md) for details.

> [!NOTE]
> SDK 2.0 (Legacy). In SDK 2.0, activity handlers are chained. Call `context.Next()` to continue to the next matching handler; return without it to stop the chain. Registration order determines handler execution order.
>
> ```csharp
> app.OnMessage(async (context, cancellationToken) =>
> {
>     if (context.Activity.Text == "/help")
>     {
>         await context.Send("Here are all the ways I can help you...", cancellationToken);
>         return; // stop chain
>     }
>
>     await context.Next(); // continue chain
> });
>
> app.OnMessage(async (context, cancellationToken) =>
> {
>     await context.Send($"Hello! you said {context.Activity.Text}", cancellationToken);
> });
> ```

::: zone-end

::: zone pivot="python"
The `event` activity handlers (and attributes) follow a [middleware](https://www.patterns.dev/vanilla/mediator-pattern/) pattern similar to how `python` middlewares work. This means that for each activity handler, a `next` function is passed in which can be called to pass control to the next handler. This allows you to build a chain of handlers that can process the same activity in different ways.

```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    """Handle message activities using the new generated handler system."""
    print(f"[GENERATED onMessage] Message received: {ctx.activity.text}")
    await ctx.next()
```

```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    """Handle message activities using the new generated handler system."""
    if ctx.activity.text == "/help":
        await ctx.send("Here are all the ways I can help you...")
    await ctx.next()
```

```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    await ctx.send(f"You said '{ctx.activity.text}'")
```
::: zone-end

::: zone pivot="typescript"
The `on` activity handlers follow a [middleware](https://www.patterns.dev/vanilla/mediator-pattern/) pattern similar to how `express` middlewares work. This means that for each activity handler, a `next` function is passed in which can be called to pass control to the next handler. This allows you to build a chain of handlers that can process the same activity in different ways.

```typescript
app.on('message', async ({ next }) => {
  console.log('global logger');
  next(); // pass control onward
});
```

```typescript
app.on('message', async ({ activity, next }) => {
  if (activity.text === '/help') {
    await send('Here are all the ways I can help you...');
    return;
  }

  // Conditionally pass control to the next handler
  next();
});
```

```typescript
app.on('message', async ({ activity }) => {
  // Fallthrough to the final handler
  await send(`Hello! you said ${activity.text}`);
});
```
::: zone-end



::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
## Activity Reference

For a list of supported activities that your application can listen to, see the [activity reference](./activity-ref.md).
::: zone-end

