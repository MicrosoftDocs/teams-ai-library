# 💬 Chat (Text)

The `ChatPrompt` and `ChatModel` support interacting with an LLM via `text <> text` communication. The `ChatPrompt` supports `functions` and `streaming`.

## Simple

A simple prompt for finding the right emojis.

```
    import { ChatPrompt } from '@microsoft/teams.ai';
    import { OpenAIChatModel } from '@microsoft/teams.openai';
    
    const prompt  new ChatPrompt({
        instructions: [
            'you are an assistant that helps find the perfect emoji to use for a given situation.',
            'you will only respond with emojis.',
        ].join('\n'),
        model: new OpenAIChatModel({
            model: 'gpt-4o',
            apiKey: process.OPENAI_API_KEY,
        }),
    });
    
    (async () > {
        const res  await prompt.chat('having a great day!');
        console.log(res); // 😄🌞🎉
    })();
```

## Streaming

Now lets add streaming support...

```
    import { ChatPrompt } from '@microsoft/teams.ai';
    import { OpenAIChatModel } from '@microsoft/teams.openai';
    
    const prompt  new ChatPrompt({
        instructions: [
            'you are an assistant that helps find the perfect emoji to use for a given situation.',
            'you will only respond with emojis.',
        ].join('\n'),
        model: new OpenAIChatModel({
            model: 'gpt-4o',
            apiKey: process.OPENAI_API_KEY,
            stream: true,
        }),
    });
    
    (async () > {
        await prompt.chat('having a great day!', (chunk) > {
            process.stdout.write(chunk); // 😄🌞🎉
        });
    
        process.stdout.write('\n');
    })();
```

## Functions

Now lets add GIF support via function calling...

```
    import { ChatPrompt } from '@microsoft/teams.ai';
    import { OpenAIChatModel } from '@microsoft/teams.openai';
    
    interface GifySearchArgs {
        readonly text: string;
        readonly limit?: number;
    }
    
    const prompt  new ChatPrompt({
        instructions: [
            'you are an assistant that helps find the perfect emoji to use for a given situation.',
            'you will only respond with emojis.',
        ].join('\n'),
        model: new OpenAIChatModel({
            model: 'gpt-4o',
            apiKey: process.OPENAI_API_KEY,
            stream: true,
        }),
    }).function(
        'gify',
        'search for gifs',
        {
            type: 'object',
            properties: {
                text: {
                    type: 'string',
                    description: 'the text to search for',
                },
                limit: {
                    type: 'number',
                    description: 'the maximum number of gifs to return',
                },
            },
            required: ['text'],
        },
        async ({ text, limit }: GifySearchArgs) > {
            const { GiphyFetch }  await import('@giphy/js-fetch-api');
            const giphy  new GiphyFetch(process.env.GIPHY_API_KEY || '');
            const res  await giphy.search(text, { limit, sort: 'relevant' });
            return res.data[0].images.original.url;
        }
    );
    
    (async () > {
        await prompt.chat('having a great day!', (chunk) > {
            process.stdout.write(chunk); // gif and/or 😄🌞🎉...
        });
    
        process.stdout.write('\n');
    })();
```