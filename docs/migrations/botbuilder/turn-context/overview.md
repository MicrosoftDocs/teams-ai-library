---
title: Turn Context
description: Understand how Teams SDK's IActivityContext replaces BotBuilder's TurnContext for handling incoming data and APIs.
ms.topic: overview
zone_pivot_groups: dev-lang
ms.date: 11/17/2025
---

# Turn Context


::: zone pivot="csharp"
This page isn't available for C#.
::: zone-end

::: zone pivot="python"
This page isn't available for Python.
::: zone-end

::: zone pivot="typescript"
While BotBuilder has a `TurnContext`, Teams SDK has `IActivityContext` which serves the same purpose.
The context is passed into activity handlers and provides a structured way for developers to interface
with apis and incoming data.
::: zone-end
