# At-mentions


Sending a message at `@mentions` a user is as simple as:

```
    app.on('message', async ({ send, activity }) > {
        await send(MessageSendActivity('hi!').mention(activity.from));
    });
```