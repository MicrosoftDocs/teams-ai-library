---
title: Code Basics (preview) (C#)
description: Get familiar with the basics of Teams AI Library for C# application code.
ms.topic: get-started
ms.date: 07/16/2025
---
# Code Basics (preview) (C#)

[This article is prerelease documentation and is subject to change.]

After creating your first Teams application, let's understand its structure and key components. This will help you build more complex applications as you progress.

## Project Structure

When you create a new Teams application, it generates a directory with this basic structure:


```
Quote.Agent/
|── appPackage/       # Teams app package files
├── Program.cs        # Main application startup code
├── MainController.cs # Main activity handling code
```

- **appPackage/**: Contains the Teams app package files, including the `manifest.json` file and icons. This is required for [sideloading](/microsoftteams/platform/concepts/deploy-and-publish/apps-upload) the app into Teams for testing. The app manifest defines the app's metadata, capabilities, and permissions.

## Core Components

Let's break down the simple application we created in the [quickstart](quickstart.md) into its core components.:

### The App Class

The heart of your application is the `App` class. This class handles all incoming activities and manages your application's lifecycle. It also acts as a way to host your application service.


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


The app configuration includes a variety of options that allow you to customize its behavior, including controlling the underlying server, authentication, and other settings. For simplicity's sake, let's focus on plugins.

### Plugins

Plugins are a core part of the Teams AI v2 SDK. They allow you to hook into various lifecycles of the application. The lifecycles include server events (start, stop, initialize etc.), and also Teams Activity events (onActivity, onActivitySent, etc.). In fact, the [DevTools](../../developer-tools/devtools/overview.md) application you already have running is a plugin too. It allows you to inspect and debug your application in real-time.

> [!WARNING]
> DevTools is a plugin that should only be used in development mode. It should not be used in production applications since it offers no authentication and allows your application to be accessed by anyone.\
> **Be sure to remove the DevTools plugin from your production code.**

### Message Handling

Teams applications respond to various types of activities. The most basic is handling messages:



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



This code:

1. Listens for all incoming messages using `[Message]` attribute.
2. Sends a typing indicator, which renders as an animated ellipsis (…) in the chat.
3. Responds by echoing back the received message.

> [!NOTE]
> Each activity type has both an attribute and a functional method for type safety/simplicity
> of routing logic!

### Application Lifecycle

Your application starts when you run:


```csharp
var app = builder.Build();
app.UseTeams();
app.Run();
```


This part initializes your application server and, when configured for Teams, also authenticates it to be ready for sending and receiving messages.

## Next Steps

Now that you understand the basic structure of your Teams application, you're ready to [run it in Teams](running-in-teams.md). You will learn about Microsoft 365 Agents Toolkit and other important tools that help you with deployment and testing your application.

After that, you can:

- Add more activity handlers for different types of interactions. See [Listening to Activities](../essentials/on-activity.md) for more details.
- Integrate with external services using the [API Client](../essentials/api.md).
- Add interactive [cards](../in-depth-guides/adaptive-cards/overview.md) and [dialogs](../in-depth-guides/dialogs/overview.md). See and for more information.
- Implement [AI](../in-depth-guides/ai/overview.md).

Continue on to the next page to learn about these advanced features.

## Other Resources

- [Essentials](../essentials/overview.md)
- [Teams concepts](../../teams/core-concepts.md)
- [Teams developer tools](../../developer-tools/overview.md)