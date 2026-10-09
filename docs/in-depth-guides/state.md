---
title: State Management
description: Store and retrieve conversation and user state across activity turns with the Teams SDK.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---

# State Management

> [!NOTE]
> SDK 2.1. Built-in state management is a **Teams SDK 2.1** feature.

::: zone pivot="csharp"
The Teams SDK provides built-in, per-turn state for storing conversation and user data across activities. State is loaded before each activity handler runs, saved automatically after the turn, and exposed through `context.State`.
::: zone-end

::: zone pivot="python,typescript"
The Teams SDK provides built-in, per-turn state for storing conversation and user data across activities. State is loaded before each activity handler runs, saved automatically after the turn, and exposed through `ctx.state`.
::: zone-end

## Setup

::: zone pivot="csharp"
State is disabled by default. Enable it with `UseState()`:
::: zone-end

::: zone pivot="python"
State is disabled by default. Enable it with the `state=True` app option:
::: zone-end

::: zone pivot="typescript"
State is disabled by default. Enable it with the `state: true` app option:
::: zone-end


::: zone pivot="csharp"
```csharp title="Program.cs"
using Microsoft.Teams.Apps;

WebApplicationBuilder builder = WebApplication.CreateSlimBuilder(args);
builder.Services.AddTeamsBotApplication(options =>
{
    options.UseState();
});

WebApplication app = builder.Build();
TeamsBotApplication teams = app.UseTeamsBotApplication();
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.apps import App

app = App(state=True)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';

const app = new App({
  state: true,
});
```
::: zone-end


::: zone pivot="csharp"
Without a dedicated provider, state uses the in-memory `IDistributedCache` implementation. This is useful for local development, but values are lost when the process restarts and aren't shared across instances.
::: zone-end

::: zone pivot="python,typescript"
Without a dedicated provider, state uses the Teams SDK's process-local, in-memory `LocalStorage` implementation. This is useful for local development, but values are lost when the process restarts and aren't shared across instances.
::: zone-end

> [!NOTE]
> ::: zone pivot="csharp"
> Registering an OAuth flow with `AddOAuthFlow()` automatically enables state so pending sign-ins can be associated with the correct flow.
> ::: zone-end
>
> ::: zone pivot="python"
> Registering an OAuth flow with `add_oauth_flow()` automatically enables state so pending sign-ins can be associated with the correct flow. Set `state=False` explicitly to fall back to process-local in-memory maps.
> ::: zone-end
>
> ::: zone pivot="typescript"
> Registering an OAuth flow with `addOAuthFlow()` automatically enables state so pending sign-ins can be associated with the correct flow. Set `state: false` explicitly to fall back to process-local in-memory maps.
> ::: zone-end

## Reading and writing state

::: zone pivot="csharp"
Use `context.State.ConversationState` and `context.State.UserState` in an activity handler. Values must be JSON-serializable.
::: zone-end

::: zone pivot="python,typescript"
Use `ctx.state.conversation` and `ctx.state.user` in an activity handler. Values must be JSON-serializable.
::: zone-end


::: zone pivot="csharp"
```csharp
teams.OnMessage(async (context, cancellationToken) =>
{
    // Write
    context.State.ConversationState.Set("lastMessage", context.Activity.Text ?? string.Empty);
    context.State.UserState.Set("messageCount",
        (context.State.UserState.Get<int>("messageCount")) + 1);

    // Read
    string? last = context.State.ConversationState.Get<string>("lastMessage");
    int count = context.State.UserState.Get<int>("messageCount");

    await context.SendAsync(
        $"Message #{count}. Last message was: {last}",
        cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api import MessageActivity
from microsoft_teams.apps import ActivityContext


@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]) -> None:
    assert ctx.state is not None

    count = ctx.state.conversation.get("message_count", 0) + 1
    ctx.state.conversation["message_count"] = count

    if ctx.state.user is not None and ctx.activity.text.startswith("my name is "):
        ctx.state.user["name"] = ctx.activity.text[len("my name is "):].strip()

    name = ctx.state.user.get("name", "there") if ctx.state.user is not None else "there"
    await ctx.send(f"Hello, {name}. Message #{count}.")
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async (ctx) => {
  if (!ctx.state) {
    throw new Error('Turn state is not enabled.');
  }

  const count = (ctx.state.conversation.get<number>('messageCount') ?? 0) + 1;
  ctx.state.conversation.set('messageCount', count);

  if (ctx.state.user && ctx.activity.text?.startsWith('my name is ')) {
    ctx.state.user.set(
      'name',
      ctx.activity.text.slice('my name is '.length).trim()
    );
  }

  const name = ctx.state.user?.get<string>('name') ?? 'there';
  await ctx.reply(`Hello, ${name}. Message #${count}.`);
});
```
::: zone-end



::: zone pivot="csharp"
Use `ContainsKey()` to check for a value, `Remove()` to remove one, and `Clear()` to remove all values. If you mutate an object or collection returned by `Get<T>(string)`, call `Set()` with the updated value so the scope is marked for persistence.
::: zone-end

::: zone pivot="python"
Use `key in scope` to check for a value, `del scope[key]` to remove one, and `clear()` to remove all values. Changes inside stored lists and dictionaries are detected automatically when the turn is saved.
::: zone-end

::: zone pivot="typescript"
Use `has()` to check for a value, `delete()` to remove one, and `clear()` to remove all values. If you mutate an object or array returned by `get()`, call `set()` with the updated value so the scope is marked for persistence.
::: zone-end


Conversation state is shared by everyone in the current conversation. User state is scoped to the current sender **within that conversation** and is unavailable when an activity has no usable sender ID.

::: zone pivot="csharp"
The SDK writes a scope to storage only when it changes during the current activity. After all handlers for that activity finish, the SDK saves those changes and closes the turn state. Read or update state only while handling the activity. Don't capture it for timers or background tasks because accessing it after the turn ends throws `InvalidOperationException`.
::: zone-end

::: zone pivot="python,typescript"
The SDK writes a scope to storage only when it changes during the current activity. After all handlers for that activity finish, the SDK saves those changes and closes the turn state. Read or update state only while handling the activity. Don't capture it for timers or background tasks because accessing it after the turn ends throws `TurnStateSealedError`.
::: zone-end

## Clearing state

::: zone pivot="csharp"
Remove a value with `Remove()`, or clear a scope with `Clear()`. To remove both scopes from the backing store:
::: zone-end

::: zone pivot="python"
Remove a value with `del scope[key]`, or clear a scope with `clear()`. To remove both scopes from the backing store:
::: zone-end

::: zone pivot="typescript"
Remove a value with `delete()`, or clear a scope with `clear()`. To remove both scopes from the backing store:
::: zone-end


::: zone pivot="csharp"
```csharp
await context.State.DeleteAsync(cancellationToken);
```
::: zone-end

::: zone pivot="python"
```python
await ctx.state.delete()
```
::: zone-end

::: zone pivot="typescript"
```typescript
await ctx.state.delete();
```
::: zone-end


::: zone pivot="csharp"
Values written after `DeleteAsync()` are saved normally at the end of the current turn.
::: zone-end

::: zone pivot="python,typescript"
Values written after `delete()` are saved normally at the end of the current turn.
::: zone-end

## Scaling to distributed state


::: zone pivot="csharp"
For production or multi-instance deployments, register a shared, durable `IDistributedCache` provider, such as Redis, SQL Server, or Azure Cache for Redis, before calling `UseState()`. The state API used by handlers doesn't change:
::: zone-end

::: zone pivot="python"
For production or multi-instance deployments, implement the Teams SDK's `Storage[str, Any]` contract with a shared, durable backend and pass it through `StateOptions`. The state API used by handlers doesn't change:
::: zone-end

::: zone pivot="typescript"
For production or multi-instance deployments, implement the Teams SDK's `IStorage<string, string>` contract with a shared, durable backend and pass it through `state.storage`. The state API used by handlers doesn't change:
::: zone-end



::: zone pivot="csharp"
```csharp title="Program.cs"
using Microsoft.Teams.Apps;
using StackExchange.Redis;

WebApplicationBuilder builder = WebApplication.CreateSlimBuilder(args);

// Register Redis — UseState() picks this up automatically
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration["Redis:ConnectionString"];
});

builder.Services.AddTeamsBotApplication(options =>
{
    options.UseState();
});
```
::: zone-end

::: zone pivot="python"
```python
from typing import Any

from microsoft_teams.apps import App, StateOptions
from microsoft_teams.common import Storage


def create_app(durable_storage: Storage[str, Any]) -> App:
    return App(
        state=StateOptions(
            storage=durable_storage,
            key_prefix="my-app",
        )
    )
```
::: zone-end

::: zone pivot="typescript"
```typescript
import type { IStorage } from '@microsoft/teams.common';
import { App } from '@microsoft/teams.apps';

function createApp(durableStorage: IStorage<string, string>): App {
  return new App({
    state: {
      storage: durableStorage,
      keyPrefix: 'my-app',
    },
  });
}
```
::: zone-end



::: zone pivot="csharp"
The SDK serializes each scope as UTF-8 JSON bytes and replaces the complete scope on save, so concurrent turns use last-writer-wins semantics. Configure cache entry expiration and the key prefix through `UseState()`. Configure any provider-specific options when registering the `IDistributedCache` implementation.
::: zone-end

::: zone pivot="python,typescript"
The SDK serializes each scope as a JSON string and replaces the complete scope on save, so concurrent turns use last-writer-wins semantics. Configure expiry, retries, and other storage-specific behavior on your storage implementation.
::: zone-end

