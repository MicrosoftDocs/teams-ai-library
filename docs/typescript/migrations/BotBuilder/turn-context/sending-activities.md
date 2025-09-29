---
title: Sending Activities (TypeScript)
description: Migrate from BotBuilder's TurnContext activity sending to Teams AI's simplified send method with better Adaptive Card support in Teams TypeScript apps.
ms.topic: how-to
ms.date: 09/29/2025
---

# Sending Activities (TypeScript)

BotBuilders pattern for sending activities via its `TurnContext` is similar to that
in Teams AI, but one key difference is that when sending adaptive cards you don't need
to construct the entire activity yourself.

# [BotBuilder](#tab/botbuilder)
```typescript
import { TeamsActivityHandler } from 'botbuilder';

export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context) => {
      // highlight-next-line
      await context.sendActivity({ type: 'typing' });
    });
  }
}
```

# [Teams AI](#tab/teams-ai)
```typescript
app.on('message', async ({ send }) => {
  // highlight-next-line
  await send({ type: 'typing' });
});
```

---

## Strings

# [BotBuilder](#tab/botbuilder)
```typescript
import { TeamsActivityHandler } from 'botbuilder';

export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context) => {
      // highlight-next-line
      await context.sendActivity('hello world');
    });
  }
}
```

# [Teams AI](#tab/teams-ai)
```typescript
app.on('message', async ({ send }) => {
  // highlight-next-line
  await send('hello world');
});
```
---


## Adaptive Cards

# [BotBuilder](#tab/botbuilder)
```typescript
import { TeamsActivityHandler, CardFactory } from 'botbuilder';

export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context) => {
      // highlight-start
      await context.sendActivity({
        type: 'message',
        attachments: [
          CardFactory.adaptiveCard({
            $schema: 'http://adaptivecards.io/schemas/adaptive-card.json',
            type: 'AdaptiveCard',
            version: '1.0',
            body: [{
              type: 'TextBlock',
              text: 'hello world'
            }]
          })
        ]
      });
      // highlight-end
    });
  }
}
```

# [Teams AI](#tab/teams-ai)
```typescript
import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';

app.on('message', async ({ send }) => {
  // highlight-next-line
  await send(new AdaptiveCard(new TextBlock('hello world')));
});
```
---


## Attachments

# [BotBuilder](#tab/botbuilder)
```typescript
import { TeamsActivityHandler } from 'botbuilder';

export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (context) => {
      // highlight-start
      await context.sendActivity({
        type: 'message',
        attachments: [
          ...
        ]
      });
      // highlight-end
    });
  }
}
```

# [Teams AI](#tab/teams-ai)
```typescript
import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';

app.on('message', async ({ send }) => {
  // highlight-next-line
  await send(new MessageActivity().addAttachment(...));
});
```
---