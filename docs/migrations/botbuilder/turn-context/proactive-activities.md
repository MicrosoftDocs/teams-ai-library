---
sidebar_position: 2
sidebar_label: Proactive Activities
title: Proactive Activities
languages: ['typescript']
summary: Migrate from BotBuilder's complex conversation reference handling to Teams SDK's simple conversation ID-based proactive messaging.
zone_pivot_groups: dev-lang
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Proactive Activities


::: zone pivot="csharp"
This page isn't available for C#.
::: zone-end

::: zone pivot="python"
This page isn't available for Python.
::: zone-end

::: zone pivot="typescript"
The BotBuilder proactive message flow requires you to have a conversation reference stored somewhere. In Teams SDK
we expose a `send` method almost identical to the one passed into our activity handlers that accepts a `conversationId`,
so all you need to store is that!

# [BotBuilder](#tab/botbuilder)
```typescript
import {
  CloudAdapter,
  ConfigurationBotFrameworkAuthentication,
  ConversationReference,
} from 'botbuilder';

const auth = new ConfigurationBotFrameworkAuthentication(process.env);
const adapter = new CloudAdapter(auth);

// highlight-start
(async () => {
  const conversationReference: ConversationReference = {
    serviceUrl: '...',
    bot: { ... },
    channelId: 'msteams',
    conversation: { ... },
    user: { ... },
  };

  await adapter.continueConversationAsync(process.env.MicrosoftAppId ?? '', conversationReference, async context => {
    await context.sendActivity('proactive hello');
  });
}());
// highlight-end
```

# [Teams SDK](#tab/teams-sdk)
```typescript
import { App } from '@microsoft/teams.apps';

const app = new App();

// highlight-start
(async () => {
  await app.start();
  await app.send('your-conversation-id', 'proactive hello');
}());
// highlight-end
```

---


::: zone-end
