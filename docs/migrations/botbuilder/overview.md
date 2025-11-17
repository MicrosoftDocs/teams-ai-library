---
sidebar_label: From BotBuilder
title: From BotBuilder
zone_pivot_groups: dev-lang
description: Migration guide from BotBuilder to Teams SDK, including the BotBuilder plugin for compatibility with existing activity handlers and adapters.
---
# From BotBuilder


::: zone pivot="csharp"
This page isn't available for C#.
::: zone-end

::: zone pivot="python"
This page isn't available for Python.
::: zone-end

::: zone pivot="typescript"
This new iteration of Teams SDK has been rebuilt from the ground up. To easy the migration process
we have created a plugin `@microsoft/teams.botbuilder`, which allows you to use a botbuilder `activity handler`
and `adapter` to send/receive activities through our new abstractions.

## Why a Plugin?

Because by using a plugin we are able to leverage all our new features while allowing developers to easily and incrementally
migration activity handlers from the legacy activity handlers to our new `App` class handlers.
::: zone-end

