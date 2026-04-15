---
title: Sending Activities
description: Migrate from BotBuilder's TurnContext activity sending to Teams SDK's simplified send method with better Adaptive Card support.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 04/14/2026
---


# Sending Activities

BotBuilder's pattern for sending activities via its `TurnContext` is similar to that in Teams SDK,
but one key difference is that sending adaptive cards doesn't require constructing the entire activity yourself.


::: zone pivot="csharp"
# [Diff](#tab/diff)
```csharp
// highlight-error-start
-   using Microsoft.Bot.Builder;
-   using Microsoft.Bot.Schema;
// highlight-error-end
// highlight-success-start
+   using Microsoft.Teams.Apps;
+   using Microsoft.Teams.Plugins.AspNetCore.Extensions;
+   using Microsoft.Teams.Api.Activities;
//highlight-success-end

// highlight-error-start
-   public class MyActivityHandler : ActivityHandler
-   {
-       protected override async Task OnMessageActivityAsync(
-           ITurnContext<IMessageActivity> turnContext,
-           CancellationToken cancellationToken)
-       {
-           await turnContext.SendActivityAsync(
-               Activity.CreateTypingActivity(),
-               cancellationToken: cancellationToken);
-       }
-   }
// highlight-error-end
// highlight-success-start
+   var teams = app.UseTeams();
+   teams.OnMessage(async (context) =>
+   {
+       await context.Send(new Activity(type:"typing"));
+   });
// highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```csharp
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;

public class MyActivityHandler : ActivityHandler
{
    protected override async Task OnMessageActivityAsync(
        ITurnContext<IMessageActivity> turnContext,
        CancellationToken cancellationToken)
    {
        // highlight-next-line
        await turnContext.SendActivityAsync(
            Activity.CreateTypingActivity(),
            cancellationToken: cancellationToken);
    }
}
```
# [Teams SDK](#tab/teams-sdk)
```csharp
using Microsoft.Teams.Apps;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;
using Microsoft.Teams.Api.Activities;

var teams = app.UseTeams();
teams.OnMessage(async (context) =>
{
    // highlight-next-line
    await context.Send(new Activity(type:"typing"));
});
```
---
## Strings

# [Diff](#tab/diff)
```csharp
// highlight-error-start
-   using Microsoft.Bot.Builder;
-   using Microsoft.Bot.Schema;
// highlight-error-end
// highlight-success-start
+   using Microsoft.Teams.Apps;
+   using Microsoft.Teams.Plugins.AspNetCore.Extensions;
//highlight-success-end

// highlight-error-start
-   public class MyActivityHandler : ActivityHandler
-   {
-       protected override async Task OnMessageActivityAsync(
-           ITurnContext<IMessageActivity> turnContext,
-           CancellationToken cancellationToken)
-       {
-           await turnContext.SendActivityAsync("hello world", cancellationToken: cancellationToken);
-       }
-   }
// highlight-error-end
// highlight-success-start
+   var teams = app.UseTeams();
+   teams.OnMessage(async (context) =>
+   {
+       await context.Send("hello world");
+   });
// highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```csharp
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;

public class MyActivityHandler : ActivityHandler
{
    protected override async Task OnMessageActivityAsync(
        ITurnContext<IMessageActivity> turnContext,
        CancellationToken cancellationToken)
    {
        // highlight-next-line
        await turnContext.SendActivityAsync("hello world", cancellationToken: cancellationToken);
    }
}
```
# [Teams SDK](#tab/teams-sdk)
```csharp
using Microsoft.Teams.Apps;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;

var teams = app.UseTeams();
teams.OnMessage(async (context) =>
{
    // highlight-next-line
    await context.Send("hello world");
});
```
---
## Adaptive Cards

# [Diff](#tab/diff)
```csharp
// highlight-error-start
-   using Microsoft.Bot.Builder;
-   using Microsoft.Bot.Schema;
// highlight-error-end
// highlight-success-start
+   using Microsoft.Teams.Apps;
+   using Microsoft.Teams.Cards;
+   using Microsoft.Teams.Plugins.AspNetCore.Extensions;
// highlight-success-end

// highlight-error-start
-   public class MyActivityHandler : ActivityHandler
-   {
-       protected override async Task OnMessageActivityAsync(
-           ITurnContext<IMessageActivity> turnContext,
-           CancellationToken cancellationToken)
-       {
-           var card = new
-           {
-               type = "AdaptiveCard",
-               version = "1.0",
-               body = new[]
-               {
-                   new { type = "TextBlock", text = "hello world" }
-               }
-           };
-           var attachment = new Attachment
-           {
-               ContentType = "application/vnd.microsoft.card.adaptive",
-               Content = card
-           };
-           var activity = MessageFactory.Attachment(attachment);
-           await turnContext.SendActivityAsync(activity, cancellationToken: cancellationToken);
-       }
-   }
// highlight-error-end
// highlight-success-start
+   var teams = app.UseTeams();
+   teams.OnMessage(async (context) =>
+   {
+       await context.Send(new AdaptiveCard(new TextBlock("hello world")));
+   });
// highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```csharp
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;

public class MyActivityHandler : ActivityHandler
{
    protected override async Task OnMessageActivityAsync(
        ITurnContext<IMessageActivity> turnContext,
        CancellationToken cancellationToken)
    {
        // highlight-start
        var card = new
        {
            type = "AdaptiveCard",
            version = "1.0",
            body = new[]
            {
                new { type = "TextBlock", text = "hello world" }
            }
        };
        var attachment = new Attachment
        {
            ContentType = "application/vnd.microsoft.card.adaptive",
            Content = card
        };
        var activity = MessageFactory.Attachment(attachment);
        await turnContext.SendActivityAsync(activity, cancellationToken: cancellationToken);
        // highlight-end
    }
}
```
# [Teams SDK](#tab/teams-sdk)
```csharp
using Microsoft.Teams.Cards;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;

var teams = app.UseTeams();
teams.OnMessage(async (context) =>
{
    // highlight-next-line
    await context.Send(new AdaptiveCard(new TextBlock("hello world")));
});
```
---
## Attachments

# [Diff](#tab/diff)
```csharp
// highlight-error-start
-   using Microsoft.Bot.Builder;
-   using Microsoft.Bot.Schema;
// highlight-error-end
// highlight-success-start
+   using Microsoft.Teams.Apps;
+   using Microsoft.Teams.Api;
+   using Microsoft.Teams.Plugins.AspNetCore.Extensions;
// highlight-success-end

// highlight-error-start
-   public class MyActivityHandler : ActivityHandler
-   {
-       protected override async Task OnMessageActivityAsync(
-           ITurnContext<IMessageActivity> turnContext,
-           CancellationToken cancellationToken)
-       {
-           var activity = MessageFactory.Attachment(new Attachment { /* ... */ });
-           await turnContext.SendActivityAsync(activity, cancellationToken: cancellationToken);
-       }
-   }
// highlight-error-end
// highlight-success-start
+   var teams = app.UseTeams();
+   teams.OnMessage(async (context) =>
+   {
+       var activity = new MessageActivity();
+       activity.AddAttachment(new Attachment { /* ... */ });
+       await context.SendAsync(activity);
+   });
// highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```csharp
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;

public class MyActivityHandler : ActivityHandler
{
    protected override async Task OnMessageActivityAsync(
        ITurnContext<IMessageActivity> turnContext,
        CancellationToken cancellationToken)
    {
        // highlight-start
        var activity = MessageFactory.Attachment(new Attachment { /* ... */ });
        await turnContext.SendActivityAsync(activity, cancellationToken: cancellationToken);
        // highlight-end
    }
}
```
# [Teams SDK](#tab/teams-sdk)
```csharp
using Microsoft.Teams.Api;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;

var teams = app.UseTeams();
teams.OnMessage(async (context) =>
{
    // highlight-start
    var activity = new MessageActivity();
    activity.AddAttachment(new Attachment { /* ... */ });
    await context.SendAsync(activity);
    // highlight-end
});
```
---
::: zone-end

::: zone pivot="python"
# [Diff](#tab/diff)
```python
# highlight-error-start
-   from botbuilder.core import ActivityHandler, TurnContext
-   from botbuilder.schema import Activity
# highlight-error-end
# highlight-success-start
+   from microsoft_teams.api import MessageActivity, TypingActivityInput
+   from microsoft_teams.apps import ActivityContext, App
# highlight-success-end

# highlight-error-start
-   class MyActivityHandler(ActivityHandler):
-       async def on_message_activity(self, turn_context: TurnContext):
-           await turn_context.send_activity(Activity(type="typing"))
# highlight-error-end
# highlight-success-start
+   @app.on_message
+   async def on_message(context: ActivityContext[MessageActivity]):
+       await context.send(TypingActivityInput())
# highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```python
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity

class MyActivityHandler(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # highlight-next-line
        await turn_context.send_activity(Activity(type="typing"))
```
# [Teams SDK](#tab/teams-sdk)
```python
from microsoft_teams.api import MessageActivity, TypingActivityInput
from microsoft_teams.apps import ActivityContext, App

@app.on_message
async def on_message(context: ActivityContext[MessageActivity]):
    # highlight-next-line
    await context.send(TypingActivityInput())
```
---
## Strings

# [Diff](#tab/diff)
```python
# highlight-error-start
-   from botbuilder.core import ActivityHandler, TurnContext
# highlight-error-end
# highlight-success-start
+   from microsoft_teams.api import MessageActivity
+   from microsoft_teams.apps import ActivityContext, App
# highlight-success-end

# highlight-error-start
-   class MyActivityHandler(ActivityHandler):
-       async def on_message_activity(self, turn_context: TurnContext):
-           await turn_context.send_activity("hello world")
# highlight-error-end
# highlight-success-start
+   @app.on_message
+   async def on_message(context: ActivityContext[MessageActivity]):
+       await context.send("hello world")
# highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```python
from botbuilder.core import ActivityHandler, TurnContext

class MyActivityHandler(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # highlight-next-line
        await turn_context.send_activity("hello world")
```
# [Teams SDK](#tab/teams-sdk)
```python
from microsoft_teams.api import MessageActivity
from microsoft_teams.apps import ActivityContext, App

@app.on_message
async def on_message(context: ActivityContext[MessageActivity]):
    # highlight-next-line
    await context.send("hello world")
```
---
## Adaptive Cards

# [Diff](#tab/diff)
```python
# highlight-error-start
-   from botbuilder.core import ActivityHandler, TurnContext
-   from botbuilder.schema import Activity, Attachment
# highlight-error-end
# highlight-success-start
+   from microsoft_teams.api import MessageActivity
+   from microsoft_teams.apps import ActivityContext, App
+   from microsoft_teams.cards import AdaptiveCard, TextBlock
# highlight-success-end

# highlight-error-start
-   class MyActivityHandler(ActivityHandler):
-       async def on_message_activity(self, turn_context: TurnContext):
-         card = {"type": "AdaptiveCard", "version": "1.0", "body": [{"type": "TextBlock", "text": "hello world"}]}
-         attachment = Attachment(content_type="application/vnd.microsoft.card.adaptive", content=card)
-         activity = Activity(type="message", attachments=[attachment])
-         await turn_context.send_activity(activity)
# highlight-error-end
# highlight-success-start
+   @app.on_message
+   async def on_message(context: ActivityContext[MessageActivity]):
+       await context.send(AdaptiveCard().with_body([TextBlock(text="Hello from Adaptive Card!")]))
# highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```python
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity, Attachment

class MyActivityHandler(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
      # hightlight-start
      card = {"type": "AdaptiveCard", "version": "1.0", "body": [{"type": "TextBlock", "text": "hello world"}]}
      attachment = Attachment(content_type="application/vnd.microsoft.card.adaptive", content=card)
      activity = Activity(type="message", attachments=[attachment])
      await turn_context.send_activity(activity)
      # highlight-end
```
# [Teams SDK](#tab/teams-sdk)
```python
from microsoft_teams.api import MessageActivity
from microsoft_teams.apps import ActivityContext, App
from microsoft_teams.cards import AdaptiveCard, TextBlock

@app.on_message
async def on_message(context: ActivityContext[MessageActivity]):
    # highlight-next-line
    await context.send(AdaptiveCard(body=[TextBlock(text="Hello from Adaptive Card!")]))
```
---
## Attachments

# [Diff](#tab/diff)
```python
# highlight-error-start
-   from botbuilder.core import ActivityHandler, TurnContext
-   from botbuilder.schema import Activity, Attachment
# highlight-error-end
# highlight-success-start
+   from microsoft_teams.api import Attachment, MessageActivity, MessageActivityInput
+   from microsoft_teams.apps import ActivityContext, App
# highlight-success-end

# highlight-error-start
-   class MyActivityHandler(ActivityHandler):
-       async def on_message_activity(self, turn_context: TurnContext):
-         attachment = Attachment(...)
-         activity = Activity(type="message", attachments=[attachment])
-         await turn_context.send_activity(activity)
# highlight-error-end
# highlight-success-start
+   @app.on_message
+   async def on_message(context: ActivityContext[MessageActivity]):
+       attachment = Attachment(...)
+       activity = MessageActivityInput().add_attachments([attachment])
+       await context.send(activity)
# highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```python
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import Activity, Attachment

class MyActivityHandler(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # highlight-start
        attachment = Attachment(...)
        activity = Activity(type="message", attachments=[attachment])
        await turn_context.send_activity(activity)
        # highlight-end
```
# [Teams SDK](#tab/teams-sdk)
```python
from microsoft_teams.api import Attachment, MessageActivity, MessageActivityInput
from microsoft_teams.apps import ActivityContext, App

@app.on_message
async def on_message(context: ActivityContext[MessageActivity]):
    # highlight-start
    attachment = Attachment(...)
    activity = MessageActivityInput().add_attachments([attachment])
    await context.send(activity)
    # highlight-end
```
---
::: zone-end

::: zone pivot="javascript"
# [Diff](#tab/diff)
```typescript
// highlight-error-start
-    import { TeamsActivityHandler } from 'botbuilder';

-    export class ActivityHandler extends TeamsActivityHandler {
-      constructor() {
-        super();
-        this.onMessage(async (context) => {
-          await context.sendActivity({ type: 'typing' });
-        });
-      }
-    }
// highlight-error-end
// highlight-success-start
+    app.on('message', async ({ send }) => {
+      await send({ type: 'typing' });
+    });
// highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```typescript
import { TeamsActivityHandler } from 'botbuilder';

export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context) => {
      // highlight-next-line
      await context.sendActivity({ type: 'typing' });
    });
  }
}
```
# [Teams SDK](#tab/teams-sdk)
```typescript
app.on('message', async ({ send }) => {
  // highlight-next-line
  await send({ type: 'typing' });
});
```
---
## Strings

# [Diff](#tab/diff)
```typescript
// highlight-error-start
-    import { TeamsActivityHandler } from 'botbuilder';

-    export class ActivityHandler extends TeamsActivityHandler {
-      constructor() {
-        super();
-        this.onMessage(async (context) => {
-          await context.sendActivity('hello world');
-        });
-      }
-    }
// highlight-error-end
// highlight-success-start
+    app.on('message', async ({ send }) => {
+      await send('hello world');
+    });
// highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```typescript
import { TeamsActivityHandler } from 'botbuilder';

export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context) => {
      // highlight-next-line
      await context.sendActivity('hello world');
    });
  }
}
```
# [Teams SDK](#tab/teams-sdk)
```typescript
app.on('message', async ({ send }) => {
  // highlight-next-line
  await send('hello world');
});
```
---
## Adaptive Cards

# [Diff](#tab/diff)
```typescript
// highlight-error-line
-    import { TeamsActivityHandler, CardFactory } from 'botbuilder';
// highlight-success-line
+    import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';

// highlight-error-start
-    export class ActivityHandler extends TeamsActivityHandler {
-      constructor() {
-        super();
-        this.onMessage(async (context) => {
-          await context.sendActivity({
-            type: 'message',
-            attachments: [
-              CardFactory.adaptiveCard({
-                $schema: 'http://adaptivecards.io/schemas/adaptive-card.json',
-                type: 'AdaptiveCard',
-                version: '1.0',
-                body: [{
-                  type: 'TextBlock',
-                  text: 'hello world'
-                }]
-              })
-            ]
-          });
-        });
-      }
-    }
// highlight-error-end
// highlight-success-start
+    app.on('message', async ({ send }) => {
+      await send(new AdaptiveCard(new TextBlock('hello world')));
+    });
// highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```typescript
import { TeamsActivityHandler, CardFactory } from 'botbuilder';

export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context) => {
      // highlight-start
      await context.sendActivity({
        type: 'message',
        attachments: [
          CardFactory.adaptiveCard({
            $schema: 'http://adaptivecards.io/schemas/adaptive-card.json',
            type: 'AdaptiveCard',
            version: '1.0',
            body: [{
              type: 'TextBlock',
              text: 'hello world'
            }]
          })
        ]
      });
      // highlight-end
    });
  }
}
```
# [Teams SDK](#tab/teams-sdk)
```typescript
import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';

app.on('message', async ({ send }) => {
  // highlight-next-line
  await send(new AdaptiveCard(new TextBlock('hello world')));
});
```
---
## Attachments

# [Diff](#tab/diff)
```typescript
// highlight-error-line
-    import { TeamsActivityHandler } from 'botbuilder';
// highlight-success-line
+    import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';

// highlight-error-start
-    export class ActivityHandler extends TeamsActivityHandler {
-      constructor() {
-        super();
-        this.onMessage(async (context) => {
-          await context.sendActivity({
-            type: 'message',
-            attachments: [
-              ...
-            ]
-          });
-        });
-      }
-    }
// highlight-error-end
// highlight-success-start
+    app.on('message', async ({ send }) => {
+      await send(new MessageActivity().addAttachment(...));
+    });
// highlight-success-end
```
# [BotBuilder](#tab/botbuilder)
```typescript
import { TeamsActivityHandler } from 'botbuilder';

export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context) => {
      // highlight-start
      await context.sendActivity({
        type: 'message',
        attachments: [
          ...
        ]
      });
      // highlight-end
    });
  }
}
```
# [Teams SDK](#tab/teams-sdk)
```typescript

app.on('message', async ({ send }) => {
  // highlight-next-line
  await send(new MessageActivity().addAttachment(...));
});
```
---
::: zone-end

