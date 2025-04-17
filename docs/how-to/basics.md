---
title: Basics
description: Basics
ms.topic: how-to
ms.date: 05/15/2025
---

# Basics


All middleware and activity handlers are given a context which can be used to react to system events known as `Activities`.

## Logging

All contexts have access to the apps `Logger` instance.

```
    app.on('activity', async ({ log, activity }) > {
        log.info(activity);
        log.warn(activity);
        log.error(activity);
        log.debug(activity);
    });
```