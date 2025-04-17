---
title: Listening To Dialogs
description: Listening To Dialogs
ms.topic: how-to
ms.date: 05/15/2025
---

# Listening To Dialogs


You can listen on the `dialog.open` activity and respond with adaptive cards or url to be rendered as the dialogs content.

## `dialog.open` (task/fetch)

triggered when a dialog is opened, used to render dialog contents.

Example: when a dialog is opened, render an [Adaptive Card](https://adaptivecards.io/) as the body.

```
    app.on('dialog.open', ({ }) > {
        return {
            status: 200,
            body: {
                task: {
                    type: 'continue',
                    value: {
                        width: 'large',
                        card: cardAttachment('adaptive', {
                            type: 'AdaptiveCard',
                            version: '1.6',
                            body: [...]
                        })
                    }
                }
            }
        };
    });
```