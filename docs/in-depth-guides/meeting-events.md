---
title: 'Meeting Events'
description: 'Guide to handling meeting events in Teams applications, covering meeting lifecycle events such as meeting start, meeting end, participant join, and participant leave events.'
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 06/29/2026
---

# Meeting Events

Microsoft Teams provides meeting events that allow your application to respond to various meeting lifecycle changes. Your app can listen to events like when a meeting starts, meeting ends, and participant activities to create rich, interactive experiences.

## Overview

Meeting events enable your application to:
- Send notifications when meetings start or end
- Track participant activity (join/leave events)
- Display relevant information or cards based on meeting context
- Integrate with meeting workflows

## Configuring Your Bot

There are a few requirements in the Teams app manifest (`manifest.json`) to support these events.

1. The scopes section must include `team`, and `groupChat`

```json
bots": [
        {
            "botId": "",
            "scopes": [
                "team",
                "personal",
                "groupChat"
            ],
            "isNotificationOnly": false
        }
    ]
```

2. In the authorization section, make sure to specify the following resource-specific permissions:

```json
 "authorization":{
        "permissions":{
            "resourceSpecific":[
                {
                    "name":"OnlineMeetingParticipant.Read.Chat",
                    "type":"Application"
                },
                {
                    "name":"ChannelMeeting.ReadBasic.Group",
                    "type":"Application"
                },
                {
                    "name":"OnlineMeeting.ReadBasic.Chat",
                    "type":"Application"
                }
                ]
            }
        }
```

3. In the Teams Developer Portal, for your `Bot`, make sure the `Meeting Event Subscriptions` are checked off. This enables you to receive the Meeting Participant events. For these events, you must create your Bot via TDP.

## Meeting Start Event

When a meeting starts, your app can handle the `meetingStart` event to send a notification or card to the meeting chat.


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities;
using Microsoft.Teams.Apps.Activities.Events;
using Microsoft.Teams.Cards;

// Register meeting start handler
teamsApp.OnMeetingStart(async (context, cancellationToken) =>
{
    var activity = context.Activity.Value;
    var startTime = activity.StartTime.ToLocalTime();

    var card = new AdaptiveCard
    {
        Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
        Body = new List<CardElement>
        {
            new TextBlock($"'{activity.Title}' has started at {startTime}.")
            {
                Wrap = true,
                Weight = TextWeight.Bolder
            }
        },
        Actions = new List<Microsoft.Teams.Cards.Action>
        {
            new OpenUrlAction(activity.JoinUrl)
            {
                Title = "Join the meeting",
            }
        }
    };

    await context.Send(card, cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api.activities.event import MeetingStartEventActivity
from microsoft_teams.apps import ActivityContext, App
from microsoft_teams.cards import AdaptiveCard, OpenUrlAction, TextBlock

app = App()

@app.on_meeting_start
async def handle_meeting_start(ctx: ActivityContext[MeetingStartEventActivity]):
    meeting_data = ctx.activity.value
    start_time = meeting_data.start_time.strftime("%c")

    card = AdaptiveCard(
        body=[
            TextBlock(
                text=f"'{meeting_data.title}' has started at {start_time}.",
                wrap=True,
                weight="Bolder",
            )
        ],
        actions=[OpenUrlAction(url=meeting_data.join_url, title="Join the meeting")],
    )

    await ctx.send(card)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
import { AdaptiveCard, TextBlock, OpenUrlAction, ActionSet } from '@microsoft/teams.cards';

const app = new App();

app.on('meetingStart', async ({ activity, send }) => {
  const meetingData = activity.value;
  const startTime = new Date(meetingData.StartTime).toLocaleString();

  const card = new AdaptiveCard(
    new TextBlock(`'${meetingData.Title}' has started at ${startTime}.`, {
      wrap: true,
      weight: 'Bolder'
    }),
    new ActionSet(
      new OpenUrlAction(meetingData.JoinUrl).withTitle('Join the meeting')
    )
  );

  await send(card);
});
```
::: zone-end


## Meeting End Event

When a meeting ends, your app can handle the `meetingEnd` event to send a summary or follow-up information.


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities;
using Microsoft.Teams.Apps.Activities.Events;
using Microsoft.Teams.Cards;

// Register meeting end handler
teamsApp.OnMeetingEnd(async (context, cancellationToken) =>
{
    var activity = context.Activity.Value;
    var endTime = activity.EndTime.ToLocalTime();

    var card = new AdaptiveCard
    {
        Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
        Body = new List<CardElement>
        {
            new TextBlock($"'{activity.Title}' has ended at {endTime}.")
            {
                Wrap = true,
                Weight = TextWeight.Bolder
            }
        }
    };

    await context.Send(card, cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api.activities.event import MeetingEndEventActivity
from microsoft_teams.apps import ActivityContext, App
from microsoft_teams.cards import AdaptiveCard, TextBlock

app = App()

@app.on_meeting_end
async def handle_meeting_end(ctx: ActivityContext[MeetingEndEventActivity]):
    meeting_data = ctx.activity.value
    end_time = meeting_data.end_time.strftime("%c")

    card = AdaptiveCard(
        body=[
            TextBlock(
                text=f"'{meeting_data.title}' has ended at {end_time}.",
                wrap=True,
                weight="Bolder",
            )
        ]
    )

    await ctx.send(card)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';

const app = new App();

app.on('meetingEnd', async ({ activity, send }) => {
  const meetingData = activity.value;
  const endTime = new Date(meetingData.EndTime).toLocaleString();

  const card = new AdaptiveCard(
    new TextBlock(`'${meetingData.Title}' has ended at ${endTime}.`, {
      wrap: true,
      weight: 'Bolder'
    })
  );

  await send(card);
});
```
::: zone-end


## Participant Join Event

When a participant joins a meeting, your app can handle the `meetingParticipantJoin` event to welcome them or display their role.


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities;
using Microsoft.Teams.Apps.Activities.Events;
using Microsoft.Teams.Cards;

// Register participant join handler
teamsApp.OnMeetingJoin(async (context, cancellationToken) =>
{
    var activity = context.Activity.Value;
    var member = activity.Members[0].User.Name;
    var role = activity.Members[0].Meeting.Role;

    var card = new AdaptiveCard
    {
        Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
        Body = new List<CardElement>
        {
            new TextBlock($"{member} has joined the meeting as {role}.")
            {
                Wrap = true,
                Weight = TextWeight.Bolder
            }
        }
    };

    await context.Send(card, cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api.activities.event import MeetingParticipantJoinEventActivity
from microsoft_teams.apps import ActivityContext, App
from microsoft_teams.cards import AdaptiveCard, TextBlock

app = App()

@app.on_meeting_participant_join
async def handle_meeting_participant_join(ctx: ActivityContext[MeetingParticipantJoinEventActivity]):
    meeting_data = ctx.activity.value
    member = meeting_data.members[0].user.name
    role = meeting_data.members[0].meeting.role if hasattr(meeting_data.members[0].meeting, "role") else "a participant"

    card = AdaptiveCard(
        body=[
            TextBlock(
                text=f"{member} has joined the meeting as {role}.",
                wrap=True,
                weight="Bolder",
            )
        ]
    )

    await ctx.send(card)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';

const app = new App();

app.on('meetingParticipantJoin', async ({ activity, send }) => {
  const meetingData = activity.value;
  const member = meetingData.members[0].user.name;
  const role = meetingData.members[0].meeting.role;

  const card = new AdaptiveCard(
    new TextBlock(`${member} has joined the meeting as ${role}.`, {
      wrap: true,
      weight: 'Bolder'
    })
  );

  await send(card);
});
```
::: zone-end


## Participant Leave Event

When a participant leaves a meeting, your app can handle the `meetingParticipantLeave` event to notify others.


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities;
using Microsoft.Teams.Apps.Activities.Events;
using Microsoft.Teams.Cards;

// Register participant leave handler
teamsApp.OnMeetingLeave(async (context, cancellationToken) =>
{
    var activity = context.Activity.Value;
    var member = activity.Members[0].User.Name;

    var card = new AdaptiveCard
    {
        Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
        Body = new List<CardElement>
        {
            new TextBlock($"{member} has left the meeting.")
            {
                Wrap = true,
                Weight = TextWeight.Bolder
            }
        }
    };

    await context.Send(card, cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api.activities.event import MeetingParticipantLeaveEventActivity
from microsoft_teams.apps import ActivityContext, App
from microsoft_teams.cards import AdaptiveCard, TextBlock

app = App()

@app.on_meeting_participant_leave
async def handle_meeting_participant_leave(ctx: ActivityContext[MeetingParticipantLeaveEventActivity]):
    meeting_data = ctx.activity.value
    member = meeting_data.members[0].user.name

    card = AdaptiveCard(
        body=[
            TextBlock(
                text=f"{member} has left the meeting.",
                wrap=True,
                weight="Bolder",
            )
        ]
    )

    await ctx.send(card)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';

const app = new App();

app.on('meetingParticipantLeave', async ({ activity, send }) => {
  const meetingData = activity.value;
  const member = meetingData.members[0].user.name;

  const card = new AdaptiveCard(
    new TextBlock(`${member} has left the meeting.`, {
      wrap: true,
      weight: 'Bolder'
    })
  );

  await send(card);
});
```
::: zone-end


