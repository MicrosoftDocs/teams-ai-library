---
sidebar_label: Link Unfurling
title: Link Unfurling
zone_pivot_groups: dev-lang
description: Enable your app to respond when users paste URLs by creating preview cards with additional information and actions.
---
# Link unfurling

Link unfurling lets your app respond when users paste URLs into Teams. When a URL from your registered domain is pasted, your app receives the URL and can return a card with additional information or actions. This works like a search command where the URL acts as the search term.

:::note
Users can use link unfurling even before they discover or install your app in Teams. This is called [Zero install link unfurling](https://learn.microsoft.com/en-us/microsoftteams/platform/messaging-extensions/how-to/link-unfurling?tabs=desktop%2Cjson%2Cadvantages#zero-install-for-link-unfurling). In this scenario, your app will receive a `message.ext.anon-query-link` activity instead of the usual `message.ext.query-link`.
:::

## Setting up your Teams app manifest

### Configure message handlers

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

### How link unfurling works

When a user pastes a URL from your registered domain (like `www.test.com`) into the Teams compose box, your app will receive a notification. Your app can then respond by returning an adaptive card that displays a preview of the linked content. This preview card appears before the user sends their message in the compose box, allowing them to see how the link will be displayed to others.

![alt-text for link-unfurling-1.png](~/assets/diagrams/link-unfurling-1.png)

## Implementing link unfurling

### Handle the query link event

Handle link unfurling when a URL from your registered domain is submitted into the Teams compose box.


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Api.Activities.Invokes.MessageExtensions;
using Microsoft.Teams.Api.MessageExtensions;
using Microsoft.Teams.Apps.Annotations;

//...

[MessageExtension.QueryLink]
public Response OnMessageExtensionQueryLink(
    [Context] QueryLinkActivity activity,
    [Context] IContext.Client client,
    [Context] ILogger log)
{
    log.Info("[MESSAGE_EXT_QUERY_LINK] Link unfurling received");

    var url = activity.Value?.Url;
    log.Info($"[MESSAGE_EXT_QUERY_LINK] URL: {url}");

    if (string.IsNullOrEmpty(url))
    {
        return CreateErrorResponse("No URL provided");
    }

    return CreateLinkUnfurlResponse(url, log);
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.api import (
    AdaptiveCardAttachment,
    MessageExtensionQueryLinkInvokeActivity,
    ThumbnailCardAttachment,
    card_attachment,
    InvokeResponse,
    AttachmentLayout,
    MessagingExtensionAttachment,
    MessagingExtensionInvokeResponse,
    MessagingExtensionResult,
    MessagingExtensionResultType,
)
from microsoft.teams.apps import ActivityContext
# ...

@app.on_message_ext_query_link
async def handle_message_ext_query_link(ctx: ActivityContext[MessageExtensionQueryLinkInvokeActivity]):
    url = ctx.activity.value.url

    if not url:
        return InvokeResponse[MessagingExtensionInvokeResponse](status=400)

    card_data = create_link_unfurl_card(url)
    main_attachment = card_attachment(AdaptiveCardAttachment(content=card_data["card"]))
    preview_attachment = card_attachment(ThumbnailCardAttachment(content=card_data["thumbnail"]))

    attachment = MessagingExtensionAttachment(
        content_type=main_attachment.content_type,
        content=main_attachment.content,
        preview=preview_attachment,
    )

    result = MessagingExtensionResult(
        type=MessagingExtensionResultType.RESULT,
        attachment_layout=AttachmentLayout.LIST,
        attachments=[attachment],
    )

    return MessagingExtensionInvokeResponse(compose_extension=result)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { cardAttachment } from '@microsoft/teams.api';
import { App } from '@microsoft/teams.apps';
import { IAdaptiveCard } from '@microsoft/teams.cards';
// ...

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
::: zone-end


### Create the unfurl card


::: zone pivot="csharp"
`CreateLinkUnfurlResponse()` method

```csharp
using Microsoft.Teams.Api;
using Microsoft.Teams.Api.MessageExtensions;
using Microsoft.Teams.Cards;

//...

private static Response CreateLinkUnfurlResponse(string url, ILogger log)
{
    var card = new AdaptiveCard
    {
        Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
        Body = new List<CardElement>
        {
            new TextBlock("Link Preview")
            {
                Weight = TextWeight.Bolder,
                Size = TextSize.Medium
            },
            new TextBlock($"URL: {url}")
            {
                IsSubtle = true,
                Wrap = true
            },
            new TextBlock("This is a preview of the linked content generated by the message extension.")
            {
                Wrap = true,
                Size = TextSize.Small
            }
        }
    };

    var attachment = new Microsoft.Teams.Api.MessageExtensions.Attachment
    {
        ContentType = new ContentType("application/vnd.microsoft.card.adaptive"),
        Content = card
    };

    return new Response
    {
        ComposeExtension = new Result
        {
            Type = ResultType.Result,
            AttachmentLayout = Layout.List,
            Attachments = new List<Microsoft.Teams.Api.MessageExtensions.Attachment> { attachment }
        }
    };
}

// Helper method to create error responses
private static Response CreateErrorResponse(string message)
{
    return new Response
    {
        ComposeExtension = new Result
        {
            Type = ResultType.Message,
            Text = message
        }
    };
}
```
::: zone-end

::: zone pivot="python"
`create_link_unfurl_card()` function

```python
from typing import Any, Dict
from microsoft.teams.cards import AdaptiveCard
# ...

def create_link_unfurl_card(url: str) -> Dict[str, Any]:
    """Create a card for link unfurling."""
    thumbnail = {
        "title": "Unfurled Link",
        "text": url,
        "images": [{"url": IMAGE_URL}],
    }

    card = AdaptiveCard.model_validate(
        {
            "type": "AdaptiveCard",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Unfurled Link",
                    "size": "Large",
                    "weight": "Bolder",
                    "color": "Accent",
                    "style": "heading",
                },
                {
                    "type": "TextBlock",
                    "text": url,
                    "size": "Small",
                    "weight": "Lighter",
                    "color": "Good",
                },
            ],
        }
    )

    return {"card": card, "thumbnail": thumbnail}
```
::: zone-end

::: zone pivot="typescript"
`createLinkUnfurlCard()` function

```typescript
import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';
import { ThumbnailCard } from '@microsoft/teams.api';
// ...

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
::: zone-end


### User experience flow

The link unfurling response includes both a full adaptive card and a preview card. The preview card appears in the compose box when a user pastes a URL:

![Screenshot showing a preview card for an unfurled URL in the Teams compose box.](/screenshots/link-unfurl-preview.png)

The user can expand the preview card by clicking on the _expand_ button on the top right.

![Screenshot of Teams compose box with an outline around the unfurled link card labeled 'Adaptive Card'.](/screenshots/link-unfurl-card.png)

The user can then choose to send either the preview or the full adaptive card as a message.

## Resources

- [Link unfurling](https://learn.microsoft.com/en-us/microsoftteams/platform/messaging-extensions/how-to/link-unfurling?tabs=desktop%2Cjson%2Cadvantages)
- [Zero install link unfurling](https://learn.microsoft.com/en-us/microsoftteams/platform/messaging-extensions/how-to/link-unfurling?tabs=desktop%2Cjson%2Cadvantages#zero-install-for-link-unfurling)
