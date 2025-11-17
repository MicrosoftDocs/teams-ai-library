---
sidebar_position: 3
sidebar_label: The API Client
title: The API Client
languages: ['typescript']
summary: Replace BotBuilder's static TeamsInfo class with Teams SDK's injected ApiClient for cleaner API interactions.
zone_pivot_groups: dev-lang
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# The API Client


::: zone pivot="csharp"
This page isn't available for C#.
::: zone-end

::: zone pivot="python"
This page isn't available for Python.
::: zone-end

::: zone pivot="typescript"
BotBuilder exposes a static class `TeamsInfo` that allows you to query the api. In Teams SDK
we pass an instance of our `ApiClient` into all our activity handlers.

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
