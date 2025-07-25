---
title: Link unfurling (preview) (C#)
description: Learn how to implement link unfurling in Teams applications using the
  Microsoft Teams AI Library for C#.
ms.topic: how-to
ms.date: 07/16/2025
---
# Link unfurling (preview) (C#)

[This article is prerelease documentation and is subject to change.]

Link unfurling lets your app respond when users paste URLs into Teams. When a URL from your registered domain is pasted, your app receives the URL and can return a card with additional information or actions. This works like a search command where the URL acts as the search term.

> [!note]
> Users can use link unfurling even before they discover or install your app in Teams. This is called [Zero install link unfurling](/microsoftteams/platform/messaging-extensions/how-to/link-unfurling?tabs=desktop%2Cjson%2Cadvantages#zero-install-for-link-unfurling). In this scenario, your app will receive a `message.ext.anon-query-link` activity instead of the usual `message.ext.query-link`.

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

```mermaid
flowchart TD
    A1["User pastes a URL (e.g., www\.test\.com) in Teams compose box"]
    B1([Microsoft Teams])
    C1["Your App"]
    D1["Adaptive Card Preview"]

    A1 --> B1
    B1 -->|Sends URL paste notification| C1
    C1 -->|Returns card and preview| B1
    B1 --> D1

    %% Styling for readability and compatibility
    style B1 fill:#2E86AB,stroke:#1B4F72,stroke-width:2px,color:#ffffff
    style C1 fill:#28B463,stroke:#1D8348,stroke-width:2px,color:#ffffff
    style D1 fill:#F39C12,stroke:#D68910,stroke-width:2px,color:#ffffff
```

## Handle link unfurling

Handle link unfurling when a URL from your registered domain is submited into the Teams compose box.

```ts
app.on('message.ext.query-link', async ({ activity }) => {
  const { url } = activity.value;

  if (!url) {
    return { status: 400 };
  }

  const { card, thumbnail } = createLinkUnfurlCard(url);
  const attachment = {
    ...cardAttachment('adaptive', card), // expanded card in the compose box...
    preview: cardAttachment('thumbnail', thumbnail), //preview card in the compose box...
  };

  return {
    composeExtension: {
      type: 'result',
      attachmentLayout: 'list',
      attachments: [attachment],
    },
  };
});
```

`createLinkUnfurlCard()` function

```ts
export function createLinkUnfurlCard(url: string) {
  const thumbnail = {
    title: 'Unfurled Link',
    text: url,
    images: [
      {
        url: IMAGE_URL,
      },
    ],
  } as ThumbnailCard;

  const card = new AdaptiveCard(
    new TextBlock('Unfurled Link', {
      size: 'Large',
      weight: 'Bolder',
      color: 'Accent',
      style: 'heading',
    }),
    new TextBlock(url, {
      size: 'Small',
      weight: 'Lighter',
      color: 'Good',
    })
  );

  return {
    card,
    thumbnail,
  };
}
```

The link unfurling response includes both a full adaptive card and a preview card. The preview card appears in the compose box when a user pastes a URL:

:::image type="content" source="~/assets/screenshots/link-unfurl-preview.png" alt-text="Link unfurl preview card":::

The user can expand the preview card by clicking on the _expand_ button on the top right.

:::image type="content" source="~/assets/screenshots/link-unfurl-card.png" alt-text="Link unfurl card in conversation":::

The user can then choose to send entire the preview or the full adaptive card as a message.

## Resources

- [Link unfurling](/microsoftteams/platform/messaging-extensions/how-to/link-unfurling?tabs=desktop%2Cjson%2Cadvantages)