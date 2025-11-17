---
sidebar_label: 🗃️ Custom Logger
title: Custom Logger
zone_pivot_groups: dev-lang
description: Configure custom loggers in your Teams app to control log levels and output destinations.
---
# Custom Logger

::: zone pivot="csharp,python,typescript"
The `App` will provide a default logger, but you can also provide your own.
The default `Logger` instance will be set to `ConsoleLogger` from the <LanguageInclude section="package-name" /> package.
::: zone-end

The `App` will provide a default logger, but you can also provide your own.
The default `Logger` instance will be set to <LanguageInclude section="default-logger" /> from the <LanguageInclude section="package-name" /> package.

::: zone pivot="csharp"
The `App` will provide a default logger, but you can also provide your own.
The default `Logger` instance will be set to <LanguageInclude section="default-logger" /> from the `Microsoft.Teams.Common` package.
::: zone-end

::: zone pivot="python"
The `App` will provide a default logger, but you can also provide your own.
The default `Logger` instance will be set to <LanguageInclude section="default-logger" /> from the `microsoft-teams-common` package.
::: zone-end

::: zone pivot="typescript"
The `App` will provide a default logger, but you can also provide your own.
The default `Logger` instance will be set to <LanguageInclude section="default-logger" /> from the `@microsoft/teams.common` package.
::: zone-end


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Apps;
using Microsoft.Teams.Common.Logging;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;

var builder = WebApplication.CreateBuilder(args);

var appBuilder = App.Builder()
    .AddLogger(new ConsoleLogger())

builder.AddTeams(appBuilder)

var app = builder.Build();
var teams = app.UseTeams();
```
::: zone-end

::: zone pivot="python"
```python
import asyncio

from microsoft.teams.api import MessageActivity
from microsoft.teams.api.activities.typing import TypingActivityInput
from microsoft.teams.apps import ActivityContext, App
from microsoft.teams.common import ConsoleLogger, ConsoleLoggerOptions

logger = ConsoleLogger().create_logger("echo", ConsoleLoggerOptions(level="debug"))
app = App(logger=logger)

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    logger.debug(ctx.activity)
    await ctx.reply(TypingActivityInput())
    await ctx.send(f"You said '{ctx.activity.text}'")


if __name__ == "__main__":
    asyncio.run(app.start())
```
::: zone-end

::: zone pivot="typescript"
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
::: zone-end
