---
title: Message Extensions (preview) (C#)
description: Learn about Message Extensions (preview) (C#)
ms.topic: overview
ms.date: 07/16/2025
---

# Message Extensions (preview) (C#)

[This article is prerelease documentation and is subject to change.]

Message extensions (or Compose Extensions) allow your application to hook into messages that users can send or perform actions on messages that users have already sent. They enhance user productivity by providing quick access to information and actions directly within the Teams interface. Users can search or initiate actions from the compose message area, the command box, or directly from a message, with the results returned as richly formatted cards that make information more accessible and actionable.

There are two types of message extensions: [API-based](/microsoftteams/platform/messaging-extensions/api-based-overview) and [Bot-based](/microsoftteams/platform/messaging-extensions/build-bot-based-message-extension?tabs=search-commands). API-based message extensions use an OpenAPI specification that Teams directly queries, requiring no additional application to build or maintain, but offering less customization. Bot-based message extensions require building an application to handle queries, providing more flexibility and customization options. This library supports bot-based message extensions only.

## Resources

- [What are message extensions?](/microsoftteams/platform/messaging-extensions/what-are-messaging-extensions?tabs=desktop)