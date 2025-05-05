---
title: File Consent Invoke Activity
ms.topic: reference
description: Learn about executing the Action Invoke activity.
ms.date: 05/02/2025
---

# Activity: File Consent Invoke (preview)

[This article is prerelease documentation and is subject to change.]

```typescript
app.on('file.consent', async ({ activity }) => {});

app.on('file.consent.accept', async ({ activity }) => {});

app.on('file.consent.decline', async ({ activity }) => {});
```