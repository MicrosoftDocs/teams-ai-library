---
title: The API Client (TypeScript)
description: Learn about The API Client (TypeScript)
ms.topic: how-to
ms.date: 06/03/2025
---

# The API Client (TypeScript) (preview)

[This article is prerelease documentation and is subject to change.]

BotBuilder exposes a static class `TeamsInfo` that allows you to query the api. In Teams AI
we pass an instance of our `ApiClient` into all our activity handlers.

# [BotBuilder](#tab/botbuilder)
```typescript showLineNumbers
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
# [Teams AI](#tab/teamsai)
```typescript showLineNumbers
    import { App } from '@microsoft/teams.apps';

    const app = new App();

    app.on('message', async ({ api, activity }) => {
      // highlight-next-line
      const members = await api.conversations.members(activity.conversation.id).get();
    });
```
---