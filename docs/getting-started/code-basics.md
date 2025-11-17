---
title: Code Basics
description: Understanding the structure and key components of a Teams SDK application including the Application class, dependency injection, and project organization.
ms.topic: get-started
zone_pivot_groups: dev-lang
ms.date: 11/17/2025
---

# Code Basics

After following the guidance in [the quickstart](quickstart.md) to create your first Teams application, let's review its structure and key components. This knowledge can help you build more complex applications as you progress.

## Project Structure

When you create a new Teams application, it generates a directory with this basic structure:


::: zone pivot="csharp"
```
Quote.Agent/
|── appPackage/       # Teams app package files
├── Program.cs        # Main application startup code
├── MainController.cs # Main activity handling code
```
::: zone-end

::: zone pivot="python"
```
quote-agent/
|── appPackage/       # Teams app package files
├── src
    ├── main.py       # Main application code
```
::: zone-end

::: zone pivot="typescript"
```
quote-agent/
|── appPackage/       # Teams app package files
├── src/
│   └── index.ts      # Main application code
```
::: zone-end



::: zone pivot="csharp"
- **appPackage/**: Contains the Teams app package files, including the `manifest.json` file and icons. This is required for [sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload) the app into Teams for testing. The app manifest defines the app's metadata, capabilities, and permissions.
::: zone-end

::: zone pivot="python"
- **appPackage/**: Contains the Teams app package files, including the `manifest.json` file and icons. This is required for [sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload) the app into Teams for testing. The app manifest defines the app's metadata, capabilities, and permissions.
- **src/**: Contains the main application code. The `main.py` file is the entry point for your application.
::: zone-end

::: zone pivot="typescript"
- **appPackage/**: Contains the Teams app package files, including the `manifest.json` file and icons. This is required for [sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload) the app into Teams for testing. The app manifest defines the app's metadata, capabilities, and permissions.
- **src/**: Contains the main application code. The `index.ts` file is the entry point for your application.
::: zone-end


## Core Components

Let's break down the simple application from the [quickstart](quickstart.md) into its core components.

### The App Class

The heart of an application is the `App` class. This class handles all incoming activities and manages the application's lifecycle. It also acts as a way to host your application service.


::: zone pivot="csharp"
```csharp title="Program.cs"
using Microsoft.Teams.Plugins.AspNetCore.DevTools.Extensions;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;

using Quote.Agent;

var builder = WebApplication.CreateBuilder(args);
builder.AddTeams();
builder.AddTeamsDevTools();
builder.Services.AddTransient<MainController>();

var app = builder.Build();
app.UseTeams();
app.Run();
```
::: zone-end

::: zone pivot="python"
```python title="src/main.py"
from microsoft.teams.api import MessageActivity, TypingActivityInput
from microsoft.teams.apps import ActivityContext, App, AppOptions
from microsoft.teams.devtools import DevToolsPlugin

app = App(plugins=[DevToolsPlugin()])

```
::: zone-end

::: zone pivot="typescript"
```typescript title="src/index.ts"
import { App } from '@microsoft/teams.apps';
import { ConsoleLogger } from '@microsoft/teams.common/logging';
import { DevtoolsPlugin } from '@microsoft/teams.dev';

const app = new App({
  plugins: [new DevtoolsPlugin()],
});
```
::: zone-end


The app configuration includes a variety of options that allow you to customize its behavior, including controlling the underlying server, authentication, and other settings.

### Plugins

::: zone pivot="csharp,typescript"
Plugins are a core part of the Teams SDK. They allow you to hook into various lifecycles of the application. The lifecycles include server events (start, stop, initialize, etc.), and also Teams Activity events (onActivity, onActivitySent, etc.). In fact, the [DevTools](/developer-tools/devtools) application you already have running is a plugin too. It allows you to inspect and debug your application in real-time.
::: zone-end

::: zone pivot="python"
Plugins are a core part of the Teams SDK. They allow you to hook into various lifecycles of the application. The lifecycles include server events (start, stop, initialize, etc.), and also Teams Activity events (on_activity, on_activity_sent, etc.). In fact, the [DevTools](/developer-tools/devtools) application you already have running is a plugin too. It allows you to inspect and debug your application in real-time.
::: zone-end

> [!WARNING]
> DevTools is a plugin that should only be used in development mode. It should not be used in production applications since it offers no authentication and allows your application to be accessed by anyone.
>
> **Be sure to remove the DevTools plugin from your production code.**

### Message Handling

Teams applications respond to various types of activities. The most basic is handling messages:


::: zone pivot="csharp"
# [Controller](#tab/controller)
```csharp title="MainController.cs"
[TeamsController("main")]
public class MainController
{
    [Message]
    public async Task OnMessage([Context] MessageActivity activity, [Context] IContext.Client client)
    {
        await client.Typing();
        await client.Send($"you said \"{activity.Text}\"");
    }
}
```

# [Minimal](#tab/minimal)
```csharp title="Program.cs"
app.OnMessage(async context =>
{
    await context.Typing();
    await context.Send($"you said \"{context.activity.Text}\"");
});
```

---


::: zone-end

::: zone pivot="python"
```python title="src/main.py"
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
```typescript title="src/index.ts"
app.on('message', async ({ send, activity }) => {
  await send({ type: 'typing' });
  await send(`you said "${activity.text}"`);
});
```
::: zone-end


This code:

::: zone pivot="csharp"
1. Listens for all incoming messages using `[Message]` attribute.
2. Sends a typing indicator, which renders as an animated ellipsis (…) in the chat.
3. Responds by echoing back the received message.
::: zone-end

::: zone pivot="python"
1. Listens for all incoming messages using `app.on_message`
2. Sends a typing indicator, which renders as an animated ellipsis (…) in the chat.
3. Responds by echoing back the received message if any other text aside from "reply" is sent.
::: zone-end

::: zone pivot="typescript"
1. Listens for all incoming messages using `app.on('message')`.
2. Sends a typing indicator, which renders as an animated ellipsis (…) in the chat.
3. Responds by echoing back the received message.
::: zone-end

::: zone pivot="csharp"
> [!NOTE]
> Each activity type has both an attribute and a functional method for type safety/simplicity
> of routing logic!
::: zone-end

::: zone pivot="python"
> [!NOTE]
> Python uses type hints for better development experience. You can change the activity handler to different supported activities, and the type system will provide appropriate hints and validation.
::: zone-end

::: zone pivot="typescript"
> [!NOTE]
> Type safety is a core tenet of this version of the SDK. You can change the activity `name` to a different supported value, and the type system will automatically adjust the type of activity to match the new value.
::: zone-end


### Application Lifecycle

Your application starts when you run:


::: zone pivot="csharp"
```csharp
var app = builder.Build();
app.UseTeams();
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
```typescript title="src/index.ts"
await app.start();
```
::: zone-end


This code initializes your application server and, when configured for Teams, also authenticates it to be ready for sending and receiving messages.

## Next Steps

Now that you understand the basic structure of your Teams application, you're ready to [run it in Teams](./running-in-teams/overview.md). You will learn about Microsoft 365 Agents Toolkit and other important tools that help you with deployment and testing your application.

After that, you can:

- Add more activity handlers for different types of interactions. See [Listening to Activities](../essentials/on-activity/overview.md) for more details.
- Integrate with external services using the [API Client](../essentials/api.md).
- Add interactive [cards](../in-depth-guides/adaptive-cards/overview.md) and [dialogs](../in-depth-guides/dialogs/overview.md).
- Implement [AI](../in-depth-guides/ai/overview.md).

Continue on to the next page to learn about these advanced features.

## Other Resources

- [Essentials](../essentials/overview.md)
- [Teams concepts](../teams/overview.md)
- [Teams developer tools](../developer-tools/overview.md)
