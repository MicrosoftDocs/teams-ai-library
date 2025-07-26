---
title: Signing Out (preview) (TypeScript)
description: Implement authentication code to sign out your user using the
  Teams AI Library for TypeScript.
ms.topic: how-to
ms.date: 07/16/2025
---
# Signing Out (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

Sign a user out by calling the `signout` method to discard the cached access token in the Bot Framework token service.

```ts
app.message('/signout', async ({ send, signout, isSignedIn }) => {
  if (!isSignedIn) return;
  await signout(); // call signout for your auth connection...
  await send('you have been signed out!');
});
```