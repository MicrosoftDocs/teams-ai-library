# Dialog Submit


You can listen on the `dialog.submit` activity and respond with adaptive cards or url to be rendered as the dialogs content.

## ](#dialogsubmit-tasksubmit)[`dialog.submit` (task/submit)

triggered when a dialog is submitted, used to handle logic before closing the dialog.

Example: when a dialog is submitted, do some custom logic and do not render anything else.

```
    app.on('dialog.submit', ({}) > {
        // ... some logic
        return { status: 200 };
    });
```