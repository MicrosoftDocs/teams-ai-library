---
title: Proactive Activities (TypeScript)
description: Learn about Proactive Activities (TypeScript)
ms.topic: how-to
ms.date: 05/17/2025
---
# Proactive Activities (TypeScript)

The BotBuilder proactive message flow requires you to have a conversation reference stored somewhere. In Teams AI
we expose a `send` method almost identical to the one passed into our activity handlers that accepts a `conversationId`,
so all you need to store is that!


 
  
  <TabItem value="BotBuilder">
```typescript showLineNumbers
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
  
  <TabItem value="Teams AI">
```typescript showLineNumbers
    import { App } from '@microsoft/teams.apps';

    const app = new App();

    // highlight-start
    (async () => {
      await app.start();
      await app.send('your-conversation-id', 'proactive hello');
    }());
    // highlight-end
```
  
