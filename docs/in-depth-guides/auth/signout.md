---
title: Signout (preview)
description: Learn about Signout (preview)
ms.topic: how-to
ms.date: 05/05/2025
---

# Signout (preview)

[This article is prerelease documentation and is subject to change.]

Sign a user out by calling the `signout` method to discard the cached access token in the Bot Framework token service.

<!-- langtabs-start -->
```typescript
app.message('/signout', async ({ send, signout, isSignedIn }) => {
  if (!isSignedIn) return;
  await signout(); // call signout for your auth connection...
  await send('you have been signed out!');
});
```
<!-- langtabs-end -->