---
title: Activity - Handoff (preview)
description: Learn about Activity - Handoff (preview)
ms.topic: overview
ms.date: 05/05/2025
---

# Activity: Handoff (preview)

[This article is prerelease documentation and is subject to change.]

Handoff activities are used to request or signal a change in focus between elements inside a bot. They are not intended to be used in wire communication (besides internal communication that occurs between services in a distributed bot).

<!-- langtabs-start -->
```typescript
app.on('handoff', async ({ activity }) => {});
```
<!-- langtabs-end -->

## Schema

Handoff activities are identified by a `type` value of `handoff`.

`A6200`: Channels SHOULD drop handoff activities if they are not supported.