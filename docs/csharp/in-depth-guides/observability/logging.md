---
title: Custom Logger (preview) (C#)
description: Implement custom logging in Teams applications using the Teams
  AI Library for C#.
ms.topic: how-to
ms.date: 07/16/2025
---
# Custom Logger (preview) (C#)

[This article is prerelease documentation and is subject to change.]

The `App` will provide a default logger, but you can also provide your own.
The default `Logger` instance will be set to `ConsoleLogger` from the
`@microsoft/teams.common` package.


```typescript
import { App } from '@microsoft/teams.apps';
import { ConsoleLogger } from '@microsoft/teams.common';

// initialize app with custom console logger
// set to debug log level
const app = new App({
  logger: new ConsoleLogger('echo', { level: 'debug' }),
});

app.on('message', async ({ send, activity, log }) => {
  log.debug(activity);
  await send({ type: 'typing' });
  await send(`you said "${activity.text}"`);
});

(async () => {
  await app.start();
})();
```