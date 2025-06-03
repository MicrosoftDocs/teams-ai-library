---
title: Signing Out (C#)
description: Learn about Signing Out (C#)
ms.topic: how-to
ms.date: 06/03/2025
---

# Signing Out (C#)

Sign a user out by calling the `signout` method to discard the cached access token in the Bot Framework token service.

```ts
app.message('/signout', async ({ send, signout, isSignedIn }) => {
  if (!isSignedIn) return;
  await signout(); // call signout for your auth connection...
  await send('you have been signed out!');
});
```