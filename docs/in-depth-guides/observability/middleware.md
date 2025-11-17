---
sidebar_position: 1
title: 'Middleware'
summary: Create middleware for logging, validation, and other cross-cutting concerns using the app.use method.
zone_pivot_groups: dev-lang
---

# Middleware

::: zone pivot="csharp"
Middleware is a useful tool for logging, validation, and more.
You can easily register your own middleware using the `app.Use` method.
::: zone-end

::: zone pivot="python,typescript"
Middleware is a useful tool for logging, validation, and more.
You can easily register your own middleware using the `app.use` method.
::: zone-end

Below is an example of a middleware that will log the elapse time of all handlers that come after it.


::: zone pivot="csharp"
```csharp
app.Use(async context =>
{
    var start = DateTime.UtcNow;
    try
    {
        await context.Next();
    } catch
    {
        context.Log.Error("error occurred during activity processing");
    }
    context.Log.Debug($"request took {(DateTime.UtcNow - start).TotalMilliseconds}ms");
});
```
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

