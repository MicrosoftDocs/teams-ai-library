---
title: Signing Out (preview) (C#)
description: Learn about Signing Out (preview) (C#)
ms.topic: how-to
ms.date: 07/16/2025
---

# Signing Out (preview) (C#)

[This article is prerelease documentation and is subject to change.]

Sign a user out by calling the `signout` method to discard the cached access token in the Bot Framework token service.

```ts
app.message('/signout', async ({ send, signout, isSignedIn }) => {
  if (!isSignedIn) return;
  await signout(); // call signout for your auth connection...
  await send('you have been signed out!');
});
```