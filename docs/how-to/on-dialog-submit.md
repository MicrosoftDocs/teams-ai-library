---
title: Dialog Submit
description: Dialog Submit
ms.topic: how-to
ms.date: 05/15/2025
---

# Dialog Submit


You can listen on the `dialog.submit` activity and respond with adaptive cards or url to be rendered as the dialogs content.

## `dialog.submit` (task/submit)

triggered when a dialog is submitted, used to handle logic before closing the dialog.

Example: when a dialog is submitted, do some custom logic and do not render anything else.

```
    app.on('dialog.submit', ({}) > {
        // ... some logic
        return { status: 200 };
    });
```