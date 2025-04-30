---
title: Meeting Start and End Events Activity
ms.topic: reference
description: Learn how meeting start and end events enable bots to receive notifications.
ms.date: 04/30/2025
---

# Activity: Meeting Start and End Events

Meeting extensibility provides a way for bots to participate in meetings and receive notifications that are specific to meeting events. Note that Teams has three types of meetings: channel meetings, scheduled meetings, and instant meetings.

## Meeting start event

```typescript
app.on('meetingStart', async ({ activity }) => {});
```

The `meetingStart` is alias for the event name `application/vnd.microsoft.meetingStart`. This event is sent when a meeting starts.

## Meeting end event

```typescript
app.on('meetingEnd', async ({ activity }) => {});
```

The `meetingEnd` is the alias for the event name `application/vnd.microsoft.meetingEnd`. This event is sent when a meeting ends.

## App permissions

In Teams, the app manifest requires specific setup to have meetings permissions.

- The `webApplicationInfo` section must be populated with the `id` and `resource` values.
- The `permissions` section under `authorization` must have the `OnlineMeeting.ReadBasic.Chat` and `ChannelMeeting.ReadBasic.Group` permissions.

## Resources

- [Microsoft Learn: Teams Meeting Extensibility](https://learn.microsoft.com/en-us/microsoftteams/platform/apps-in-teams-meetings/meeting-apps-apis#example-of-getting-meeting-start-or-end-events)
- [Microsoft Learn: Graph API - Resource specific consent](https://learn.microsoft.com/en-us/microsoftteams/platform/graph-api/rsc/resource-specific-consent)
