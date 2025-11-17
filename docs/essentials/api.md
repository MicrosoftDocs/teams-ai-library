---
sidebar_label: API Client
title: API Client
zone_pivot_groups: dev-lang
description: Overview of the Teams API Client and how to use it to interact with conversations, meetings, and teams in your application.
---
# Teams API Client

::: zone pivot="csharp"
Teams has a number of areas that your application has access to via its API. These are all available via the `app.Api` object. Here is a short summary of the different areas:
::: zone-end

::: zone pivot="python,typescript"
Teams has a number of areas that your application has access to via its API. These are all available via the `app.api` object. Here is a short summary of the different areas:
::: zone-end


::: zone pivot="csharp"
| Area            | Description                                                                                                                                                          |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Conversations` | Gives your application the ability to perform activities on conversations (send, update, delete messages, etc.), or create conversations (like 1:1 chat with a user) |
| `Meetings`      | Gives your application access to meeting details                                                                                                                     |
| `Teams`         | Gives your application access to team or channel details                                                                                                             |
::: zone-end

::: zone pivot="python,typescript"
| Area            | Description                                                                                                                                                          |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `conversations` | Gives your application the ability to perform activities on conversations (send, update, delete messages, etc.), or create conversations (like 1:1 chat with a user) |
| `meetings`      | Gives your application access to meeting details                                                                                                                     |
| `teams`         | Gives your application access to team or channel details                                                                                                             |
::: zone-end


An instance of the API client is passed to handlers that can be used to fetch details:

## Example

::: zone pivot="csharp"
In this example, we use the API client to fetch the members in a conversation. The `Api` object is passed to the activity handler in this case.
::: zone-end

::: zone pivot="python,typescript"
In this example, we use the API client to fetch the members in a conversation. The `api` object is passed to the activity handler in this case.
::: zone-end


::: zone pivot="csharp"
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# [Controller](#tab/controller)
```csharp
[Message]
public async Task OnMessage([Context] MessageActivity activity, [Context] ApiClient api)
{
    var members = await api.Conversations.Members.Get(context.Conversation.Id);
}
```

# [Minimal](#tab/minimal)
```csharp
app.OnMessage(async context =>
{
    var members = await context.Api.Conversations.Members.Get(context.Conversation.Id);
});
```

---


::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    members = await ctx.api.conversations.members.get(ctx.activity.conversation.id)
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ activity, api }) => {
  const members = await api.conversations.members(activity.conversation.id).get();
});
```
::: zone-end


## Proactive API

It's also possible to access the API client from outside a handler via the app instance. Here we have the same example as above, but we're access the API client via the app instance.


::: zone pivot="csharp"
```csharp
const members = await app.Api.Conversations.Members.Get("...");
```
::: zone-end

::: zone pivot="python"
```python
members = await app.api.conversations.members.get("...")
```
::: zone-end

::: zone pivot="typescript"
```typescript
import * as endpoints from '@microsoft/teams.graph-endpoints';

const res = await app.api.graph.call(endpoints.chats.getAllMessages.get);
```
::: zone-end
