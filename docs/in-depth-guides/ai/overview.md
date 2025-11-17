---
title: AI
zone_pivot_groups: dev-lang
description: Overview of AI components in Teams SDK, including Prompts for orchestration and Models for LLM interfaces.
---
# AI

::: zone pivot="csharp"
The AI packages in this SDK are designed to make it easier to build applications with LLMs.
The `Microsoft.Teams.AI` has two main components:
::: zone-end

::: zone pivot="python"
The AI packages in this SDK are designed to make it easier to build applications with LLMs.
The `microsoft-teams-ai` package has two main components:
::: zone-end

::: zone pivot="typescript"
The AI packages in this SDK are designed to make it easier to build applications with LLMs.
The `@microsoft/teams.ai` package has two main components:
::: zone-end

## 📦 Prompts

A `Prompt` is the component that orchestrates everything, it handles state management,
function definitions, and invokes the model/template when needed. This layer abstracts many of
the complexities of the Models to provide a common interface.

## 🧠 Models

A `Model` is the component that interfaces with the LLM, being given some `input` and returning the `output`.
This layer deals with any of the nuances of the particular Models being used.

::: zone pivot="csharp"
It is in the model implementation that the individual LLM features (i.e. streaming/tools etc.)
are made compatible with the more general features of the `Microsoft.Teams.AI`.
::: zone-end

::: zone pivot="python"
It is in the model implementation that the individual LLM features (i.e. streaming/tools etc.)
are made compatible with the more general features of the `microsoft-teams-ai` package.
::: zone-end

::: zone pivot="typescript"
It is in the model implementation that the individual LLM features (i.e. streaming/tools etc.)
are made compatible with the more general features of the `@microsoft/teams.ai` package.
::: zone-end

::: zone pivot="csharp"
:::note
You are not restricted to use the `Microsoft.Teams.AI` to build your Teams Agent applications. You can use models directly if you choose. These packages are there to simplify the interactions with the models and Teams.
:::
::: zone-end

::: zone pivot="python"
:::note
You are not restricted to use the `microsoft-teams-ai` package to build your Teams Agent applications. You can use models directly if you choose. These packages are there to simplify the interactions with the models and Teams.
:::
::: zone-end

::: zone pivot="typescript"
:::note
You are not restricted to use the `@microsoft/teams.ai` package to build your Teams Agent applications. You can use models directly if you choose. These packages are there to simplify the interactions with the models and Teams.
:::
::: zone-end
