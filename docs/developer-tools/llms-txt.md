---
title: llms.txt
description: Documentation files optimized for AI coding assistants to give them context about the Teams SDK.
ms.topic: how-to
ms.date: 07/27/2026
---


# llms.txt

The Teams SDK publishes [llms.txt](https://llmstxt.org) files, plain-text versions of the documentation optimized for AI coding assistants. Point your tool at the right file and it gets the context it needs to help you build Teams apps.

## Available files

### Root

High-level SDK overview with links to reference guides.

```
https://microsoft.github.io/teams-sdk/llms_docs/llms.txt
```

> [!TIP]
>
> Instead of manually providing URLs, you can install the [`teams-dev` agent skill](./agent-skills.md) which automatically gives your coding assistant the right context.

### Per-language
# [TypeScript](#tab/typescript)
**Small** a navigation index, the assistant fetches individual pages as needed.
```
https://microsoft.github.io/teams-sdk/llms_docs/llms_typescript.txt
```

**Full** a complete documentation in a single file, best for tools with large context windows.
```
https://microsoft.github.io/teams-sdk/llms_docs/llms_typescript_full.txt
```

---

# [Python](#tab/python)
**Small** a navigation index, the assistant fetches individual pages as needed.
```
https://microsoft.github.io/teams-sdk/llms_docs/llms_python.txt
```

**Full** a complete documentation in a single file, best for tools with large context windows.
```
https://microsoft.github.io/teams-sdk/llms_docs/llms_python_full.txt
```

---

# [C#](#tab/csharp)
**Small** a navigation index, the assistant fetches individual pages as needed.
```
https://microsoft.github.io/teams-sdk/llms_docs/llms_csharp.txt
```

**Full** a complete documentation in a single file, best for tools with large context windows.
```
https://microsoft.github.io/teams-sdk/llms_docs/llms_csharp_full.txt
```
