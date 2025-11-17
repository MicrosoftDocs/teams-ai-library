---
sidebar_label: Executing Actions
title: Executing Actions
zone_pivot_groups: dev-lang
description: How to implement interactive elements in Adaptive Cards through actions like buttons, links, and input submission triggers.
---
# Executing Actions

Adaptive Cards support interactive elements through **actions**—buttons, links, and input submission triggers that respond to user interaction.
You can use these to collect form input, trigger workflows, show task modules, open URLs, and more.

## Action Types

The Teams SDK supports several action types for different interaction patterns:

| Action Type               | Purpose                | Description                                                                  |
| ------------------------- | ---------------------- | ---------------------------------------------------------------------------- |
| `Action.Execute`          | Server‑side processing | Send data to your bot for processing. Best for forms & multi‑step workflows. |
| `Action.Submit`           | Simple data submission | Legacy action type. Prefer `Execute` for new projects.                       |
| `Action.OpenUrl`          | External navigation    | Open a URL in the user's browser.                                            |
| `Action.ShowCard`         | Progressive disclosure | Display a nested card when clicked.                                          |
| `Action.ToggleVisibility` | UI state management    | Show/hide card elements dynamically.                                         |

> [!NOTE]
> For complete reference, see the [official documentation](https://adaptivecards.microsoft.com/?topic=Action.Execute).

## Creating Actions with the SDK

### Single Actions

The SDK provides builder helpers that abstract the underlying JSON. For example:


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Cards;

var action = new ExecuteAction
{
    Title = "Submit Feedback",
    Data = new Union<string, SubmitActionData>(new SubmitActionData
    {
        NonSchemaProperties = new Dictionary<string, object?>
        {
            { "action", "submit_feedback" }
        }
    }),
    AssociatedInputs = AssociatedInputs.Auto
};
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.cards.core import ExecuteAction
# ...

action = ExecuteAction(title="Submit Feedback")
                    .with_data({"action": "submit_feedback"})
                    .with_associated_inputs("auto")
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { ExecuteAction } from '@microsoft/teams.cards';
// ...

new ExecuteAction({ title: 'Submit Feedback' })
  .withData({ action: 'submit_feedback' })
  .withAssociatedInputs('auto'),
```
::: zone-end


### Action Sets

Group actions together using `ActionSet`:


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Cards;

var card = new AdaptiveCard
{
    Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
    Actions = new List<Microsoft.Teams.Cards.Action>
    {
        new ExecuteAction
        {
            Title = "Submit Feedback",
            Data = new Union<string, SubmitActionData>(new SubmitActionData
            {
                NonSchemaProperties = new Dictionary<string, object?>
                {
                    { "action", "submit_feedback" }
                }
            })
        },
        new OpenUrlAction("https://adaptivecards.microsoft.com")
        {
            Title = "Learn More"
        }
    }
};
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.cards.core import ActionSet, ExecuteAction, OpenUrlAction
# ...

action_set = ActionSet(
                actions=[
                    ExecuteAction(title="Submit Feedback")
                    .with_data({"action": "submit_feedback"}),
                    OpenUrlAction(url="https://adaptivecards.microsoft.com").with_title("Learn More")
                ]
            ),
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { ExecuteAction, OpenUrlAction, ActionSet } from '@microsoft/teams.cards';
// ...

new ActionSet(
  new ExecuteAction({ title: 'Submit Feedback' })
    .withData({ action: 'submit_feedback' })
    .withAssociatedInputs('auto'),
  new OpenUrlAction('https://adaptivecards.microsoft.com').withTitle('Learn More')
);
```
::: zone-end


### Raw JSON Alternative

::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
Just like when building cards, if you prefer to work with raw JSON, you can do just that. You get type safety for free in Python.
::: zone-end

::: zone pivot="typescript"
Just like when building cards, if you prefer to work with raw JSON, you can do just that. You get type safety for free in TypeScript.
::: zone-end


::: zone pivot="csharp"
```csharp
var actionJson = """
{
  "type": "Action.OpenUrl",
  "url": "https://adaptivecards.microsoft.com",
  "title": "Learn More"
}
""";
var action = OpenUrlAction.Deserialize(actionJson);
```
::: zone-end

::: zone pivot="python"
```python
json = {
  "type": "Action.OpenUrl",
  "url": "https://adaptivecards.microsoft.com",
  "title": "Learn More",
}
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { IOpenUrlAction } from '@microsoft/teams.cards';
// ...

{
  type: 'Action.OpenUrl',
  url: 'https://adaptivecards.microsoft.com',
  title: 'Learn More',
} as const satisfies IOpenUrlAction
```
::: zone-end


## Working with Input Values

### Associating data with the cards

Sometimes you want to send a card and have it be associated with some data. Set the `data` value to be sent back to the client so you can associate it with a particular entity.


::: zone pivot="csharp"
```csharp
private static AdaptiveCard CreateProfileCard()
{
    return new AdaptiveCard
    {
        Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
        Body = new List<CardElement>
        {
            new TextBlock("User Profile")
            {
                Weight = TextWeight.Bolder,
                Size = TextSize.Large
            },
            new TextInput
            {
                Id = "name",
                Label = "Name",
                Value = "John Doe"
            },
            new TextInput
            {
                Id = "email",
                Label = "Email",
                Value = "john@contoso.com"
            },
            new ToggleInput("Subscribe to newsletter")
            {
                Id = "subscribe",
                Value = "false"
            }
        },
        Actions = new List<Microsoft.Teams.Cards.Action>
        {
            new ExecuteAction
            {
                Title = "Save",
                // entity_id will come back after the user submits
                Data = new Union<string, SubmitActionData>(new SubmitActionData
                {
                    NonSchemaProperties = new Dictionary<string, object?>
                    {
                        { "action", "save_profile" },
                        { "entity_id", "12345" }
                    }
                }),
                AssociatedInputs = AssociatedInputs.Auto
            }
        }
    };
}

// Data received in handler (conceptual structure)
/*
{
  "action": "save_profile",
  "entity_id": "12345",     // From action data
  "name": "John Doe",       // From name input
  "email": "john@doe.com",  // From email input
  "subscribe": "true"       // From toggle input (as string)
}

Accessed in C# as:
- data["action"] → "save_profile"
- data["entity_id"] → "12345"
- data["name"] → "John Doe"
- data["email"] → "john@doe.com"
- data["subscribe"] → "true"
*/
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.cards import AdaptiveCard, ActionSet, ExecuteAction, OpenUrlAction
from microsoft.teams.cards.core import TextInput, ToggleInput
# ...

profile_card = AdaptiveCard(
        schema="http://adaptivecards.io/schemas/adaptive-card.json",
        body=[
            TextInput(id="name").with_label("Name").with_value("John Doe"),
            TextInput(id="email", label="Email", value="john@contoso.com"),
            ToggleInput(title="Subscribe to newsletter").with_id("subscribe").with_value("false"),
            ActionSet(
                actions=[
                    ExecuteAction(title="Save")
                    # entity_id will come back after the user submits
                    .with_data({"action": "save_profile", "entity_id": "12345"}),
                ]
            ),
        ],
    )

# Data received in handler:
"""
{
  "action": "save_profile",
  "entity_id": "12345",     # From action data
  "name": "John Doe",       # From name input
  "email": "john@doe.com",  # From email input
  "subscribe": "true"       # From toggle input (as string)
}
"""
```
::: zone-end

::: zone pivot="typescript"
```typescript
import {
  AdaptiveCard,
  TextInput,
  ToggleInput,
  ActionSet,
  ExecuteAction,
} from '@microsoft/teams.cards';
// ...

function editProfileCard() {
  const card = new AdaptiveCard(
    new TextInput({ id: 'name' }).withLabel('Name').withValue('John Doe'),
    new TextInput({ id: 'email', label: 'Email', value: 'john@contoso.com' }),
    new ToggleInput('Subscribe to newsletter').withId('subscribe').withValue('false'),
    new ActionSet(
      new ExecuteAction({ title: 'Save' })
        .withData({
          action: 'save_profile',
          entityId: '12345', // This will come back once the user submits
        })
        .withAssociatedInputs('auto')
    )
  );

  // Data received in handler
  /**
  {
    action: "save_profile",
    entityId: "12345",     // From action data
    name: "John Doe",      // From name input
    email: "john@doe.com", // From email input
    subscribe: "true"      // From toggle input (as string)
  }
  */

  return card;
}
```
::: zone-end


### Input Validation

Input Controls provide ways for you to validate. More details can be found on the Adaptive Cards [documentation](https://adaptivecards.microsoft.com/?topic=input-validation).


::: zone pivot="csharp"
```csharp
private static AdaptiveCard CreateProfileCardWithValidation()
{
    return new AdaptiveCard
    {
        Schema = "http://adaptivecards.io/schemas/adaptive-card.json",
        Body = new List<CardElement>
        {
            new TextBlock("Profile with Validation")
            {
                Weight = TextWeight.Bolder,
                Size = TextSize.Large
            },
            new NumberInput
            {
                Id = "age",
                Label = "Age",
                IsRequired = true,
                Min = 0,
                Max = 120
            },
            // Can configure custom error messages
            new TextInput
            {
                Id = "name",
                Label = "Name",
                IsRequired = true,
                ErrorMessage = "Name is required"
            },
            new TextInput
            {
                Id = "location",
                Label = "Location"
            }
        },
        Actions = new List<Microsoft.Teams.Cards.Action>
        {
            new ExecuteAction
            {
                Title = "Save",
                // All inputs should be validated
                Data = new Union<string, SubmitActionData>(new SubmitActionData
                {
                    NonSchemaProperties = new Dictionary<string, object?>
                    {
                        { "action", "save_profile" }
                    }
                }),
                AssociatedInputs = AssociatedInputs.Auto
            }
        }
    };
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.cards import AdaptiveCard, ActionSet, ExecuteAction, NumberInput, TextInput
# ...

def create_profile_card_input_validation():
    age_input = NumberInput(id="age").with_label("age").with_is_required(True).with_min(0).with_max(120)
    # Can configure custom error messages
    name_input = TextInput(id="name").with_label("Name").with_is_required(True).with_error_message("Name is required")

    card = AdaptiveCard(
        schema="http://adaptivecards.io/schemas/adaptive-card.json",
        body=[
            age_input,
            name_input,
            TextInput(id="location").with_label("Location"),
            ActionSet(
                actions=[
                    ExecuteAction(title="Save")
                    # All inputs should be validated
                    .with_data({"action": "save_profile"})
                    .with_associated_inputs("auto")
                ]
            ),
        ],
    )
    return card
```
::: zone-end

::: zone pivot="typescript"
```typescript
import {
  AdaptiveCard,
  NumberInput,
  TextInput,
  ActionSet,
  ExecuteAction,
} from '@microsoft/teams.cards';
// ...

function createProfileCardInputValidation() {
  const ageInput = new NumberInput({ id: 'age' })
    .withLabel('Age')
    .withIsRequired(true)
    .withMin(0)
    .withMax(120);

  const nameInput = new TextInput({ id: 'name' })
    .withLabel('Name')
    .withIsRequired()
    .withErrorMessage('Name is required!'); // Custom error messages
  const card = new AdaptiveCard(
    nameInput,
    ageInput,
    new TextInput({ id: 'location' }).withLabel('Location'),
    new ActionSet(
      new ExecuteAction({ title: 'Save' })
        .withData({
          action: 'save_profile',
        })
        .withAssociatedInputs('auto') // All inputs should be validated
    )
  );

  return card;
}
```
::: zone-end


## Server Handlers

### Basic Structure

Card actions arrive as `card.action` activities in your app. These give you access to the validated input values plus any `data` values you had configured to be sent back to you.


::: zone pivot="csharp"
```csharp
using System.Text.Json;
using Microsoft.Teams.Api.Activities.Invokes.AdaptiveCards;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Annotations;
using Microsoft.Teams.Common.Logging;

//...

[Microsoft.Teams.Apps.Activities.Invokes.AdaptiveCard.Action]
public async Task<ActionResponse> OnCardAction([Context] ActionActivity activity, [Context] IContext.Client client, [Context] ILogger log)
{
    log.Info("[CARD_ACTION] Card action received");

    var data = activity.Value?.Action?.Data;

    if (data == null)
    {
        log.Error("[CARD_ACTION] No data in card action");
        return new ActionResponse.Message("No data specified") { StatusCode = 400 };
    }

    // Extract action from the Value property
    string? action = data.TryGetValue("action", out var actionObj) ? actionObj?.ToString() : null;

    if (string.IsNullOrEmpty(action))
    {
        log.Error("[CARD_ACTION] No action specified in card data");
        return new ActionResponse.Message("No action specified") { StatusCode = 400 };
    }

    log.Info($"[CARD_ACTION] Processing action: {action}");

    // Helper method to extract form field values
    string? GetFormValue(string key)
    {
        if (data.TryGetValue(key, out var val))
        {
            if (val is JsonElement element)
                return element.GetString();
            return val?.ToString();
        }
        return null;
    }

    switch (action)
    {
        case "submit_feedback":
            var feedbackText = GetFormValue("feedback") ?? "No feedback provided";
            await client.Send($"Feedback received: {feedbackText}");
            break;

        case "save_profile":
            var name = GetFormValue("name") ?? "Unknown";
            var email = GetFormValue("email") ?? "No email";
            var subscribe = GetFormValue("subscribe") ?? "false";
            await client.Send($"Profile saved!\nName: {name}\nEmail: {email}\nSubscribed: {subscribe}");
            break;

        case "create_task":
            var title = GetFormValue("title") ?? "Untitled";
            var priority = GetFormValue("priority") ?? "medium";
            var dueDate = GetFormValue("due_date") ?? "No date";
            await client.Send($"Task created!\nTitle: {title}\nPriority: {priority}\nDue: {dueDate}");
            break;

        default:
            log.Error($"[CARD_ACTION] Unknown action: {action}");
            return new ActionResponse.Message("Unknown action") { StatusCode = 400 };
    }

    return new ActionResponse.Message("Action processed successfully") { StatusCode = 200 };
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.api import AdaptiveCardInvokeActivity, AdaptiveCardActionErrorResponse, AdaptiveCardActionMessageResponse, HttpError, InnerHttpError, AdaptiveCardInvokeResponse
from microsoft.teams.apps import ActivityContext
# ...

@app.on_card_action
async def handle_card_action(ctx: ActivityContext[AdaptiveCardInvokeActivity]) -> AdaptiveCardInvokeResponse:
    data = ctx.activity.value.action.data
    if not data.get("action"):
        return AdaptiveCardActionErrorResponse(
            status_code=400,
            type="application/vnd.microsoft.error",
            value=HttpError(
                code="BadRequest",
                message="No action specified",
                inner_http_error=InnerHttpError(
                    status_code=400,
                    body={"error": "No action specified"},
                ),
            ),
        )

    print("Received action data:", data)

    if data["action"] == "submit_feedback":
        await ctx.send(f"Feedback received: {data.get('feedback')}")
    elif data["action"] == "purchase_item":
        await ctx.send(f"Purchase request received for game: {data.get('choiceGameSingle')}")
    elif data["action"] == "save_profile":
        await ctx.send(
            f"Profile saved!\nName: {data.get('name')}\nEmail: {data.get('email')}\nSubscribed: {data.get('subscribe')}"
        )
    else:
        return AdaptiveCardActionErrorResponse(
            status_code=400,
            type="application/vnd.microsoft.error",
            value=HttpError(
                code="BadRequest",
                message="Unknown action",
                inner_http_error=InnerHttpError(
                    status_code=400,
                    body={"error": "Unknown action"},
                ),
            ),
        )

    return AdaptiveCardActionMessageResponse(
        status_code=200,
        type="application/vnd.microsoft.activity.message",
        value="Action processed successfully",
    )
```
::: zone-end

::: zone pivot="typescript"
```typescript
import {
  AdaptiveCardActionErrorResponse,
  AdaptiveCardActionMessageResponse,
} from '@microsoft/teams.api';
import { App } from '@microsoft/teams.apps';
// ...

app.on('card.action', async ({ activity, send }) => {
  const data = activity.value?.action?.data;
  if (!data?.action) {
    return {
      statusCode: 400,
      type: 'application/vnd.microsoft.error',
      value: {
        code: 'BadRequest',
        message: 'No action specified',
        innerHttpError: {
          statusCode: 400,
          body: { error: 'No action specified' },
        },
      },
    } satisfies AdaptiveCardActionErrorResponse;
  }

  console.debug('Received action data:', data);

  switch (data.action) {
    case 'submit_feedback':
      await send(`Feedback received: ${data.feedback}`);
      break;

    case 'purchase_item':
      await send(`Purchase request received for game: ${data.choiceGameSingle}`);
      break;

    case 'save_profile':
      await send(
        `Profile saved!\nName: ${data.name}\nEmail: ${data.email}\nSubscribed: ${data.subscribe}`
      );
      break;

    default:
      return {
        statusCode: 400,
        type: 'application/vnd.microsoft.error',
        value: {
          code: 'BadRequest',
          message: 'Unknown action',
          innerHttpError: {
            statusCode: 400,
            body: { error: 'Unknown action' },
          },
        },
      } satisfies AdaptiveCardActionErrorResponse;
  }

  return {
    statusCode: 200,
    type: 'application/vnd.microsoft.activity.message',
    value: 'Action processed successfully',
  } satisfies AdaptiveCardActionMessageResponse;
});
```
::: zone-end



::: zone pivot="csharp"
> [!NOTE]
> The `data` values come from JSON and need to be extracted using the helper method shown above to handle different JSON element types.
::: zone-end

::: zone pivot="python"
> [!NOTE]
> The `data` values are accessible as a dictionary and can be accessed using `.get()` method for safe access.
::: zone-end

::: zone pivot="typescript"
> [!NOTE]
> The `data` values are not typed and come as `any`, so you will need to cast them to the correct type in this case.
::: zone-end
