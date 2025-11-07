---
title: Turn Context (TypeScript)
description: Understand how Teams SDK's IActivityContext replaces BotBuilder's TurnContext for handling incoming data and APIs in Teams TypeScript apps.
ms.topic: overview
ms.date: 09/18/2025
---

# Turn Context (TypeScript)

While BotBuilder has a `TurnContext`, Teams SDK has `IActivityContext` which serves the same purpose.
The context is passed into activity handlers and provides a structured way for developers to interface
with apis and incoming data.
