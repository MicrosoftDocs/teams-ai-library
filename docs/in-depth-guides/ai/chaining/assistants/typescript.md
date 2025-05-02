---
title: Typescript (preview)
description: Learn about Typescript (preview)
ms.topic: how-to
ms.date: 04/30/2025
---

# Typescript (preview)

[This article is prerelease documentation and is subject to change.]

The assistant that specializes in Typescript syntax/error knowledge.

```bash
src
├── prompts
│   ├── project.ts
│   ├── documentation.ts
│   └── typescript.ts
└── developer.ts
```

## `/src/prompts/typescript.ts`

```typescript
import { ChatPrompt } from '@microsoft/teams.ai';
import { OpenAIChatModel } from '@microsoft/teams.openai';

export const typescript = new ChatPrompt({
  instructions: [
    'you are an expert Typescript engineer.',
    'you are great at solving Typescript problems, searching for errors, and providing solutions.',
  ].join('\n'),
  model: new OpenAIChatModel({
    model: 'o1-preview', // we use o1 here for its advanced reasoning
    apiKey: process.OPENAI_API_KEY,
  }),
});
```