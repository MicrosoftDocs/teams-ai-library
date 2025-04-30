# @Mention (preview)

[This article is prerelease documentation and is subject to change.]

Sending a message at `@mentions` a user is as simple as:

```typescript
app.on('message', async ({ send, activity }) => {
  await send(MessageSendActivity('hi!').mention(activity.from));
});
```