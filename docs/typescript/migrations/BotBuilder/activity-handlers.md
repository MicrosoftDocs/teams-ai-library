---
title: Activity Handlers (TypeScript)
description: Learn about Activity Handlers (TypeScript)
ms.topic: how-to
ms.date: 05/17/2025
---
# Activity Handlers (TypeScript) (preview)

[This article is prerelease documentation and is subject to change.]


A BotBuilder `ActivityHandler` is similar to the activity routing of the Teams AI `App`.
The `BotBuilderPlugin` accepts a botbuilder Activity Handler instance so you can keep using your
existing activity handlers while migrating however many you want to new Teams AI handlers. This allows for
a more incremental migration strategy.

> [!NOTE]
> this snippet shows how to use the `BotBuilderPlugin` to route activities using
> botbuilder alongside the default Teams AI activity routing.

# [index.ts](#tab/index)

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

# [adapter.ts](#tab/adapter)

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
  
# [activity-handler.ts](#tab/activity-handler)
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

```
hi from botbuilder...
hi from teams...
```