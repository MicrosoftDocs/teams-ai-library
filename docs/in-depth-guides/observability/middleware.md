---
title: Observability Middleware
description: Create middleware for logging, validation, and other cross-cutting concerns using the app.use method.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---
# Observability Middleware

::: zone pivot="csharp"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="python,typescript"
Middleware is a useful tool for logging, validation, and more.
You can easily register your own middleware using the `app.use` method.
::: zone-end

::: zone pivot="python,typescript"
Below is an example of a middleware that will log the elapse time of all handlers that come after it.
::: zone-end

::: zone pivot="python"
```python
@app.use
async def log_activity(ctx: ActivityContext[MessageActivity]):
    started_at = datetime.now()
    await ctx.next()
    ctx.logger.debug(f"{datetime.now() - started_at}")
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.use(async ({ log, next }) => {
  const startedAt = new Date();
  await next();
  log.debug(new Date().getTime() - startedAt.getTime());
});
```
::: zone-end


