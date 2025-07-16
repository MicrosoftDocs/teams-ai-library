---
title: Signing In (preview) (C#)
description: Learn about Signing In (preview) (C#)
ms.topic: how-to
ms.date: 07/16/2025
---

# Signing In (preview) (C#)

[This article is prerelease documentation and is subject to change.]

Prompting the user to sign in using an `OAuth` connection has
never been easier! Just use the `signin` method to send the request
and the listen to the `signin` event to handle the token result.

```ts
app.on('message', async ({ log, signin, userGraph, isSignedIn }) => {
  if (!isSignedIn) {
    await signin({
      // Customize the OAuth card text (only applies to OAuth flow, not SSO)
      oauthCardText: 'Sign in to your account',
      signInButtonText: 'Sign in' 
    }); // call signin for your auth connection...
    return;
  }

  const me = await userGraph.me.get();
  log.info(`user "${me.displayName}" already signed in!`);
});

app.event('signin', async ({ send, userGraph, token }) => {
  const me = await userGraph.me.get();
  await send(`user "${me.displayName}" signed in. Here's the token: ${JSON.stringify(token)}`);
});
```