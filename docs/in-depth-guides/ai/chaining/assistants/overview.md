---
title: Assistants
description: Learn about the Assistants.
ms.topic: overview
ms.date: 05/02/2025
---

# Assistants (preview)

[This article is prerelease documentation and is subject to change.]

Lets create a prompt with a complex directive
that we can split into sub prompts.

We are going to make a developer assistant, someone who
specializes in Typescript, can search internal documentation,
and can read/write files in the project source code.

```bash
src
├── prompts
│   ├── project.ts
│   ├── documentation.ts
│   └── typescript.ts
└── developer.ts
```