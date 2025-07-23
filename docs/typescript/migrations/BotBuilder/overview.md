---
title: From BotBuilder (preview) (TypeScript)
description: Learn about From BotBuilder (preview) (TypeScript)
ms.topic: overview
ms.date: 07/16/2025
---

# From BotBuilder (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

This new iteration of Teams AI has been rebuilt from the ground up. To easy the migration process
we have created a plugin `@microsoft/teams.botbuilder`, which allows you to use a botbuilder `activity handler`
and `adapter` to send/receive activities through our new abstractions.

## Why A Plugin?

Because by using a plugin we are able to leverage all our new features while allowing developers to easily and incrementally
migration activity handlers from the legacy activity handlers to our new `App` class handlers.