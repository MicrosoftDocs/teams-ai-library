---
title: Turn Context
sidebar_position: 3
languages: ['typescript']
summary: Understand how Teams SDK's IActivityContext replaces BotBuilder's TurnContext for handling incoming data and APIs.
zone_pivot_groups: dev-lang
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

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

