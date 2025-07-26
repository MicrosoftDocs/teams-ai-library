---
title: Proactive Activities (preview) (TypeScript)
description: Migration guide for updating BotBuilder proactive messages to use Teams AI Library for TypeScript.
ms.topic: how-to
ms.date: 07/16/2025
---
# Proactive Activities (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

The BotBuilder proactive message flow requires you to have a conversation reference stored somewhere. In Teams AI
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

# [Teams AI](#tab/teams-ai)

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