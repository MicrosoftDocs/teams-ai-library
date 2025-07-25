---
title: AI (preview) (TypeScript)
description: Overview of AI capabilities and features in the Microsoft Teams AI Library for TypeScript.
ms.topic: overview
ms.date: 07/16/2025
---

# AI (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

The AI packages in this library are designed to make it easier to build applications with LLMs.
The `@microsoft/teams.ai` package has two main components:

## 📦 Prompts

A `Prompt` is the component that orchestrates everything, it handles state management,
function definitions, and invokes the model/template when needed. This layer abstracts many of
the complexities of the Models to provide a common interface.

## 🧠 Models

A `Model` is the component that interfaces with the LLM, being given some `input` and returning the `output`.
This layer deals with any of the nuances of the particular Models being used.

It is in the model implementation that the individual LLM features (i.e. streaming/tools etc.)
are made compatible with the more general features of the `@microsoft/teams.ai` package.

> [!NOTE]
> You are not restricted to use the `@microsoft/teams.ai` package to build your Teams Agent applications. You can use models directly if you choose. These packages are there to simplify the interactions with the models and Teams.