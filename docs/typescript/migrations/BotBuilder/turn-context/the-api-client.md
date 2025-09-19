---
sidebar_position: 3
summary: Replace BotBuilder's static TeamsInfo class with Teams AI's injected ApiClient for cleaner API interactions.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# The API Client

BotBuilder exposes a static class `TeamsInfo` that allows you to query the api. In Teams AI
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

# [Teams AI](#tab/teams-ai)
```typescript
import { App } from '@microsoft/teams.apps';

const app = new App();

app.on('message', async ({ api, activity }) => {
  // highlight-next-line
  const members = await api.conversations.members(activity.conversation.id).get();
});
```
