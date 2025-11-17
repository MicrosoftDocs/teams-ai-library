---
sidebar_position: 1
sidebar_label: Building Adaptive Cards
title: Building Adaptive Cards
summary: Guide to building Adaptive Cards with builder helpers for type-safe, maintainable UI development.
zone_pivot_groups: dev-lang
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Building Adaptive Cards

Adaptive Cards are JSON payloads that describe rich, interactive UI fragments.


::: zone pivot="csharp"
With `Microsoft.Teams.Cards` you can build these cards entirely in C# while enjoying full IntelliSense and compiler safety.
::: zone-end

::: zone pivot="python"
With `microsoft-teams-cards` you can build these cards entirely in Python while enjoying full IntelliSense and compiler safety.
::: zone-end

::: zone pivot="typescript"
With `@microsoft/teams.cards` you can build these cards entirely in TypeScript/JavaScript while enjoying full IntelliSense and compiler safety.
::: zone-end


## The Builder Pattern


::: zone pivot="csharp"
`Microsoft.Teams.Cards` exposes small **builder helpers** including `AdaptiveCard`, `TextBlock`, `ToggleInput`, `ExecuteAction`, _etc._
::: zone-end

::: zone pivot="python"
`microsoft-teams-cards` exposes small **builder helpers** including `Card`, `TextBlock`, `ToggleInput`, `ExecuteAction`, _etc._
::: zone-end

::: zone pivot="typescript"
`@microsoft/teams.cards` exposes small **builder helpers** including `Card`, `TextBlock`, `ToggleInput`, `ExecuteAction`, _etc._
::: zone-end


Each helper wraps raw JSON and provides fluent, chainable methods that keep your code concise and readable.


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Cards;

var card = new AdaptiveCard
{
    Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
    Body = new List<CardElement>
    {
        new TextBlock("Hello world")
        {
            Wrap = true,
            Weight = TextWeight.Bolder
        },
        new ToggleInput("Notify me")
        {
            Id = "notify"
        }
    },
    Actions = new List<Microsoft.Teams.Cards.Action>
    {
        new ExecuteAction
        {
            Title = "Submit",
            Data = new Union<string, SubmitActionData>(new SubmitActionData
            {
                NonSchemaProperties = new Dictionary<string, object?>
                {
                    { "action", "submit_basic" }
                }
            }),
            AssociatedInputs = AssociatedInputs.Auto
        }
    }
};
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.cards import AdaptiveCard, TextBlock, ToggleInput, ActionSet, ExecuteAction

card = AdaptiveCard(
        schema="http://adaptivecards.io/schemas/adaptive-card.json",
        body=[
            TextBlock(text="Hello world", wrap=True, weight="Bolder"),
            ToggleInput(label="Notify me").with_id("notify"),
            ActionSet(
                actions=[
                    ExecuteAction(title="Submit")
                    .with_data({"action": "submit_basic"})
                    .with_associated_inputs("auto")
                ]
            ),
        ],
    )
```
::: zone-end

::: zone pivot="typescript"
```ts
import {
  AdaptiveCard,
  TextBlock,
  ToggleInput,
  ExecuteAction,
  ActionSet,
} from '@microsoft/teams.cards';

const card = new AdaptiveCard(
  new TextBlock('Hello world', { wrap: true, weight: 'Bolder' }),
  new ToggleInput('Notify me').withId('notify'),
  new ActionSet(
    new ExecuteAction({ title: 'Submit' })
      .withData({ action: 'submit_basic' })
      .withAssociatedInputs('auto')
  )
);
```
::: zone-end


Benefits:

| Benefit     | Description                                                                   |
| ----------- | ----------------------------------------------------------------------------- |
| Readability | No deep JSON trees—just chain simple methods.                                 |
| Re‑use      | Extract snippets to functions or classes and share across cards.              |
| Safety      | Builders validate every property against the Adaptive Card schema (see next). |


::: zone pivot="csharp"
:::info
The builder helpers use strongly-typed interfaces. Use IntelliSense (Ctrl+Space) or "Go to Definition" (F12) in your IDE to explore available types and properties. Source code lives in the `Microsoft.Teams.Cards` namespace.
:::
::: zone-end

::: zone pivot="python"
:::info
The builder helpers use typed dictionaries and type hints. Use your IDE's IntelliSense features to explore available properties. Source code lives in the `teams.cards` module.
:::
::: zone-end

::: zone pivot="typescript"
:::info
Source code lives in `teams.ts/packages/cards/src/`. Feel free to inspect or extend the helpers for your own needs.
:::
::: zone-end


## Type‑safe Authoring & IntelliSense

::: zone pivot="csharp"
The package bundles the **Adaptive Card v1.5 schema** as strict C# types.
While coding you get:
::: zone-end

::: zone pivot="python"
The package bundles the **Adaptive Card v1.5 schema** as strict Python types.
While coding you get:
::: zone-end

::: zone pivot="typescript"
The package bundles the **Adaptive Card v1.5 schema** as strict TypeScript/JavaScript types.
While coding you get:
::: zone-end

- **Autocomplete** for every element and attribute.
- **In‑editor validation**—invalid enum values or missing required properties produce build errors.
- Automatic upgrades when the schema evolves; simply update the package.


::: zone pivot="csharp"
```csharp
// "Huge" is not a valid size for TextBlock - this will cause a compilation error
var textBlock = new TextBlock("Test")
{
    Wrap = true,
    Weight = TextWeight.Bolder,
    Size = "Huge" // This is invalid - should be TextSize enum
};
```
::: zone-end

::: zone pivot="python"
```python
# "huge" is not a valid size for TextBlock
text_block = TextBlock(text="Test", wrap=True, weight="Bolder", size="huge"),
```
::: zone-end

::: zone pivot="typescript"
```typescript
// @ts-expect-error: "huge" is not a valid size for TextBlock
const textBlock = new TextBlock('Valid', { size: 'huge' });
```
::: zone-end


## The Visual Designer

Prefer a drag‑and‑drop approach? Use [Microsoft's Adaptive Card Designer](https://adaptivecards.microsoft.com/designer.html):

1. Add elements visually until the card looks right.
2. Copy the JSON payload from the editor pane.
3. Paste the JSON into your project **or** convert it to builder calls:


::: zone pivot="csharp"
```csharp
var cardJson = """
{
    "type": "AdaptiveCard",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "verticalContentAlignment": "center",
                    "items": [
                        {
                            "type": "Image",
                            "style": "Person",
                            "url": "https://aka.ms/AAp9xo4",
                            "size": "Small",
                            "altText": "Portrait of David Claux"
                        }
                    ],
                    "width": "auto"
                },
                {
                    "type": "Column",
                    "spacing": "medium",
                    "verticalContentAlignment": "center",
                    "items": [
                        {
                            "type": "TextBlock",
                            "weight": "Bolder",
                            "text": "David Claux",
                            "wrap": true
                        }
                    ],
                    "width": "auto"
                },
                {
                    "type": "Column",
                    "spacing": "medium",
                    "verticalContentAlignment": "center",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Principal Platform Architect at Microsoft",
                            "isSubtle": true,
                            "wrap": true
                        }
                    ],
                    "width": "stretch"
                }
            ]
        }
    ],
    "version": "1.5",
    "schema": "http://adaptivecards.io/schemas/adaptive-card.json"
}
""";

// Deserialize the JSON into an AdaptiveCard object
var card = AdaptiveCard.Deserialize(cardJson);

// Send the card
await client.Send(card);
```
::: zone-end

::: zone pivot="python"
```python

card = AdaptiveCard.model_validate(
    {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "verticalContentAlignment": "center",
                        "items": [
                            {
                                "type": "Image",
                                "style": "Person",
                                "url": "https://aka.ms/AAp9xo4",
                                "size": "Small",
                                "altText": "Portrait of David Claux",
                            }
                        ],
                        "width": "auto",
                    },
                    {
                        "type": "Column",
                        "spacing": "medium",
                        "verticalContentAlignment": "center",
                        "items": [{"type": "TextBlock", "weight": "Bolder", "text": "David Claux", "wrap": True}],
                        "width": "auto",
                    },
                    {
                        "type": "Column",
                        "spacing": "medium",
                        "verticalContentAlignment": "center",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Principal Platform Architect at Microsoft",
                                "isSubtle": True,
                                "wrap": True,
                            }
                        ],
                        "width": "stretch",
                    },
                ],
            }
        ],
        "version": "1.5",
    }
)
# Send the card as an attachment
message = MessageActivityInput(text="Hello text!").add_card(card)
```
::: zone-end

::: zone pivot="typescript"
```typescript
const cardJson = /* copied JSON */;
const card = new AdaptiveCard().withBody(cardJson);
```

```ts
const rawCard: IAdaptiveCard = {
  type: 'AdaptiveCard',
  body: [
    {
      text: 'Please fill out the below form to send a game purchase request.',
      wrap: true,
      type: 'TextBlock',
      style: 'heading',
    },
    {
      columns: [
        {
          width: 'stretch',
          items: [
            {
              choices: [
                { title: 'Call of Duty', value: 'call_of_duty' },
                { title: "Death's Door", value: 'deaths_door' },
                { title: 'Grand Theft Auto V', value: 'grand_theft' },
                { title: 'Minecraft', value: 'minecraft' },
              ],
              style: 'filtered',
              placeholder: 'Search for a game',
              id: 'choiceGameSingle',
              type: 'Input.ChoiceSet',
              label: 'Game:',
            },
          ],
          type: 'Column',
        },
      ],
      type: 'ColumnSet',
    },
  ],
  actions: [
    {
      title: 'Request purchase',
      type: 'Action.Execute',
      data: { action: 'purchase_item' },
    },
  ],
  version: '1.5',
};
```
::: zone-end


::: zone pivot="csharp,python"
This method leverages the full Adaptive Card schema and ensures that the payload adheres strictly to `AdaptiveCard`.
::: zone-end

::: zone pivot="typescript"
This method leverages the full Adaptive Card schema and ensures that the payload adheres strictly to `IAdaptiveCard`.
::: zone-end

:::tip
You can use a combination of raw JSON and builder helpers depending on whatever you find easier.
:::

## End‑to‑end Example – Task Form Card

Below is a complete example showing a task management form.


::: zone pivot="csharp"
# [Controller](#tab/controller)
```csharp
[Message]
public async Task OnMessage([Context] MessageActivity activity, [Context] IContext.Client client)
{
    var text = activity.Text?.ToLowerInvariant() ?? "";

    if (text.Contains("form"))
    {
        await client.Typing();
        var card = CreateTaskFormCard();
        await client.Send(card);
    }
}
```

# [Minimal](#tab/minimal)
```csharp
teams.OnMessage(async context =>
{
    var text = context.Activity.Text?.ToLowerInvariant() ?? "";

    if (text.Contains("form"))
    {
        await context.Typing();
        var card = CreateTaskFormCard();
        await context.Send(card);
    }
});
```

---



The definition for `CreateTaskFormCard` is as follows
::: zone-end

::: zone pivot="python,typescript"
Notice how the builder pattern keeps the file readable and maintainable:
::: zone-end



::: zone pivot="csharp"
```csharp
private static AdaptiveCard CreateTaskFormCard()
{
    return new AdaptiveCard
    {
        Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
        Body = new List<CardElement>
        {
            new TextBlock("Create New Task")
            {
                Weight = TextWeight.Bolder,
                Size = TextSize.Large
            },
            new TextInput
            {
                Id = "title",
                Label = "Task Title",
                Placeholder = "Enter task title"
            },
            new TextInput
            {
                Id = "description",
                Label = "Description",
                Placeholder = "Enter task details",
                IsMultiline = true
            },
            new ChoiceSetInput
            {
                Id = "priority",
                Label = "Priority",
                Value = "medium",
                Choices = new List<Choice>
                {
                    new() { Title = "High", Value = "high" },
                    new() { Title = "Medium", Value = "medium" },
                    new() { Title = "Low", Value = "low" }
                }
            },
            new DateInput
            {
                Id = "due_date",
                Label = "Due Date",
                Value = DateTime.Now.ToString("yyyy-MM-dd")
            }
        },
        Actions = new List<Microsoft.Teams.Cards.Action>
        {
            new ExecuteAction
            {
                Title = "Create Task",
                Data = new Union<string, SubmitActionData>(new SubmitActionData
                {
                    NonSchemaProperties = new Dictionary<string, object?>
                    {
                        { "action", "create_task" }
                    }
                }),
                AssociatedInputs = AssociatedInputs.Auto,
                Style = ActionStyle.Positive
            }
        }
    };
}
```
::: zone-end

::: zone pivot="python"
```python
from datetime import datetime
from microsoft.teams.api import MessageActivity, TypingActivityInput
from microsoft.teams.apps import ActivityContext
from microsoft.teams.cards import AdaptiveCard, TextBlock, ActionSet, ExecuteAction, Choice, ChoiceSetInput, DateInput, TextInput
# ...

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    await ctx.reply(TypingActivityInput())

    card = AdaptiveCard(
        schema="http://adaptivecards.io/schemas/adaptive-card.json",
        body=[
            TextBlock(text="Create New Task", weight="Bolder", size="Large"),
            TextInput(id="title").with_label("Task Title").with_placeholder("Enter task title"),
            TextInput(id="description").with_label("Description").with_placeholder("Enter task details").with_is_multiline(True),
            ChoiceSetInput(choices=[
                Choice(title="High", value="high"),
                Choice(title="Medium", value="medium"),
                Choice(title="Low", value="low"),
            ]).with_id("priority").with_label("Priority").with_value("medium"),
            DateInput(id="due_date").with_label("Due Date").with_value(datetime.now().strftime("%Y-%m-%d")),
            ActionSet(
                actions=[
                    ExecuteAction(title="Create Task")
                    .with_data({"action": "create_task"})
                    .with_associated_inputs("auto")
                    .with_style("positive")
                ]
            ),
        ],
    )

    await ctx.send(card)
```
::: zone-end

::: zone pivot="typescript"
```ts
import {
  AdaptiveCard,
  TextBlock,
  TextInput,
  ChoiceSetInput,
  DateInput,
  ActionSet,
  ExecuteAction,
} from '@microsoft/teams.cards';
import { App } from '@microsoft/teams.apps';
// ...

app.on('message', async ({ send, activity }) => {
  await send({ type: 'typing' });
  const card = new AdaptiveCard(
    new TextBlock('Create New Task', {
      size: 'Large',
      weight: 'Bolder',
    }),
    new TextInput({ id: 'title' }).withLabel('Task Title').withPlaceholder('Enter task title'),
    new TextInput({ id: 'description' })
      .withLabel('Description')
      .withPlaceholder('Enter task details')
      .withIsMultiline(true),
    new ChoiceSetInput(
      { title: 'High', value: 'high' },
      { title: 'Medium', value: 'medium' },
      { title: 'Low', value: 'low' }
    )
      .withId('priority')
      .withLabel('Priority')
      .withValue('medium'),
    new DateInput({ id: 'due_date' })
      .withLabel('Due Date')
      .withValue(new Date().toISOString().split('T')[0]),
    new ActionSet(
      new ExecuteAction({ title: 'Create Task' })
        .withData({ action: 'create_task' })
        .withAssociatedInputs('auto')
        .withStyle('positive')
    )
  );
  await send(card);
  // Or build a complex activity out that includes the card:
  // const message  = new MessageActivity('Enter this form').addCard('adaptive', card);
  // await send(message);
});
```
::: zone-end


## Additional Resources

- [**Official Adaptive Card Documentation**](https://adaptivecards.microsoft.com/)
- [**Adaptive Cards Designer**](https://adaptivecards.microsoft.com/designer.html)

### Summary

- Use **builder helpers** for readable, maintainable card code.
- Enjoy **full type safety** and IDE assistance.
- Prototype quickly in the **visual designer** and refine with builders.

Happy card building! 🎉
