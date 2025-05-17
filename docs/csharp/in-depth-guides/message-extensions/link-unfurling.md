---
title: Link unfurling (C#)
description: Learn about Link unfurling (C#)
ms.topic: how-to
ms.date: 05/17/2025
---
# Link unfurling (C#)

Link unfurling lets your app respond when users paste URLs into Teams. When a URL from your registered domain is pasted, your app receives the URL and can return a card with additional information or actions. This works like a search command where the URL acts as the search term. Users can use link unfurling without installing your app.

## Setting up your Teams app manifest


```json
"composeExtensions": [
    {
        "botId": "${{BOT_ID}}",
        "messageHandlers": [
            {
                "type": "link",
                "value": {
                    "domains": [
                        "www.test.com"
                    ]
                }
            }
        ]
    }
]
```


When a user pastes a URL from your registered domain (like `www.test.com`) into the Teams compose box, your app will receive a notification. Your app can then respond by returning an adaptive card that displays a preview of the linked content. This preview card appears before the user sends their message in the compose box, allowing them to see how the link will be displayed to others.

![alt-text for link-unfurling-1.png](~/assets/diagrams/link-unfurling-1.png)

## Handle link unfurling

Handle link unfurling when a URL from your registered domain is submited into the Teams compose box.

<FileCodeBlock
    lang="typescript"
    src="/generated-snippets/ts/index.snippet.message-ext-query-link.ts"
/>

`createLinkUnfurlCard()` function

<FileCodeBlock
    lang="typescript"
    src="/generated-snippets/ts/card.snippet.message-ext-create-link-unfurl-card.ts"
/>

The link unfurling response includes both a full adaptive card and a preview card. The preview card appears in the compose box when a user pastes a URL:

![Link unfurl preview card](/screenshots/link-unfurl-preview.png)

The user can expand the preview card by clicking on the _expand_ button on the top right.

![Link unfurl card in conversation](/screenshots/link-unfurl-card.png)

The user can then choose to send entire the preview or the full adaptive card as a message.

## Resources

- [Link unfurling](https://learn.microsoft.com/en-us/microsoftteams/platform/messaging-extensions/how-to/link-unfurling?tabs=desktop%2Cjson%2Cadvantages)
