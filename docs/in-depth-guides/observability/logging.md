---
title: 'Custom Logger'
description: 'Configure custom loggers in your Teams app to control log levels and output destinations.'
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 06/29/2026
---

#  Custom Logger

::: zone pivot="csharp"
The `App` will provide a default logger, but you can also provide your own.
The default `Logger` instance will be set to `ConsoleLogger` from the `Microsoft.Teams.Common` package.
::: zone-end

::: zone pivot="python"
The `App` will provide a default logger, but you can also provide your own.
The default `Logger` instance will be set to Python's standard `logging` module, using `logging.getLogger(__name__)` per module. from the `microsoft-teams-common` package.
::: zone-end

::: zone pivot="typescript"
The `App` will provide a default logger, but you can also provide your own.
The default `Logger` instance will be set to `ConsoleLogger` from the `@microsoft/teams.common` package.
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
The Python SDK uses standard `logging`  there's no custom logger to inject into `App`. To see SDK log output, attach a handler to the `microsoft_teams` logger hierarchy. The SDK ships a `ConsoleFormatter` with color-coded output if you want it:

```python
import logging
import os
from microsoft_teams.common import ConsoleFormatter

handler = logging.StreamHandler()
handler.setFormatter(ConsoleFormatter())
logging.getLogger("microsoft_teams").addHandler(handler)
logging.getLogger("microsoft_teams").setLevel(
    os.getenv("LOG_LEVEL", "INFO").upper()
)
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


## Log Levels


::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
Python's standard `logging` levels apply: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
::: zone-end

::: zone pivot="typescript"
Available levels, from most to least severe: `error`, `warn`, `info`, `debug`, `trace`. The default is `info`. Setting `level: 'debug'` emits `error`, `warn`, `info`, and `debug`  but not `trace`.
::: zone-end


## Filtering by Logger Name

Each logger is created with a name. You can filter which loggers emit output by providing a name pattern, using `*` as a wildcard.


::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
Use `ConsoleFilter` to limit which loggers emit, matched by name with `*` wildcards:

```python
from microsoft_teams.common import ConsoleFilter, ConsoleFormatter

handler = logging.StreamHandler()
handler.setFormatter(ConsoleFormatter())
handler.addFilter(ConsoleFilter("microsoft_teams*"))  # only SDK loggers
logging.getLogger().addHandler(handler)
```
::: zone-end

::: zone pivot="typescript"
Each logger has a name. The `pattern` option filters which loggers emit, with `*` as a wildcard. Prefix a pattern with `-` to exclude. Combine with commas.

```typescript
new ConsoleLogger('my-app', { pattern: '@teams*' });        // only SDK loggers
new ConsoleLogger('my-app', { pattern: '*,-@teams/http*' }); // everything except HTTP
```
::: zone-end


## Environment Variables


::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
The Python SDK does not read logging environment variables on its own. If you want `LOG_LEVEL` to control verbosity, read it yourself at startup:

```python
import os
logging.getLogger().setLevel(os.getenv("LOG_LEVEL", "INFO").upper())
```
::: zone-end

::: zone pivot="typescript"
The TypeScript SDK's `ConsoleLogger` reads two environment variables at construction:

| Variable     | Purpose                          | Example                 |
| ------------ | -------------------------------- | ----------------------- |
| `LOG_LEVEL`  | Minimum severity                 | `LOG_LEVEL=debug`       |
| `LOG`        | Logger name pattern (wildcards)  | `LOG=@teams*`           |

Env vars override options passed to the constructor. If you do not pass a logger to `App`, the SDK creates a default `ConsoleLogger` named `@teams/app`  so `LOG_LEVEL=debug` alone is enough to enable debug output.

> **Gotcha:** `LOG` is a name filter, not a toggle. Setting `LOG` to a pattern that doesn't match the default `@teams/app` (for example `LOG=my-app*`) silences the default logger. If in doubt, unset `LOG` to match everything.
::: zone-end



::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
## Child Loggers

Call `log.child('scope')` on an existing logger to get a scoped logger. Its name is `parent/scope`, and pattern/level are inherited.

```typescript
app.on('message', async ({ log }) => {
  const msgLog = log.child('message-handler');
  msgLog.debug('processing'); // logged as "@teams/app/message-handler"
});
```
::: zone-end


