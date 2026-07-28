---
title: Code Basics
description: Understanding the structure and key components of a Teams SDK application including the Application class, dependency injection, and project organization.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 07/27/2026
---



::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
<!-- Not applicable -->
::: zone-end


# Code Basics

After following the guidance in [the quickstart.md](quickstart.md) to create your first Teams application, let's review its structure and key components. This knowledge can help you build more complex applications as you progress.

## Project Structure

When you create a new Teams application, it generates a directory with this basic structure:


::: zone pivot="csharp"
```
QuoteAgent/
├── Program.cs        # Main application startup code
```
::: zone-end

::: zone pivot="python"
```
quote-agent/
├── src
    ├── main.py       # Main application code
```
::: zone-end

::: zone pivot="typescript"
```
quote-agent/
├── src/
│   └── index.ts      # Main application code
```
::: zone-end



::: zone pivot="csharp"
- **Program.cs**: Contains the main application code and is the entry point for your application.
::: zone-end

::: zone pivot="python"
- **src/**: Contains the main application code. The `main.py` file is the entry point for your application.
::: zone-end

::: zone pivot="typescript"
- **src/**: Contains the main application code. The `index.ts` file is the entry point for your application.
::: zone-end


## Core Components

Let's break down the simple application from the [quickstart.md](quickstart.md) into its core components.

### The App Class

The heart of an application is the `App` class. This class handles all incoming activities and manages the application's lifecycle. It also acts as a way to host your application service.


::: zone pivot="csharp"
```csharp
title="Program.cs"
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Handlers;

WebApplicationBuilder builder = WebApplication.CreateSlimBuilder(args);
builder.Services.AddTeamsBotApplication();
WebApplication app = builder.Build();

TeamsBotApplication teams = app.UseTeamsBotApplication();

teams.OnMessage(async (context, cancellationToken) =>
{
    await context.TypingAsync(cancellationToken: cancellationToken);
    await context.SendAsync($"you said '{context.Activity.Text}'", cancellationToken);
});

app.Run();
```
::: zone-end

::: zone pivot="python"
```python
title="src/main.py"
from microsoft_teams.api import MessageActivity, TypingActivityInput
from microsoft_teams.apps import ActivityContext, App

app = App()

```
::: zone-end

::: zone pivot="typescript"
```typescript
title="src/index.ts"
import { App } from '@microsoft/teams.apps';
import { ConsoleLogger } from '@microsoft/teams.common/logging';

const app = new App();
```
::: zone-end


The app configuration includes a variety of options that allow you to customize its behavior, including controlling the underlying server, authentication, and other settings.

### Plugins

::: zone pivot="csharp,typescript"
Plugins are a core part of the Teams SDK. They allow you to hook into various lifecycles of the application. The lifecycles include server events (start, stop, initialize, etc.), and also Teams Activity events (onActivity, onActivitySent, etc.).
::: zone-end

::: zone pivot="python"
Plugins are a core part of the Teams SDK. They allow you to hook into various lifecycles of the application. The lifecycles include server events (start, stop, initialize, etc.), and also Teams Activity events (on_activity, on_activity_sent, etc.).
::: zone-end


::: zone pivot="csharp,typescript"
To test your agent locally without sideloading into Teams, run the **[Microsoft 365 Agents Playground](../developer-tools/agents-playground/overview.md)** alongside your agent. The playground is a separate CLI tool and does not require a plugin in your app code.
::: zone-end

::: zone pivot="python"
To test your agent locally without sideloading into Teams, run the **[Microsoft 365 Agents Playground](../developer-tools/agents-playground/overview.md)** alongside your agent. The playground is a separate CLI tool and does not require any plugin in your app code.
::: zone-end


### Message Handling

Teams applications respond to various types of activities. The most basic is handling messages:


::: zone pivot="csharp"
```csharp
title="Program.cs"
teams.OnMessage(async (context, cancellationToken) =>
{
    await context.TypingAsync(cancellationToken: cancellationToken);
    await context.SendAsync($"you said \"{context.Activity.Text}\"", cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
```python
title="src/main.py"
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    await ctx.reply(TypingActivityInput())

    if "reply" in ctx.activity.text.lower():
        await ctx.reply("Hello! How can I assist you today?")
    else:
        await ctx.send(f"You said '{ctx.activity.text}'")
```
::: zone-end

::: zone pivot="typescript"
```typescript
title="src/index.ts"
app.on('message', async ({ send, activity }) => {
  await send({ type: 'typing' });
  await send(`you said "${activity.text}"`);
});
```
::: zone-end


This code:

::: zone pivot="csharp"
1. Listens for all incoming messages using `onMessage` handler.
2. Sends a typing indicator, which renders as an animated ellipsis (a) in the chat.
3. Responds by echoing back the received message.
::: zone-end

::: zone pivot="python"
1. Listens for all incoming messages using `app.on_message`
2. Sends a typing indicator, which renders as an animated ellipsis (a) in the chat.
3. Responds by echoing back the received message if any other text aside from "reply" is sent.
::: zone-end

::: zone pivot="typescript"
1. Listens for all incoming messages using `app.on('message')`.
2. Sends a typing indicator, which renders as an animated ellipsis (a) in the chat.
3. Responds by echoing back the received message.
::: zone-end


::: zone pivot="csharp"
:::info
Each activity type has both an attribute and a functional method for type safety/simplicity
of routing logic!
:::
::: zone-end

::: zone pivot="python"
:::info
Python uses type hints for better development experience. You can change the activity handler to different supported activities, and the type system will provide appropriate hints and validation.
:::
::: zone-end

::: zone pivot="typescript"
:::info
Type safety is a core tenet of this version of the SDK. You can change the activity `name` to a different supported value, and the type system will automatically adjust the type of activity to match the new value.
:::
::: zone-end


### Application Lifecycle

Your application starts when you run:


::: zone pivot="csharp"
```csharp

WebApplication app = builder.Build();
app.UseTeamsBotApplication();
app.Run();
```
::: zone-end

::: zone pivot="python"
```python

if __name__ == "__main__":
    asyncio.run(app.start())
```
::: zone-end

::: zone pivot="typescript"
```typescript
title="src/index.ts"
await app.start();
```
::: zone-end


This code initializes your application server and, when configured for Teams, also authenticates it to be ready for sending and receiving messages.

## Next Steps

Now that you understand the basic structure of your Teams application, you're ready to [run it in Teams](running-in-teams/overview.md). You'll use the Teams Developer CLI to register your bot and sideload it into Teams.

After that, you can:

- Add more activity handlers for different types of interactions. See [Listening to Activities](../essentials/on-activity/overview.md) for more details.
- Integrate with external services using the [API Client](../essentials/api.md).
- Add interactive [cards](../in-depth-guides/adaptive-cards/overview.md) and [dialogs](../in-depth-guides/dialogs/overview.md).

Continue on to the next page to learn about these advanced features.

## Other Resources

- [Essentials](../essentials/overview.md)
- [Teams concepts](../teams/overview.md)
- [Teams developer tools](../developer-tools/overview.md)

