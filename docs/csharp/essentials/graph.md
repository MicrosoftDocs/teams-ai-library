---
title: Graph API Client (preview) (C#)
description: Work with Graph APIs in your Teams application using the Teams AI Library for C#.
ms.topic: how-to
ms.date: 07/16/2025
---
# Graph API Client (preview) (C#)

[This article is prerelease documentation and is subject to change.]

[Microsoft Graph](/graph/overview) gives you access to the wider Microsoft 365 ecosystem. You can enrich your application with data from across Microsoft 365.

The library gives your application easy access to the Microsoft Graph API via the `Microsoft.Graph` package.

Microsoft Graph can be accessed by your application using its own application token, or by using the user's token. If you need access to resources that your application may not have, but your user does, you will need to use the user's scoped graph client. To grant explicit consent for your application to access resources on behalf of a user, follow the [auth guide](../in-depth-guides/user-authentication/overview.md).

To access the graph using the Graph using the app, you may use the `app.Graph` object. 

```csharp
// Equivalent of /graph/api/user-get
// Gets the details of the bot-user
var user = app.Graph.Me.GetAsync().GetAwaiter().GetResult();
Console.WriteLine($"User ID: {user.id}");
Console.WriteLine($"User Display Name: {user.displayName}");
Console.WriteLine($"User Email: {user.mail}");
Console.WriteLine($"User Job Title: {user.jobTitle}");
```

To access the graph using the user's token, you need to do this as part of a message handler:


# [Controller](#tab/controller)
```csharp 
    [Message]
    public async Task OnMessage([Context] MessageActivity activity, [Context] GraphClient userGraph)
    {
        var user = await userGraph.Me.GetAsync();
        Console.WriteLine($"User ID: {user.id}");
        Console.WriteLine($"User Display Name: {user.displayName}");
        Console.WriteLine($"User Email: {user.mail}");
        Console.WriteLine($"User Job Title: {user.jobTitle}");
    }
```
# [Minimal](#tab/minimal)
```csharp 
    app.OnMessage(async context =>
    {
        var user = await context.UserGraph.Me.GetAsync();
        Console.WriteLine($"User ID: {user.id}");
        Console.WriteLine($"User Display Name: {user.displayName}");
        Console.WriteLine($"User Email: {user.mail}");
        Console.WriteLine($"User Job Title: {user.jobTitle}");
    });
```
---


Here, the `userGraph` object is a scoped graph client for the user that sent the message.

> [!TIP]
> You also have access to the `appGraph` object in the activity handler. This is equivalent to `app.Graph`.