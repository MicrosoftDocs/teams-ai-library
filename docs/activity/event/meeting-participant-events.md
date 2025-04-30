---
title: Meeting Participant Events Activity
ms.topic: reference
description: Learn how participant events allow bots to receive meeting notifications about users in a meeting.
ms.date: 04/30/2025
---

# Activity: Meeting Participant Events

Meeting extensibility on Teams also provides events such as a user joining or leaving a meeting.

## Meeting participant join event

```typescript
app.on('meetingParticipantJoin', async ({ activity }) => {});
```

The `meetingParticipantJoin` is the alias for the event name `application/vnd.microsoft.meetingParticipantJoin`. This event is sent when a user joins a meeting.

## Meeting participant leave event

```typescript
app.on('meetingParticipantLeave', async ({ activity }) => {});
```

The `meetingParticipantLeave` is the alias for the event name `application/vnd.microsoft.meetingParticipantLeave`. This event is sent when a user leaves a meeting.

## App permissions

In Teams, the app manifest requires specific setup to have meeting participant events permissions.

- The `permissions` section under `authorization` must have the `OnlineMeetingParticipant.Read.Chat` permission.
- The bot must have participant meeting event subscriptions enabled in the [Developer Portal](https://dev.teams.microsoft.com/).

## Resources

- [Microsoft Learn: Teams meeting extensibility participant events](/microsoftteams/platform/apps-in-teams-meetings/meeting-apps-apis)
- [Microsoft Learn: Graph API - resource specific consent](/microsoftteams/platform/graph-api/rsc/resource-specific-consent)
