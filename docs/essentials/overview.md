---
title: Essentials
description: Introduction to the core concepts of Teams SDK applications including events, activities, handlers, and the reactive paradigm for building intelligent agents.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---

# Essentials


At its core, an application that hosts an agent on Microsoft Teams exists to do three things well: listen to **activities**, handle the ones that matter, and respond efficiently. Whether a user sends a message, opens a dialog, or clicks a button — your app is there to interpret the activity and act on it.

With Teams SDK, we've made it easier than ever to build this kind of reactive, conversational logic. The SDK gives you simple, strongly-typed handlers to connect to Teams, react to activities, and build intelligent agent behaviors quickly.


At its core, an application that hosts an agent on Microsoft Teams exists to do three things well: listen to events, handle the ones that matter, and respond efficiently. Whether a user sends a message, opens a dialog, or clicks a button — your app is there to interpret the event and act on it.

With Teams SDK, we've made it easier than ever to build this kind of reactive, conversational logic. The SDK introduces a few simple but powerful paradigms to help you connect to Teams, register handlers, and build intelligent agent behaviors quickly.

Before diving in, let's define a few key terms:


::: zone pivot="csharp"
- Activity: The Teams-specific payload that flows between the user and your app. Activities include things like messages, reactions, adaptive card actions, and installs.
- InvokeActivity: A specific kind of activity triggered by user interaction (like submitting a form), which may or may not require a response.
- Handler: The logic in your application that reacts to an activity. You register handlers (`OnMessage`, `OnMessageReaction`, `OnEvent`, …) that decide what to do, when, and how to respond.
::: zone-end

::: zone pivot="python,typescript"
- Event: Anything interesting that happens on Teams — or within your application as a result of handling an earlier event.
- Activity: A special type of Teams-specific event. Activities include things like messages, reactions, and adaptive card actions.
- InvokeActivity: A specific kind of activity triggered by user interaction (like submitting a form), which may or may not require a response.
- Handler: The logic in your application that reacts to events or activities. Handlers decide what to do, when, and how to respond.
::: zone-end



In the **2.1**, your app is a standard ASP.NET Core application. Incoming activities from Teams arrive at your app's endpoint, pass through any **turn middleware** you register, and are routed to the dedicated **activity handler** (`OnMessage`, `OnEvent`, `OnMembersAdded`, …) that matches.

:::image type="content" source="~/assets/diagrams/essentials-overview-1.png" alt-text="Flowchart showing Teams activities, sign-in events, and other incoming events reaching an ASP.NET Core app server, then passing through turn middleware and the activity router to activity handlers for message, card, installation, and other activities." lightbox="~/assets/diagrams/essentials-overview-1.png" :::

> [!NOTE]
> SDK 2.0 (Legacy). SDK 2.0 routed both incoming and outgoing events through a **plugin event bus** before they reached your handlers. The 2.1 removes plugins in favor of standard ASP.NET Core **middleware** and **dependency injection**.


::: zone pivot="csharp"
:::image type="content" source="~/assets/diagrams/essentials-overview-2.png" alt-text="Flowchart showing Teams activities, sign-in events, and other incoming events reaching the app server, which sends activity events to the activity router and incoming and outgoing events to activity handling middleware, with the router dispatching to activity handlers such as OnMessage." lightbox="~/assets/diagrams/essentials-overview-2.png" :::
::: zone-end

::: zone pivot="python"
:::image type="content" source="~/assets/diagrams/essentials-overview-3.png" alt-text="Flowchart showing Teams activities, sign-in events, and other incoming events reaching the app server, which sends activity events to the activity router and incoming and outgoing events to an event handler decorator, with the router dispatching to activity handler decorators." lightbox="~/assets/diagrams/essentials-overview-3.png" :::
::: zone-end

::: zone pivot="typescript"
:::image type="content" source="~/assets/diagrams/essentials-overview-4.png" alt-text="Flowchart showing Teams activities, sign-in events, and other incoming events reaching the app server, which sends activity events to the activity router and incoming and outgoing events to an app.event() handler, with the router dispatching to app.on() activity handlers." lightbox="~/assets/diagrams/essentials-overview-4.png" :::
::: zone-end


This section will walk you through the foundational pieces needed to build responsive, intelligent agents using the SDK.
