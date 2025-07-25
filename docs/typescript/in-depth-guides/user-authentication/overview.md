---
title: User Authentication (preview) (TypeScript)
description: Overview of user authentication in the Microsoft Teams AI Library for TypeScript.
ms.topic: overview
ms.date: 07/16/2025
---

# User Authentication (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

<!-- 
Things to potentially add to this section:

- The name of the auth is fixed to `graph` here, but it can easily be changed by supplying a value when building the App.

- Show that for explicit oauth you can configure the oauth card that is sent to the user via the options to the signin function.

- Create mermaid diagrams for how sso and oauth works
--->

At times agents must access secured online resources on behalf of the user, such as checking email, checking on flight status, or placing an order. To enable this, the user must authenticate their identity and grant consent for the application to access these resources. This process results in the application receiving a token, which the application can then use to access the permitted resources on the user's behalf.

## Resources

[User Authentication Basics](/azure/bot-service/bot-builder-concept-authentication)