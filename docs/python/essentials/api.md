---
title: Teams API Client
description: Learn about Teams API Client
ms.topic: how-to
ms.date: 09/18/2025
---

# Teams API Client

Teams has a number of areas that your application has access to via its API. These are all available via the `app.api` object. Here is a short summary of the different areas:

| Area | Description |
|------|-------------|
| `conversations` | Gives your application the ability to perform activities on conversations (send, update, delete messages, etc.), or create conversations (like 1:1 chat with a user) |
| `meetings` | Gives your application access to meeting details |
| `teams` | Gives your application access to team or channel details |


An instance of the API client is passed to handlers that can be used to fetch details:

## Example

In this example, we use the API client to fetch the members in a conversation. The `Api` object is passed to the activity handler in this case.

```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    const members = await ctx.api.conversations.members.get(ctx.activity.conversation.id)
```
