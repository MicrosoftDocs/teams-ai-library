---
title: 📖 [🔒 User Authentication](/bots/how-to/authentication/add-authentication) (preview)
description: Learn about 📖 [🔒 User Authentication](/bots/how-to/authentication/add-authentication) (preview)
ms.topic: how-to
ms.date: 04/30/2025
---

# 📖 [🔒 User Authentication](/bots/how-to/authentication/add-authentication) (preview)

[This article is prerelease documentation and is subject to change.]

Prompting the user to sign in using an `OAuth` connection has
never been easier! Just use the `signin` method to send the request
and the listen to the `signin` event to handle the token result.

```typescript
app.on('message', async ({ signin, send, isSignedIn }) => {
  if (!isSignedIn) {
    await signin(); // call signin for your auth connection...
    return;
  }

  await send('you are already signed in!');
});

app.event('signin', async ({ token }) => {
  // do something with the token...
});
```