---
title: Middleware (preview) (TypeScript)
description: Learn about building middleware for logging and validation using the Teams AI Library for TypeScript.
ms.topic: how-to
ms.date: 07/16/2025
---
# Middleware (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

Middleware is a useful tool for logging, validation, and more.
You can easily register your own middleware using the `app.use` method.

Below is an example of a middleware that will log the elapse time of all handers
that come after it.


```typescript
app.use(async ({ log, next }) => {
  const startedAt = new Date();
  await next();
  log.debug(new Date().getTime() - startedAt.getTime());
});
```