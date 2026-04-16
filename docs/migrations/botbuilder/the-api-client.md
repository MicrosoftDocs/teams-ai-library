---
title: The API Client
description: Replace BotBuilder's static TeamsInfo class with Teams SDK's injected ApiClient for cleaner API interactions.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 04/14/2026
---


# The API Client

BotBuilder exposes a static class `TeamsInfo` that allows you to query the api. In Teams SDK
we pass an instance of our `ApiClient` into all our activity handlers through the context.

> [!TIP]
> The Teams SDK `ApiClient` uses a fluent API pattern that makes it easier to discover available methods through IDE autocompletion.


::: zone pivot="csharp"
# [Diff](#tab/diff)
  ```csharp
  // highlight-error-start
-  using Microsoft.Bot.Builder;
-  using Microsoft.Bot.Builder.Teams;
  // highlight-error-end
  // highlight-success-line
+  using Microsoft.Teams.Apps;

  // highlight-error-start
-  public class MyActivityHandler : ActivityHandler
-  {
-      protected override async Task OnMessageActivityAsync(
-          ITurnContext<IMessageActivity> turnContext,
-          CancellationToken cancellationToken)
-      {
-          var members = await TeamsInfo.GetMembersAsync(turnContext, cancellationToken);
-      }
-  }
  // highlight-error-end
  // highlight-success-start
+  var teams = app.UseTeams();
+  teams.OnMessage(async (context) =>
+  {
+      var members = await context.Api.Conversations.Members.GetAsync(context.Activity.Conversation.Id);
+  });
  // highlight-success-end
  ```
# [BotBuilder](#tab/botbuilder)
```csharp
using Microsoft.Bot.Builder;
using Microsoft.Bot.Builder.Teams;

public class MyActivityHandler : TeamsActivityHandler
{
    protected override async Task OnMessageActivityAsync(
        ITurnContext<IMessageActivity> turnContext,
        CancellationToken cancellationToken)
    {
        // highlight-next-line
        var members = await TeamsInfo.GetMembersAsync(turnContext, cancellationToken);
    }
}
```
# [Teams SDK](#tab/teams-sdk)
```csharp
using Microsoft.Teams.Apps;

app.OnMessage(async (context) =>
{
    // highlight-next-line
    var members = await context.Api.Conversations.Members.GetAsync(context.Activity.Conversation.Id);
});
```
---
::: zone-end

::: zone pivot="python"
# [Diff](#tab/diff)
  ```python
  # highlight-error-start
-  from botbuilder.core import ActivityHandler, TurnContext
-  from botbuilder.core.teams import TeamsInfo
  # highlight-error-end
  # highlight-success-line
+  from microsoft_teams.apps import ActivityContext
+  from microsoft_teams.api import MessageActivity

  # highlight-error-start
-  class MyActivityHandler(ActivityHandler):
-      async def on_message_activity(self, turn_context: TurnContext):
-          members = await TeamsInfo.get_members(turn_context)
  # highlight-error-end
  # highlight-success-start
+  @app.on_message
+  async def on_message(context: ActivityContext[MessageActivity]):
+      members = await context.api.conversations.members(context.activity.conversation.id).get_all()
  # highlight-success-end
  ```
# [BotBuilder](#tab/botbuilder)
```python
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.core.teams import TeamsInfo

class MyActivityHandler(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # highlight-next-line
        members = await TeamsInfo.get_members(turn_context)
```
# [Teams SDK](#tab/teams-sdk)
```python
from microsoft_teams.api import MessageActivity
from microsoft_teams.apps import ActivityContext

@app.on_message
async def on_message(context: ActivityContext[MessageActivity]):
    # highlight-next-line
    members = await context.api.conversations.members(context.activity.conversation.id).get()
```
---
::: zone-end

::: zone pivot="typescript"
# [Diff](#tab/diff)
  ```typescript
  // highlight-error-start
-  import {
-    CloudAdapter,
-    ConfigurationBotFrameworkAuthentication,
-    TeamsInfo,
-  } from 'botbuilder';
  // highlight-error-end
  // highlight-success-line
+  import { App } from '@microsoft/teams.apps';

  // highlight-error-start
-  const auth = new ConfigurationBotFrameworkAuthentication(process.env);
-  const adapter = new CloudAdapter(auth);
  // highlight-error-end
  // highlight-success-line
+  const app = new App();

  // highlight-error-start
-  export class ActivityHandler extends TeamsActivityHandler {
-    constructor() {
-      super();
-      this.onMessage(async (context) => {
-        const members = await TeamsInfo.getMembers(context);
-      });
-    }
-  }
  // highlight-error-end
  // highlight-success-start
+  app.on('message', async ({ api, activity }) => {
+    const members = await api.conversations.members(activity.conversation.id).get();
+  });
  // highlight-success-end
  ```
# [BotBuilder](#tab/botbuilder)
```typescript
import {
  CloudAdapter,
  ConfigurationBotFrameworkAuthentication,
  TeamsInfo,
} from 'botbuilder';

const auth = new ConfigurationBotFrameworkAuthentication(process.env);
const adapter = new CloudAdapter(auth);

export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context) => {
      // highlight-next-line
      const members = await TeamsInfo.getMembers(context);
    });
  }
}
```
# [Teams SDK](#tab/teams-sdk)
```typescript
import { App } from '@microsoft/teams.apps';

const app = new App();

app.on('message', async ({ api, activity }) => {
  // highlight-next-line
  const members = await api.conversations.members(activity.conversation.id).get();
});
```
---
::: zone-end


## Mapping TeamsInfo APIs to Teams SDK ApiClient Methods

The following table shows common BotBuilder `TeamsInfo` methods and their equivalent Teams SDK `ApiClient` methods:


::: zone pivot="csharp"
| BotBuilder (TeamsInfo) | Teams SDK (ApiClient) |
|------------------------|----------------------|
| `TeamsInfo.GetMemberAsync(context, userId)` | `Api.Conversations.Members.GetByIdAsync(conversationId, userId)` |
| `TeamsInfo.GetTeamDetailsAsync(context, teamId)` | `Api.Teams.GetByIdAsync(teamId)` |
| `TeamsInfo.GetMeetingInfoAsync(context, meetingId)` | `Api.Meetings.GetByIdAsync(meetingId)` |
| `TeamsInfo.SendMessageToTeamsChannelAsync(context, teamId, message)` | `Api.Conversations.CreateAsync(CreateRequest)` then `Api.Conversations.Activities.CreateAsync(conversationId, activity)` |
::: zone-end

::: zone pivot="python"
| BotBuilder (TeamsInfo) | Teams SDK (ApiClient) |
|------------------------|----------------------|
| `TeamsInfo.getMembers(context, user_id)` | `api.conversations.members(conversation_id).get(user_id)` |
| `TeamsInfo.get_team_details(context, team_id)` | `api.teams.get_by_id(team_id)` |
| `TeamsInfo.get_meeting_info(context, meeting_id)` | `api.meetings.get_by_id(meeting_id)` |
| `TeamsInfo.send_message_to_teams_channel(context, team_id, message)` | `api.conversations.create(CreateConversationParams)` then `api.conversations.activities(conversation_id).create(activity)` |
::: zone-end

::: zone pivot="typescript"
| BotBuilder (TeamsInfo) | Teams SDK (ApiClient) |
|------------------------|----------------------|
| `TeamsInfo.getMember(context, userId)` | `api.conversations.members(conversationId).getById(userId)` |
| `TeamsInfo.getTeamDetails(context, teamId)` | `api.teams.getById(teamId)` |
| `TeamsInfo.getMeetingInfo(context, meetingId)` | `api.meetings.getById(meetingId)` |
| `TeamsInfo.sendMessageToTeamsChannel(context, teamId, message)` | `api.conversations.create(CreateConversationParams)` then `api.conversations.activities(conversationId).create(activity)` |
::: zone-end
