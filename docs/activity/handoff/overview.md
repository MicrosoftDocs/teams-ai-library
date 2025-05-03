---
title: Handoff Activity
ms.topic: overview
description: Learn how to use the handoff activity to initiate or indicate a handoff between bot elements.
ms.date: 05/02/2025
---

# Activity: Handoff (preview)

[This article is prerelease documentation and is subject to change.]

Handoff activities are used to request or signal a change in focus between elements inside a bot. They are not intended to be used in wire communication (besides internal communication that occurs between services in a distributed bot).

```typescript
app.on('handoff', async ({ activity }) => {});
```

## Schema

Handoff activities are identified by a `type` value of `handoff`.

`A6200`: Channels SHOULD drop handoff activities if they are not supported.