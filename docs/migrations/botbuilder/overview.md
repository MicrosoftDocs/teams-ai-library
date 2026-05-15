---
title: From BotBuilder
description: Migration guide from BotBuilder to Teams SDK, including the BotBuilder plugin for compatibility with existing activity handlers and adapters.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 05/15/2026
---

# From BotBuilder

::: zone pivot="csharp"
This new iteration of Teams SDK has been rebuilt from the ground up.
To ease the migration process, we've introduced a plugin `Microsoft.Teams.Plugins.AspNetCore.BotBuilder` that
allows you to continue using BotBuilder components like `ActivityHandler` and `CloudAdapter`
to receive, process and send activities within the new Teams SDK abstractions.
::: zone-end

::: zone pivot="python"
This new iteration of Teams SDK has been rebuilt from the ground up.
To ease the migration process, we've introduced a plugin microsoft-teams-botbuilder that
allows you to continue using BotBuilder components like `ActivityHandler` and `CloudAdapter`
to receive, process and send activities within the new Teams SDK abstractions.
::: zone-end

::: zone pivot="typescript"
This new iteration of Teams SDK has been rebuilt from the ground up.
To ease the migration process, we've introduced a plugin `@microsoft/teams.botbuilder` that
allows you to continue using BotBuilder components like `ActivityHandler` and `CloudAdapter`
to receive, process and send activities within the new Teams SDK abstractions.
::: zone-end

## Why a Plugin?

The plugin exists to bridge BotBuilder and the new Teams SDK,
letting developers keep their existing BotBuilder activity handlers while gradually moving to the new Teams SDK App handlers.
It enables incremental migration and smooth adoption of new SDK features.
