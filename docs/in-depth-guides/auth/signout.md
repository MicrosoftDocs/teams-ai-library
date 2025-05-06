# Signout

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