---
title: From BotBuilder (TypeScript)
description: Migration guide from BotBuilder to Teams SDK for Teams TypeScript apps, including the BotBuilder plugin for compatibility with existing activity handlers and adapters.
ms.topic: overview
ms.date: 09/18/2025
---

# From BotBuilder (TypeScript)

This new iteration of Teams AI has been rebuilt from the ground up. To easy the migration process
we have created a plugin `@microsoft/teams.botbuilder`, which allows you to use a botbuilder `activity handler`
and `adapter` to send/receive activities through our new abstractions.

## Why A Plugin?

Because by using a plugin we are able to leverage all our new features while allowing developers to easily and incrementally
migration activity handlers from the legacy activity handlers to our new `App` class handlers.
