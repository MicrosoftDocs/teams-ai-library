---
title: "Quickstart: Build your first bot"
description: Wire up a message handler in TypeScript, C#, or Python with the Teams SDK.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 07/27/2026
---


# Quickstart: Build your first bot

Write a bot that responds to messages in Teams using the Teams SDK. Pick your language below.

> [!TIP]
>
> If you haven't registered your Teams app yet, start with [Quickstart: Register your app](./quickstart-register.md) a you'll need the credentials before this code can talk to Teams.

::: zone pivot="typescript"

If you scaffolded with `teams project new typescript`, your `src/index.ts` already looks like this:

```typescript

import { App } from '@microsoft/teams.apps';

const app = new App();

app.on('message', async ({ send, activity }) => {
  await send({ type: 'typing' });
  await send(`you said "${activity.text}"`);
});

app.start(process.env.PORT || 3978).catch(console.error);
```

| Part | Purpose |
| --- | --- |
| `new App()` | Reads credentials from `.env` automatically |
| `app.on('message', ...)` | Registers a handler for incoming messages |
| `send({ type: 'typing' })` | Shows the typing indicator while you build a reply |
| `send(...)` | Replies in the same conversation |
| `app.start(port)` | Starts the HTTP server on the given port |

Run it:

```bash

npm run dev
```

Continue with the [TypeScript guide](../getting-started/overview.md) for events, sending messages, Adaptive Cards, AI, and more.

---

::: zone-end

::: zone pivot="csharp"

If you scaffolded with `teams project new csharp`, your `Program.cs` already looks like this:

```csharp

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

Run it:

```bash

dotnet run
```

Continue with the [C# guide](../getting-started/overview.md?tabs=csharp) for events, sending messages, Adaptive Cards, AI, and more.

---

::: zone-end

::: zone pivot="python"

If you scaffolded with `teams project new python`, your `src/main.py` already looks like this:

```python

import asyncio
import re

from microsoft_teams.api import MessageActivity, TypingActivityInput
from microsoft_teams.apps import ActivityContext, App

app = App()


@app.on_message_pattern(re.compile(r"hello|hi|greetings"))
async def handle_greeting(ctx: ActivityContext[MessageActivity]) -> None:
    """Handle greeting messages."""
    await ctx.send("Hello! How can I assist you today?")


@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    """Handle message activities using the new generated handler system."""
    await ctx.reply(TypingActivityInput())

    if "reply" in ctx.activity.text.lower():
        await ctx.reply("Hello! How can I assist you today?")
    else:
        await ctx.send(f"You said '{ctx.activity.text}'")


def main():
    asyncio.run(app.start())


if __name__ == "__main__":
    main()
```

The scaffold registers two handlers: `on_message_pattern` for greetings and a fall-through `on_message` for everything else.

Run it:

```bash

pip install -e .
python src/main.py
```

Continue with the [Python guide](../getting-started/overview.md?tabs=python) for events, sending messages, Adaptive Cards, AI, and more.

::: zone-end

## What's next

- **Essentials** events, activities, sending messages, authentication: [TypeScript](../essentials/overview.md) [C#](../essentials/overview.md?tabs=csharp) [Python](../essentials/overview.md?tabs=python)
- **In-depth guides** Adaptive Cards, AI, MCP, dialogs, tabs, and more: [TypeScript](../in-depth-guides/overview.md) [C#](../in-depth-guides/overview.md?tabs=csharp) [Python](../in-depth-guides/overview.md?tabs=python)
- [Quickstart: Register your app](./quickstart-register.md) set up bot infrastructure with the Teams Developer CLI

