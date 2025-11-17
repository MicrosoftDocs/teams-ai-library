---
sidebar_position: 1
summary: Guide to handling Teams-specific activities like chat messages, card actions, and installs using the fluent router API.
title: Listening to Activities
zone_pivot_groups: dev-lang
---

# Listening To Activities

An **Activity** is the Teams‑specific payload that flows between the user and your bot.
Where _events_ describe high‑level happenings inside your app, _activities_ are the raw Teams messages such as chat text, card actions, installs, or invoke calls.


::: zone pivot="csharp"
The Teams SDK exposes a fluent router so you can subscribe to these activities with `app.OnActivity(...)`, or you can use controllers/attributes.
::: zone-end

::: zone pivot="python"
The Teams SDK exposes a fluent router so you can subscribe to these activities with `@app.event("activity")`.
::: zone-end

::: zone pivot="typescript"
The Teams SDK exposes a fluent router so you can subscribe to these activities with `app.on('<route>', …)`.
::: zone-end


![alt-text for overview-1.png](~/assets/diagrams/overview-1.png)

Here is an example of a basic message handler:


::: zone pivot="csharp"
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem label="Controller" value="controller" default>
    ```csharp
    [TeamsController]
    public class MainController
    {
        [Message]
        public async Task OnMessage([Context] MessageActivity activity, [Context] IContext.Client client)
        {
            await client.Send($"you said: {activity.Text}");
        }
    }
    ```
  </TabItem>
  <TabItem label="Minimal" value="minimal">
    ```csharp
    app.OnMessage(async context =>
    {
        await context.Send($"you said: {context.activity.Text}");
    });
    ```
  </TabItem>
</Tabs>
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
In the above example, the `activity` parameter is of type `MessageActivity`, which has a `Text` property. You'll notice that the handler here does not return anything, but instead handles it by `send`ing a message back. For message activities, Teams does not expect your application to return anything (though it's usually a good idea to send some sort of friendly acknowledgment!).
::: zone-end

::: zone pivot="python"
In the above example, the `ctx.activity` parameter is of type `MessageActivity`, which has a `text` property. You'll notice that the handler here does not return anything, but instead handles it by `send`ing a message back. For message activities, Teams does not expect your application to return anything (though it's usually a good idea to send some sort of friendly acknowledgment!).
::: zone-end

::: zone pivot="typescript"
In the above example, the `activity` parameter is of type `MessageActivity`, which has a `text` property. You'll notice that the handler here does not return anything, but instead handles it by `send`ing a message back. For message activities, Teams does not expect your application to return anything (though it's usually a good idea to send some sort of friendly acknowledgment!).

[Other activity types](./activity-ref) have different properties and different required results. For a given handler, the SDK will automatically determine the type of `activity` and also enforce the correct return type.
::: zone-end


## Middleware pattern


::: zone pivot="csharp"
The `OnActivity` activity handlers (and attributes) follow a [middleware](https://www.patterns.dev/vanilla/mediator-pattern/) pattern similar to how `dotnet` middlewares work. This means that for each activity handler, a `Next` function is passed in which can be called to pass control to the next handler. This allows you to build a chain of handlers that can process the same activity in different ways.
::: zone-end

::: zone pivot="python"
The `event` activity handlers (and attributes) follow a [middleware](https://www.patterns.dev/vanilla/mediator-pattern/) pattern similar to how `python` middlewares work. This means that for each activity handler, a `next` function is passed in which can be called to pass control to the next handler. This allows you to build a chain of handlers that can process the same activity in different ways.
::: zone-end

::: zone pivot="typescript"
The `on` activity handlers follow a [middleware](https://www.patterns.dev/vanilla/mediator-pattern/) pattern similar to how `express` middlewares work. This means that for each activity handler, a `next` function is passed in which can be called to pass control to the next handler. This allows you to build a chain of handlers that can process the same activity in different ways.
::: zone-end



::: zone pivot="csharp"
<Tabs>
  <TabItem label="Controller" value="controller" default>
    ```csharp
    [Message]
    public void OnMessage([Context] MessageActivity activity, [Context] ILogger logger, [Context] IContext.Next next)
    {
        Console.WriteLine("global logger");
        next(); // pass control onward
    }
    ```
  </TabItem>
  <TabItem label="Minimal" value="minimal">
    ```csharp
    app.OnMessage(async context =>
    {
        Console.WriteLine("global logger");
        context.Next(); // pass control onward
        return Task.CompletedTask;
    });
    ```
  </TabItem>
</Tabs>

<Tabs>
  <TabItem label="Controller" value="controller" default>
    ```csharp
    [Message]
    public async Task OnMessage(IContext<MessageActivity> context)
    {
        if (context.Activity.Text == "/help")
        {
            await context.Send("Here are all the ways I can help you...");
        }

        // Conditionally pass control to the next handler
        context.Next();
    }
    ```

  </TabItem>
  <TabItem label="Minimal" value="minimal">
    ```csharp
    app.OnMessage(async context =>
    {
        if (context.Activity.Text == "/help")
        {
            await context.Send("Here are all the ways I can help you...");
        }

        // Conditionally pass control to the next handler
        context.Next();
    });
    ```

  </TabItem>
</Tabs>

<Tabs>
  <TabItem label="Controller" value="controller" default>
    ```csharp
    [Message]
    public async Task OnMessage(IContext<MessageActivity> context)
    {
        // Fallthrough to the final handler
        await context.Send($"Hello! you said {context.Activity.Text}");
    }
    ```
  </TabItem>
  <TabItem label="Minimal" value="minimal">
    ```csharp
    app.OnMessage(async context =>
    {
        // Fallthrough to the final handler
        await context.Send($"Hello! you said {context.Activity.Text}");
    });
    ```
  </TabItem>
</Tabs>
::: zone-end

::: zone pivot="python"
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


:::info
Just like other middlewares, if you stop the chain by not calling `next()`, the activity will not be passed to the next handler. The order of registration for the handlers also matters as that determines how the handlers will be called.
:::


::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
## Activity Reference

For a list of supported activities that your application can listen to, see the [activity reference](./activity-ref).
::: zone-end

