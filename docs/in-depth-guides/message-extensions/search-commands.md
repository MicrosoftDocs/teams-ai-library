---
sidebar_label: Search Commands
title: Search Commands
zone_pivot_groups: dev-lang
description: Create search commands that allow users to search external systems and insert results as cards in Teams messages.
---
# Search commands

Message extension search commands allow users to search external systems and insert the results of that search into a message in the form of a card.

## Search command invocation locations

There are two different areas search commands can be invoked from:

1. Compose Area
2. Compose Box

### Compose Area and Box

![Screenshot of Teams with outlines around the 'Compose Box' (for typing messages) and the 'Compose Area' (the menu option next to the compose box that provides a search bar for actions and apps).](~/assets/screenshots/compose-area.png)

## Setting up your Teams app manifest

To use search commands you have to define them in the Teams app manifest. Here is an example:

```json
"composeExtensions": [
    {
        "botId": "${{BOT_ID}}",
        "commands": [
            {
                "id": "searchQuery",
                "context": [
                    "compose",
                    "commandBox"
                ],
                "description": "Test command to run query",
                "title": "Search query",
                "type": "query",
                "parameters": [
                    {
                        "name": "searchQuery",
                        "title": "Search Query",
                        "description": "Your search query",
                        "inputType": "text"
                    }
                ]
            }
        ]
    }
]
```

Here we are defining the `searchQuery` search (or query) command.

## Handle submission

Handle the search query submission when the `searchQuery` search command is invoked.


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Api.Activities.Invokes.MessageExtensions;
using Microsoft.Teams.Api.MessageExtensions;
using Microsoft.Teams.Apps.Annotations;

//...

[MessageExtension.Query]
public Response OnMessageExtensionQuery(
    [Context] QueryActivity activity,
    [Context] IContext.Client client,
    [Context] ILogger log)
{
    log.Info("[MESSAGE_EXT_QUERY] Search query received");

    var commandId = activity.Value?.CommandId;
    var query = activity.Value?.Parameters?.FirstOrDefault(p => p.Name == "searchQuery")?.Value?.ToString() ?? "";

    log.Info($"[MESSAGE_EXT_QUERY] Command: {commandId}, Query: {query}");

    if (commandId == "searchQuery")
    {
        return CreateSearchResults(query, log);
    }

    return new Response
    {
        ComposeExtension = new Result
        {
            Type = ResultType.Result,
            AttachmentLayout = Layout.List,
            Attachments = new List<Microsoft.Teams.Api.MessageExtensions.Attachment>()
        }
    };
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.api import AdaptiveCardAttachment, MessageExtensionQueryInvokeActivity, ThumbnailCardAttachment, card_attachment, InvokeResponse, AttachmentLayout, MessagingExtensionAttachment, MessagingExtensionInvokeResponse, MessagingExtensionResult, MessagingExtensionResultType
# ...

@app.on_message_ext_query
async def handle_message_ext_query(ctx: ActivityContext[MessageExtensionQueryInvokeActivity]):
    command_id = ctx.activity.value.command_id
    search_query = ""
    if ctx.activity.value.parameters and len(ctx.activity.value.parameters) > 0:
        search_query = ctx.activity.value.parameters[0].value or ""

    if command_id == "searchQuery":
        cards = await create_dummy_cards(search_query)
        attachments: list[MessagingExtensionAttachment] = []
        for card_data in cards:
            main_attachment = card_attachment(AdaptiveCardAttachment(content=card_data["card"]))
            preview_attachment = card_attachment(ThumbnailCardAttachment(content=card_data["thumbnail"]))

            attachment = MessagingExtensionAttachment(
                content_type=main_attachment.content_type, content=main_attachment.content, preview=preview_attachment
            )
            attachments.append(attachment)

        result = MessagingExtensionResult(
            type=MessagingExtensionResultType.RESULT, attachment_layout=AttachmentLayout.LIST, attachments=attachments
        )

        return MessagingExtensionInvokeResponse(compose_extension=result)

    return InvokeResponse[MessagingExtensionInvokeResponse](status=400)

```
::: zone-end

::: zone pivot="typescript"
```typescript
import { cardAttachment } from '@microsoft/teams.api';
import { App } from '@microsoft/teams.apps';
// ...

app.on('message.ext.query', async ({ activity }) => {
  const { commandId } = activity.value;
  const searchQuery = activity.value.parameters![0].value;

  if (commandId == 'searchQuery') {
    const cards = await createDummyCards(searchQuery);
    const attachments = cards.map(({ card, thumbnail }) => {
      return {
        ...cardAttachment('adaptive', card), // expanded card in the compose box...
        preview: cardAttachment('thumbnail', thumbnail), // preview card in the compose box...
      };
    });

    return {
      composeExtension: {
        type: 'result',
        attachmentLayout: 'list',
        attachments: attachments,
      },
    };
  }

  return { status: 400 };
});
```
::: zone-end



::: zone pivot="csharp"
`CreateSearchResults()` method

```csharp
using Microsoft.Teams.Api.MessageExtensions;
using Microsoft.Teams.Cards;
using Microsoft.Teams.Common;

//...

private static Response CreateSearchResults(string query, ILogger log)
{
    var attachments = new List<Microsoft.Teams.Api.MessageExtensions.Attachment>();

    // Create simple search results
    for (int i = 1; i <= 5; i++)
    {
        var card = new AdaptiveCard
        {
            Body = new List<CardElement>
            {
                new TextBlock($"Search Result {i}")
                {
                    Weight = TextWeight.Bolder,
                    Size = TextSize.Large
                },
                new TextBlock($"Query: '{query}' - Result description for item {i}")
                {
                    Wrap = true,
                    IsSubtle = true
                }
            }
        };

        var previewCard = new ThumbnailCard()
        {
            Title = $"Result {i}",
            Text = $"This is a preview of result {i} for query '{query}'."
        };

        var attachment = new Microsoft.Teams.Api.MessageExtensions.Attachment
        {
            ContentType = ContentType.AdaptiveCard,
            Content = card,
            Preview = new Microsoft.Teams.Api.MessageExtensions.Attachment
            {
                ContentType = ContentType.ThumbnailCard,
                Content = previewCard
            }
        };

        attachments.Add(attachment);
    }

    return new Response
    {
        ComposeExtension = new Result
        {
            Type = ResultType.Result,
            AttachmentLayout = Layout.List,
            Attachments = attachments
        }
    };
}
```

To implement custom actions when a user clicks on a search result item, you can handle the select item event:

```csharp
using System.Text.Json;
using Microsoft.Teams.Api;
using Microsoft.Teams.Api.Activities.Invokes.MessageExtensions;
using Microsoft.Teams.Api.MessageExtensions;
using Microsoft.Teams.Apps.Annotations;
using Microsoft.Teams.Cards;

//...

[MessageExtension.SelectItem]
public Response OnMessageExtensionSelectItem(
    [Context] SelectItemActivity activity,
    [Context] IContext.Client client,
    [Context] ILogger log)
{
    log.Info("[MESSAGE_EXT_SELECT_ITEM] Item selection received");

    var selectedItem = activity.Value;
    log.Info($"[MESSAGE_EXT_SELECT_ITEM] Selected: {JsonSerializer.Serialize(selectedItem)}");

    return CreateItemSelectionResponse(selectedItem, log);
}

// Helper method to create item selection response
private static Response CreateItemSelectionResponse(object? selectedItem, ILogger log)
{
    var itemJson = JsonSerializer.Serialize(selectedItem);

    var card = new AdaptiveCard
    {
        Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
        Body = new List<CardElement>
        {
            new TextBlock("Item Selected")
            {
                Weight = TextWeight.Bolder,
                Size = TextSize.Large,
                Color = TextColor.Good
            },
            new TextBlock("You selected the following item:")
            {
                Wrap = true
            },
            new TextBlock(itemJson)
            {
                Wrap = true,
                FontType = FontType.Monospace,
                Separator = true
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
```
::: zone-end

::: zone pivot="python"
`create_dummy_cards()` method

```python
from typing import Any, Dict, List
from microsoft.teams.cards import AdaptiveCard
# ...

async def create_dummy_cards(search_query: str) -> List[Dict[str, Any]]:
    """Create dummy cards for search results."""
    dummy_items = [
        {
            "title": "Item 1",
            "description": f"This is the first item and this is your search query: {search_query}",
        },
        {"title": "Item 2", "description": "This is the second item"},
        {"title": "Item 3", "description": "This is the third item"},
        {"title": "Item 4", "description": "This is the fourth item"},
        {"title": "Item 5", "description": "This is the fifth item"},
    ]

    cards: List[Dict[str, Any]] = []
    for item in dummy_items:
        card_data: Dict[str, Any] = {
            "card": AdaptiveCard.model_validate(
                {
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": item["title"],
                            "size": "Large",
                            "weight": "Bolder",
                            "color": "Accent",
                            "style": "heading",
                        },
                        {"type": "TextBlock", "text": item["description"], "wrap": True, "spacing": "Medium"},
                    ],
                }
            ),
            "thumbnail": {
                "title": item["title"],
                "text": item["description"],
            },
        }
        cards.append(card_data)

    return cards
```
::: zone-end

::: zone pivot="typescript"
`createDummyCards()` function

```typescript
import { ThumbnailCard } from '@microsoft/teams.api';
import { AdaptiveCard, TextBlock } from '@microsoft/teams.cards';
// ...

export async function createDummyCards(searchQuery: string) {
  const dummyItems = [
    {
      title: 'Item 1',
      description: `This is the first item and this is your search query: ${searchQuery}`,
    },
    { title: 'Item 2', description: 'This is the second item' },
    { title: 'Item 3', description: 'This is the third item' },
    { title: 'Item 4', description: 'This is the fourth item' },
    { title: 'Item 5', description: 'This is the fifth item' },
  ];

  const cards = dummyItems.map((item) => {
    return {
      card: new AdaptiveCard(
        new TextBlock(item.title, {
          size: 'Large',
          weight: 'Bolder',
          color: 'Accent',
          style: 'heading',
        }),
        new TextBlock(item.description, {
          wrap: true,
          spacing: 'Medium',
        })
      ),
      thumbnail: {
        title: item.title,
        text: item.description,
        // When a user clicks on a list item in Teams:
        // - If the thumbnail has a `tap` property: Teams will trigger the `message.ext.select-item` activity
        // - If no `tap` property: Teams will insert the full adaptive card into the compose box
        // tap: {
        //   type: "invoke",
        //   title: item.title,
        //   value: {
        //     "option": index,
        //   },
        // },
      } satisfies ThumbnailCard,
    };
  });

  return cards;
}
```
::: zone-end


The search results include both a full adaptive card and a preview card. The preview card appears as a list item in the search command area:

![Screenshot of Teams showing a message extensions search menu open with list of search results displayed as preview cards.](~/assets/screenshots/preview-card.png)

When a user clicks on a list item the dummy adaptive card is added to the compose box:

![Screenshot of Teams showing the selected adaptive card added to the compose box.](~/assets/screenshots/card-in-compose.png)

To implement custom actions when a user clicks on a search result item, you can add the `tap` property to the preview card. This allows you to handle the click event with custom logic:


::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.api import MessageExtensionSelectItemInvokeActivity, AttachmentLayout, MessagingExtensionInvokeResponse, MessagingExtensionResult, MessagingExtensionResultType
from microsoft.teams.apps import ActivityContext
# ...

@app.on_message_ext_select_item
async def handle_message_ext_select_item(ctx: ActivityContext[MessageExtensionSelectItemInvokeActivity]):
    option = getattr(ctx.activity.value, "option", None)
    await ctx.send(f"Selected item: {option}")

    result = MessagingExtensionResult(
        type=MessagingExtensionResultType.RESULT, attachment_layout=AttachmentLayout.LIST, attachments=[]
    )

    return MessagingExtensionInvokeResponse(compose_extension=result)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
// ...

app.on('message.ext.select-item', async ({ activity, send }) => {
  const { option } = activity.value;

  await send(`Selected item: ${option}`);

  return {
    status: 200,
  };
});
```
::: zone-end


## Resources

- [Search command](/microsoftteams/platform/messaging-extensions/how-to/search-commands/define-search-command?tabs=Teams-toolkit%2Cdotnet)
- [Just-In-Time Install](/microsoftteams/platform/messaging-extensions/how-to/search-commands/universal-actions-for-search-based-message-extensions#just-in-time-install)
