---
title: Assistants
description: Assistants
ms.topic: how-to
ms.date: 05/15/2025
---

# Assistants


Lets create a prompt with a complex directive that we can split into sub prompts.

We are going to make a developer assistant, someone who specializes in Typescript, can search internal documentation, and can read/write files in the project source code.

```
    src
    ├── prompts
    │   ├── project.ts
    │   ├── documentation.ts
    │   └── typescript.ts
    └── developer.ts
```

## Developer

The top level assistant that is responsible for orchestrating the other assistants.

```
    src
    ├── prompts
    │   ├── project.ts
    │   ├── documentation.ts
    │   └── typescript.ts
    └── developer.ts
    

```
### `/src/developer.ts`

```
    import { ChatPrompt, ObjectSchema } from '@microsoft/teams.ai';
    import { OpenAIChatModel } from '@microsoft/teams.openai';
    
    import { project } from './prompts/project';
    import { documentation } from './prompts/documentation';
    import { typescript } from './prompts/typescript';
    
    const schema: ObjectSchema  {
        type: 'object',
        properties: {
            text: {
                type: 'string',
                description: 'what you want to ask or say to the assistant',
            },
        },
        required: ['text'],
    };
    
    const developer  new ChatPrompt({
        instructions: [
            'you are an expert Typescript developer.',
            'you help other developers perform various development tasks including:',
            '- searching documentation',
            '- writing/reading/building the project source code',
            '- searching/resolving typescript related errors.',
        ].join('\n'),
        model: new OpenAIChatModel({
            model: 'gpt-4o',
            apiKey: process.OPENAI_API_KEY,
            stream: true,
        }),
    })
        .function(
            'project-assistant',
            'ask the project assistant to read or write a file/directory from the source code, or run a build',
            schema,
            async ({ text }: { text: string }) > {
                return project.chat(text);
            }
        )
        .function(
            'documentation-assistant',
            'ask the documentation assistant to search for how to use internal packages',
            schema,
            async ({ text }: { text: string }) > {
                return documentation.chat(text);
            }
        )
        .function(
            'typescript-assistant',
            'ask the typescript assistant search the web for typescript errors and offer possible solutions',
            schema,
            async ({ text }: { text: string }) > {
                return typescript.chat(text);
            }
        );
    
    (async () > {
        await developer.chat('run a build and fix any errors', (chunk) > {
            process.stdout.write(chunk);
        });
    
        process.stdout.write('\n');
    })();
```

## Project

The assistant that specializes in project operations like reading/writing a file/directory or running a build.

```
    src
    ├── prompts
    │   ├── project.ts
    │   ├── documentation.ts
    │   └── typescript.ts
    └── developer.ts
    

```
### `/src/prompts/project.ts`

```
    import { ChatPrompt } from '@microsoft/teams.ai';
    import { OpenAIChatModel } from '@microsoft/teams.openai';
    
    export const project  new ChatPrompt({
        instructions: [
            'you are an expert Typescript project manager.',
            'you help other developers perform various development tasks including:',
            '- reading source files/directories',
            '- writing source files/directories',
            '- running builds',
        ].join('\n'),
        model: new OpenAIChatModel({
            model: 'gpt-4o',
            apiKey: process.OPENAI_API_KEY,
        }),
    })
        .function(
            'read-file',
            'read a source file',
            {
                type: 'object',
                properties: {
                    path: {
                        type: 'string',
                        description: 'the path to the file',
                    },
                },
                required: ['path'],
            },
            async ({ path }: { path: string }) > {
                // read the file and return the string content
            }
        )
        .function(
            'read-directory',
            'read the contents of a directory',
            {
                type: 'object',
                properties: {
                    path: {
                        type: 'string',
                        description: 'the path to the directory',
                    },
                },
                required: ['path'],
            },
            async ({ path }: { path: string }) > {
                // read the directory and return the list of files
            }
        )
        .function(
            'write-file',
            'write to a source file',
            {
                type: 'object',
                properties: {
                    path: {
                        type: 'string',
                        description: 'the path to the file',
                    },
                    content: {
                        type: 'string',
                        description: 'the content to write',
                    },
                },
                required: ['path', 'content'],
            },
            async ({ text, content }: { text: string; content: string }) > {
                // write to the file recursively
            }
        )
        .function('build', 'run a project build', async () > {
            // run build
        });
```

## Documentation

The assistant that specializes in documentation searching.

```
    src
    ├── prompts
    │   ├── project.ts
    │   ├── documentation.ts
    │   └── typescript.ts
    └── developer.ts
    

```
### `/src/prompts/documentation.ts`

```
    import { ChatPrompt } from '@microsoft/teams.ai';
    import { OpenAIChatModel } from '@microsoft/teams.openai';
    
    export const documentation  new ChatPrompt({
        instructions: [
            'you are an expert at searching documentation.',
            'you help other developers perform various searches to understand how to use internal packages.',
        ].join('\n'),
        model: new OpenAIChatModel({
            model: 'gpt-4o',
            apiKey: process.OPENAI_API_KEY,
        }),
    }).function(
        'search',
        'search the documentation for relevant information',
        {
            type: 'object',
            properties: {
                text: {
                    type: 'string',
                    description: 'the text to search',
                },
            },
            required: ['text'],
        },
        async ({ text }: { text: string }) > {
            // vector search and return nearest neighbors
        }
    );
```

## TypeScript

The assistant that specializes in Typescript syntax/error knowledge.

```
    src
    ├── prompts
    │   ├── project.ts
    │   ├── documentation.ts
    │   └── typescript.ts
    └── developer.ts
    

```
## `/src/prompts/typescript.ts`

```
    import { ChatPrompt } from '@microsoft/teams.ai';
    import { OpenAIChatModel } from '@microsoft/teams.openai';
    
    export const typescript  new ChatPrompt({
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