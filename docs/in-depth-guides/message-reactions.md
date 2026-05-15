---
title: Message Reactions
description: Guide to adding, removing, and receiving message reactions in Teams agents, including available reaction types, skin tones, rate limits, and best practices.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 05/15/2026
---

# Message Reactions

:::image type="content" source="~/assets/screenshots/reaction-emoji.png" alt-text="Reaction emoji sent by bot" lightbox="~/assets/screenshots/reaction-emoji.png":::

Message reactions allow your agent to add or remove emoji reactions on messages in a Teams conversation, and to react to reactions added by users. This gives your agent a quick, low-friction way to acknowledge messages or signal status without sending a full text reply.

## Adding a Reaction

To add a reaction to a message, use the reactions client through the API client:


::: zone pivot="csharp"
```csharp
app.OnMessage(async (context, cancellationToken) =>
{
    await context.Send("Hello! I'll react to your message.", cancellationToken);

    // Add a reaction to the incoming message
    await context.Api.Conversations.Reactions.AddAsync(
        context.Activity.Conversation.Id,
        context.Activity.Id,
        ReactionType.Like,
        cancellationToken: cancellationToken
    );
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    await ctx.send("Hello! I'll react to your message.")

    # Add a reaction to the incoming message
    await ctx.api.reactions.add(
        ctx.activity.conversation.id,
        ctx.activity.id,
        'like'
    )
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ activity, api, send }) => {
  await send("Hello! I'll react to your message.");

  // Add a reaction to the incoming message
  await api.reactions.add(activity.conversation.id, activity.id, 'like');
});
```
::: zone-end


## Removing a Reaction

You can also remove reactions that your agent has previously added:


::: zone pivot="csharp"
```csharp
app.OnMessage(async (context, cancellationToken) =>
{
    // First, add a reaction
    await context.Api.Conversations.Reactions.AddAsync(
        context.Activity.Conversation.Id,
        context.Activity.Id,
        ReactionType.Heart,
        cancellationToken: cancellationToken
    );

    // Wait a bit, then remove it
    await Task.Delay(2000, cancellationToken);
    await context.Api.Conversations.Reactions.DeleteAsync(
        context.Activity.Conversation.Id,
        context.Activity.Id,
        ReactionType.Heart,
        cancellationToken: cancellationToken
    );
});
```
::: zone-end

::: zone pivot="python"
```python
import asyncio

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    # First, add a reaction
    await ctx.api.reactions.add(
        ctx.activity.conversation.id,
        ctx.activity.id,
        'heart'
    )

    # Wait a bit, then remove it
    await asyncio.sleep(2)
    await ctx.api.reactions.delete(
        ctx.activity.conversation.id,
        ctx.activity.id,
        'heart'
    )
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ activity, api }) => {
  // First, add a reaction
  await api.reactions.add(activity.conversation.id, activity.id, 'heart');

  // Wait a bit, then remove it
  await new Promise((resolve) => setTimeout(resolve, 2000));
  await api.reactions.delete(activity.conversation.id, activity.id, 'heart');
});
```
::: zone-end


## Receiving Reactions

::: zone pivot="csharp"
Your agent can also listen for reactions that users add or remove on messages in conversations it participates in. The activity carries `ReactionsAdded` and `ReactionsRemoved` collections.
::: zone-end

::: zone pivot="python"
Your agent can also listen for reactions that users add or remove on messages in conversations it participates in. The activity carries `reactions_added` and `reactions_removed` lists.
::: zone-end

::: zone pivot="typescript"
Your agent can also listen for reactions that users add or remove on messages in conversations it participates in. The activity carries `reactionsAdded` and `reactionsRemoved` arrays.
::: zone-end


::: zone pivot="csharp"
.NET exposes a single `OnMessageReaction` handler plus dedicated `OnMessageReactionAdded` / `OnMessageReactionRemoved` sub-handlers.

```csharp
app.OnMessageReactionAdded(async (context, cancellationToken) =>
{
    foreach (var reaction in context.Activity.ReactionsAdded ?? [])
    {
        Console.WriteLine($"User added reaction: {reaction.Type}");
    }
});

app.OnMessageReactionRemoved(async (context, cancellationToken) =>
{
    foreach (var reaction in context.Activity.ReactionsRemoved ?? [])
    {
        Console.WriteLine($"User removed reaction: {reaction.Type}");
    }
});
```

If you only need a single handler that runs for both adds and removes, use `app.OnMessageReaction` instead.
::: zone-end

::: zone pivot="python"
```python
@app.on_message_reaction
async def handle_reaction(ctx: ActivityContext[MessageReactionActivity]):
    for reaction in ctx.activity.reactions_added or []:
        print(f"User added reaction: {reaction.type}")

    for reaction in ctx.activity.reactions_removed or []:
        print(f"User removed reaction: {reaction.type}")
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('messageReaction', async ({ activity }) => {
  for (const reaction of activity.reactionsAdded ?? []) {
    console.log(`User added reaction: ${reaction.type}`);
  }

  for (const reaction of activity.reactionsRemoved ?? []) {
    console.log(`User removed reaction: ${reaction.type}`);
  }
});
```
::: zone-end


## Available Reaction Types

::: zone pivot="csharp"
The SDK ships a small set of named reaction constants for the most common reactions, exposed via the `ReactionType` class.
::: zone-end

::: zone pivot="python,typescript"
The SDK ships a small set of named reaction constants for the most common reactions.
::: zone-end

<!-- TODO: restore with correct URL once Learn reactions reference is published (see msteams-docs PR #13991)
Any string-valued reaction ID is accepted, so you can pass any reaction ID from the [Teams reactions reference](#TODO-learn-reactions-reference).
-->


::: zone pivot="csharp"
- `ReactionType.Like` —
- `ReactionType.Heart` —
- `ReactionType.Eyes` —
- `ReactionType.CheckMark` —
- `ReactionType.Launch` —
- `ReactionType.Pushpin` —
::: zone-end

::: zone pivot="python,typescript"
- `'like'` —
- `'heart'` —
- `'1f440_eyes'` —
- `'2705_whiteheavycheckmark'` —
- `'launch'` —
- `'1f4cc_pushpin'` —
::: zone-end


## Skin Tones

Reactions tagged **Diverse** in the Teams reactions reference support five skin-tone variants. Append `-tone1` through `-tone5` to the reaction ID to select a variant:

```text
1f44b_wavinghand-tone4
```

<!-- TODO: restore once Learn reactions reference is published (see msteams-docs PR #13991)
See the [Teams reactions reference](#TODO-learn-reactions-reference) for the full list of reactions that support skin tones.
-->

## Rate Limits

Agents are limited to **two reactions per second**. Calls that exceed this limit are throttled and return a `429` response. Implement exponential backoff and honor the `Retry-After` header.

## Best Practices

- **Use reactions sparingly.** Reactions work best when they signal something specific (acknowledgement, completion, an error). Reacting to every message creates noise.
- **Match the reaction to the context.** Different reactions carry different meanings. Choose one that aligns with your agent's purpose.
- **Replace, don't stack.** If your agent has already added a reaction and needs to update it, remove the existing reaction first, then add the new one. Adding a reaction that's already present is a no-op.
- **Handle errors.** Reaction operations can fail if the message no longer exists or the agent isn't a member of the conversation. Handle exceptions appropriately.

## Differences from Feedback

Message reactions are different from the [feedback](./feedback.md) feature:

- **Reactions** are quick emoji responses your agent adds to or removes from messages programmatically, and reactions users add to messages your agent can listen for.
- **Feedback** are interactive UI components (like/dislike buttons) that users can click to provide structured feedback on agent responses.

Use reactions when your agent wants to acknowledge or respond to a message with emoji. Use feedback when you want to collect user opinions about your agent's responses.
