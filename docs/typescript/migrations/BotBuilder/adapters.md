---
title: Adapters (preview) (TypeScript)
description: Migration guide for upgrading otBuilder adapters to the Microsoft Teams AI Library for TypeScript.
ms.topic: how-to
ms.date: 07/16/2025
---
# Adapters (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

A BotBuilder `Adapter` is similar to a Teams AI `Plugin` in the sense that they are both
an abstraction that is meant to send/receive activities. To make migrating stress free we have
shipped a pre-built `BotBuilderPlugin` that can accept a botbuilder Adapter instance.

> [!NOTE]
> this snippet shows how to use the `BotBuilderPlugin` to send/receive activities using
> botbuilder instead of the default Teams AI http plugin.

# [index.ts](#tab/indexts)

```typescript
import { App } from '@microsoft/teams.apps';
import { BotBuilderPlugin } from '@microsoft/teams.botbuilder';

import adapter from './adapter';
import handler from './activity-handler';

const app = new App({
  // highlight-next-line
  plugins: [new BotBuilderPlugin({ adapter, handler })],
});

app.on('message', async ({ send }) => {
  await send('hi from teams...');
});

(async () => {
  await app.start();
})();
```

# [adapter.ts](#tab/adapterts)

```typescript
import { CloudAdapter } from 'botbuilder';

// replace with your BotAdapter
// highlight-start
const adapter = new CloudAdapter(
  new ConfigurationBotFrameworkAuthentication(
    {},
    new ConfigurationServiceClientCredentialFactory({
      MicrosoftAppType: tenantId ? 'SingleTenant' : 'MultiTenant',
      MicrosoftAppId: clientId,
      MicrosoftAppPassword: clientSecret,
      MicrosoftAppTenantId: tenantId,
    })
  )
);
// highlight-end

export default adapter;
```

# [activity-handler.ts](#tab/activityhandlerts)

```typescript
import { TeamsActivityHandler } from 'botbuilder';

// replace with your TeamsActivityHandler
// highlight-start
export class ActivityHandler extends TeamsActivityHandler {
  constructor() {
    super();
    this.onMessage(async (ctx, next) => {
      await ctx.sendActivity('hi from botbuilder...');
      await next();
    });
  }
}
// highlight-end

const handler = new ActivityHandler();
export default handler;
```

---

```text
hi from botbuilder...
hi from teams...
```