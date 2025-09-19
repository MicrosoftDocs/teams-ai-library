---
title: Graph API Client (Python)
description: Learn about Graph API Client (Python)
ms.topic: how-to
ms.date: 09/18/2025
---

# Graph API Client (Python)

[Microsoft Graph](/graph/overview) gives you access to the wider Microsoft 365 ecosystem. You can enrich your application with data from across Microsoft 365.

The library gives your application easy access to the Microsoft Graph API via the `microsoft-teams-graph` package.

Microsoft Graph can be accessed by your application using its own application token, or by using the user's token. If you need access to resources that your application may not have, but your user does, you will need to use the user's scoped graph client. To grant explicit consent for your application to access resources on behalf of a user, follow the [auth guide](../in-depth-guides/user-authentication.md).
