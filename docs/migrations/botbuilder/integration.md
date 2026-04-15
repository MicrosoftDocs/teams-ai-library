---
title: Using the BotBuilder Plugin
description: How to migrate BotBuilder adapters to Teams SDK plugins for handling bot communication and middleware.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 04/14/2026
---


# Using the BotBuilder Plugin

## Adapters
A BotBuilder `CloudAdapter` is responsible for managing communication between a bot and its users.
It serves as the entry point for incoming activities and forwards them to the registered `ActivityHandler` for processing.
You can customize the adapter to add middleware for logging, authentication, and define error handling.

The `BotBuilderPlugin` provided within the Teams SDK, connects the SDK with the BotBuilder framework.
It can either use an existing `CloudAdapter` or create a new default one, allowing activities to be processed through BotBuilder
while still handling events via the Teams SDK App framework.

::: zone pivot="csharp"
## Activity Handlers
The BotBuilder `ActivityHandler` contains the actual bot logic for processing messages or events
similar to how the Teams SDK `App` routes messages and events. You can override any number of methods,
such as `OnMembersAddedAsync`
or `OnMessageActivityAsync` ,
to handle different activity types.
::: zone-end

::: zone pivot="python"
## Activity Handlers
The BotBuilder `ActivityHandler` contains the actual bot logic for processing messages or events
similar to how the Teams SDK `App` routes messages and events. You can override any number of methods,
such as `on_members_added_activity`
or `on_message_activity` ,
to handle different activity types.
::: zone-end

::: zone pivot="javascript"
## Activity Handlers
The BotBuilder `ActivityHandler` contains the actual bot logic for processing messages or events
similar to how the Teams SDK `App` routes messages and events. You can override any number of methods,
such as `OnMembersAdded`
or `onMessage` ,
to handle different activity types.
::: zone-end

## Turn Context
Each incoming activity is wrapped in a `TurnContext`, which represents the context of a single turn in the conversation.
TurnContext provides access to:
- The incoming activity (message, event).
- Services for sending responses back to the user.
- Conversation, user, and channel metadata.

::: zone pivot="csharp,javascript"
Teams SDK has `IActivityContext` for the same purpose.
::: zone-end

::: zone pivot="python"
Teams SDK has `ActivityContext` for the same purpose.
::: zone-end

## How it all comes together

The `CloudAdapter` creates the `TurnContext`, and the `ActivityHandler` uses it to read the activity and send responses.

With the `BotBuilderPlugin`, when a message or activity is received:
1. The BotBuilder ActivityHandler runs first, handling the activity according to standard Bot Framework logic.
2. The Teams SDK app based activity handlers execute afterward, allowing Teams SDK logic to execute.

> [!NOTE]
> This snippet shows how to use the `BotBuilderPlugin` to send and receive activities using botbuilder instead of the default Teams SDK http plugin.

::: zone pivot="csharp"
## [Program.cs](#tab/programcs)

```csharp

using Microsoft.Bot.Builder.Integration.AspNet.Core;
using Microsoft.Teams.Api.Activities;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities;
using Microsoft.Teams.Apps.Annotations;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;

public static partial class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        builder
            .AddTeams()
            // highlight-next-line
            .AddBotBuilder<Bot, BotBuilderAdapter, ConfigurationBotFrameworkAuthentication>();

        var app = builder.Build();

        var teams = app.UseTeams();
        app.Run();
    }

    teams.OnMessage(async context =>
    {
        await context.Client.Typing();
        await context.Client.Send($"hi from teams...");
    });
}
```
## [BotBuilderAdapter.cs](#tab/botbuilderadaptercs)
```csharp
using Microsoft.Bot.Builder.Integration.AspNet.Core;
using Microsoft.Bot.Connector.Authentication;

// replace with your Adapter
// highlight-start
public class BotBuilderAdapter : CloudAdapter
{
    public BotBuilderAdapter(BotFrameworkAuthentication auth, ILogger<IBotFrameworkHttpAdapter> logger)
        : base(auth, logger)
    {
        OnTurnError = async (turnContext, exception) =>
        {
            logger.LogError(exception, $"[OnTurnError] unhandled error : {exception.Message}");

            // Send a message to the user
            await turnContext.SendActivityAsync("The bot encountered an error or bug.");
        };
    }
}
// highlight-end
```
## [ActivityHandler.cs](#tab/activityhandlercs)
```csharp
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;

// replace with your ActivityHandler
// highlight-start
public class Bot : ActivityHandler
{
    protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
    {
        var replyText = $"hi from botbuilder...";
        await turnContext.SendActivityAsync(MessageFactory.Text(replyText, replyText), cancellationToken);
    }
}
// highlight-end
```
---
::: zone-end

::: zone pivot="python"
## [app.py](#tab/apppy)
```python
import asyncio
from adapter import adapter
from activity_handler import MyActivityHandler
from microsoft_teams.api import MessageActivity
from microsoft_teams.apps import ActivityContext, App
from microsoft_teams.botbuilder import BotBuilderPlugin

# highlight-next-line
app = App(plugins=[BotBuilderPlugin(adapter=adapter, handler=MyActivityHandler())])

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    print("Handling message in app...")
    await ctx.send("hi from teams...")


if __name__ == "__main__":
    asyncio.run(app.start())
```
## [adapter.py](#tab/adapterpy)
```python
from botbuilder.core import TurnContext
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
from botbuilder.schema import Activity, ActivityTypes
from types import SimpleNamespace

config = SimpleNamespace(
            APP_TYPE="SingleTenant" if tenant_id else "MultiTenant",
            APP_ID=client_id,
            APP_PASSWORD=client_secret,
            APP_TENANTID=tenant_id,
        )

# replace with your Adapter
# highlight-start
adapter = CloudAdapter(ConfigurationBotFrameworkAuthentication(config))

async def on_error(context: TurnContext, error: Exception):
    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")

adapter.on_turn_error = on_error
# highlight-end
```
## [activity_handler.py](#tab/activity-handlerpy)
```python
from botbuilder.core import ActivityHandler, TurnContext

# replace with your ActivityHandler
# highlight-start
class MyActivityHandler(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity("hi from botbuilder...")
# highlight-end
```
---
::: zone-end

::: zone pivot="javascript"
## [index.ts](#tab/indexts)
```typescript
import { App } from '@microsoft/teams.apps';
import { BotBuilderPlugin } from '@microsoft/teams.botbuilder';

import adapter from './adapter';
import handler from './activity-handler';

const app = new App({
  // highlight-next-line
  plugins: [new BotBuilderPlugin({ adapter, handler })],
});

app.on('message', async ({ send }) => {
  await send('hi from teams...');
});

(async () => {
  await app.start();
})();
```
## [adapter.ts](#tab/adapterts)
```typescript
import { CloudAdapter } from 'botbuilder';

// replace with your BotAdapter
// highlight-start
const adapter = new CloudAdapter(
  new ConfigurationBotFrameworkAuthentication(
    {},
    new ConfigurationServiceClientCredentialFactory({
      MicrosoftAppType: tenantId ? 'SingleTenant' : 'MultiTenant',
      MicrosoftAppId: clientId,
      MicrosoftAppPassword: clientSecret,
      MicrosoftAppTenantId: tenantId,
    })
  )
);
// highlight-end

export default adapter;
```
## [activity-handler.ts](#tab/activity-handlerts)
```typescript
import { TeamsActivityHandler } from 'botbuilder';

// replace with your TeamsActivityHandler
// highlight-start
export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (ctx, next) => {
      await ctx.sendActivity('hi from botbuilder...');
      await next();
    });
  }
}
// highlight-end

const handler = new ActivityHandler();
export default handler;
```
---
::: zone-end


::: zone pivot="csharp"
In this example:
- `BotBuilderAdapter.cs` defines a `CloudAdapter` to
handle incoming activities, and can include middleware support or error handling.
- `Bot.cs` defines the `ActivityHandler` and contains the core bot logic,
handling incoming messages and sending responses via the `TurnContext`.
- `Program.cs` sets up a Teams SDK `app`
and registers the `BotBuilderPlugin` with your adapter and activity handler. It also defines a native Teams SDK activity handler that responds to messages.
::: zone-end

::: zone pivot="python"
In this example:
- `adapter.py` defines a `CloudAdapter` to
handle incoming activities, and can include middleware support or error handling.
- `activity_handler.py` defines the `ActivityHandler` and contains the core bot logic,
handling incoming messages and sending responses via the `TurnContext`.
- `app.py` sets up a Teams SDK `app`
and registers the `BotBuilderPlugin` with your adapter and activity handler. It also defines a native Teams SDK activity handler that responds to messages.
::: zone-end

::: zone pivot="javascript"
In this example:
- `adapter.ts` defines a `CloudAdapter` to
handle incoming activities, and can include middleware support or error handling.
- `activity-handler.ts` defines the `ActivityHandler` and contains the core bot logic,
handling incoming messages and sending responses via the `TurnContext`.
- `index.ts` sets up a Teams SDK `app`
and registers the `BotBuilderPlugin` with your adapter and activity handler. It also defines a native Teams SDK activity handler that responds to messages.
::: zone-end

In the ouptut below,
The first line comes from the BotBuilder ActivityHandler. The second line comes from the Teams SDK message activity handler.
This shows that both handlers can process the same message sequentially when using the BotBuilder Plugin.
This strategy can now be used to incrementally migrate from BotBuilder to the Teams SDK.

```
hi from botbuilder...
hi from teams...
```
