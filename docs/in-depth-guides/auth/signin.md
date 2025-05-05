---
title: Initiating Signing In
description: Learn about initiating signing in using OAuth connection.
ms.topic: how-to
ms.date: 05/02/2025
---

# Initiating Signing In (preview)

[This article is prerelease documentation and is subject to change.]

Prompting the user to sign in using an `OAuth` connection has
never been easier! Just use the `signin` method to send the request
and the listen to the `signin` event to handle the token result.

```typescript
app.on('message', async ({ log, signin, api, isSignedIn }) => {
  if (!isSignedIn) {
    await signin(); // call signin for your auth connection...
    return;
  }

  const me = await api.user.me.get();
  log.info(`user "${me.displayName}" already signed in!`);
});

app.event('signin', async ({ send, api, token }) => {
  const me = await api.user.me.get();
  await send(`user "${me.displayName}" signed in. Here's the token: ${token}`);
});

```