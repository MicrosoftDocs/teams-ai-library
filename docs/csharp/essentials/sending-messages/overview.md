---
title: Sending Messages (C#)
description: Learn about Sending Messages (C#)
ms.topic: overview
ms.date: 05/17/2025
---
# Sending Messages (C#) (preview)

[This article is prerelease documentation and is subject to change.]

Sending messages is a core part of an agent's functionality. With all activity handlers, a `Send` method is provided which allows your handlers to send a message back to the user to the relevant conversation. 
# [Controller](#tab/controller)
```csharp 
    [Message]
    public async Task OnMessage([Context] MessageActivity activity, [Context] IContext.Client client)
    {
        await client.Send($"you said: {activity.Text}");
    }
```
# [Minimal](#tab/minimal)
```csharp 
    app.OnMessage(async context =>
    {
        await context.Send($"you said: {context.activity.Text}");
    });
```
---

In the above example, the handler gets a `message` activity, and uses the `send` method to send a reply to the user.
# [Controller](#tab/controller)
```csharp 
    [SignIn.VerifyState]
    public async Task OnVerifyState([Context] SignIn.VerifyStateActivity activity, [Context] IContext.Client client)
    {
        await client.Send("You have successfully signed in!");
    }
```
# [Minimal](#tab/minimal)
```csharp 
    app.OnVerifyState(async context =>
    {
        await context.Send("You have successfully signed in!");
    });
```
---

You are not restricted to only replying to `message` activities. In the above example, the handler is listening to `SignIn.VerifyState` events, which are sent when a user successfully signs in. 

> [!TIP]
> This shows an example of sending a text message. Additionally, you are able to send back things like [adaptive cards](../../in-depth-guides/adaptive-cards/overview.md) by using the same `Send` method. Look at the [adaptive card](../../in-depth-guides/adaptive-cards/overview.md) section for more details.

## Streaming

You may also stream messages to the user which can be useful for long messages, or AI generated messages. The library makes this simple for you by providing a `Stream` function which you can use to send messages in chunks. 
# [Controller](#tab/controller)
```csharp 
    [Message]
    public void OnMessage([Context] MessageActivity activity, [Context] IStreamer stream)
    {
        stream.Emit("hello");
        stream.Emit(", ");
        stream.Emit("world!");
        // result message: "hello, world!"
    }
```
# [Minimal](#tab/minimal)
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
---

> [!NOTE]
> Streaming is currently only supported in 1:1 conversations, not group chats or channels

:::image type="content" source="~/assets/screenshots/streaming-chat.gif" alt-text="Streaming Example":::

## @Mention

Sending a message at `@mentions` a user is as simple including the details of the user using the `AddMention` method
# [Controller](#tab/controller)
```csharp 
    [Message]
    public async Task OnMessage([Context] MessageActivity activity, [Context] IContext.Client client)
    {
        await client.Send(new MessageActivity("hi!").AddMention(activity.From));
    }
```
# [Minimal](#tab/minimal)
```csharp 
    app.OnMessage(async context =>
    {
        await context.Send(new MessageActivity("hi!").AddMention(activity.From));
    });
```
---