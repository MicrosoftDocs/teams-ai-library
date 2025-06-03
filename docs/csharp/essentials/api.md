---
title: Teams API Client (C#)
description: Learn about Teams API Client (C#)
ms.topic: how-to
ms.date: 06/03/2025
---

# Teams API Client (C#)

Teams has a number of areas that your application has access to via its API. These are all available via the `app.Api` object. Here is a short summary of the different areas:

| Area | Description |
|------|-------------|
| `Conversations` | Gives your application the ability to perform activities on conversations (send, update, delete messages, etc.), or create conversations (like 1:1 chat with a user) |
| `Meetings` | Gives your application access to meeting details |
| `Teams` | Gives your application access to team or channel details |


An instance of the Api Client is passed to handlers that can be used to fetch details:

## Example

In this example, we use the api client to fetch the members in a conversation. The `Api` object is passed to the activity handler in this case.


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


## Proactive API

It's also possible to access the api client from outside a handler via the app instance. Here we have the same example as above, but we're access the api client via the app instance.

```csharp
const members = await app.Api.Conversations.Members.Get("...");
```
