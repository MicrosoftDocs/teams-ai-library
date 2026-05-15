---
title: Handling Multi-Step Forms
description: Tutorial on implementing multi-step dialogs in Teams, demonstrating how to create dynamic form flows that adapt based on user input, with examples of handling state between steps and conditional navigation.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 05/15/2026
---

# Handling Multi-Step Forms

Dialogs can become complex yet powerful with multi-step forms. These forms can alter the flow of the survey depending on the user's input or customize subsequent steps based on previous answers.


::: zone pivot="csharp"
## Creating the Initial Dialog

Start off by sending an initial card in the `TaskFetch` event.
::: zone-end

::: zone pivot="python"
Start by returning the first step's card from the `dialog_open` handler.
::: zone-end

::: zone pivot="typescript"
Start by returning the first step's card from the `dialog.open` handler.
::: zone-end



::: zone pivot="csharp"
```csharp
using System.Text.Json;
using Microsoft.Teams.Api;
using Microsoft.Teams.Api.TaskModules;
using Microsoft.Teams.Cards;

//...

private static Response CreateMultiStepFormDialog()
{
    var cardJson = """
    {
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "TextBlock",
                "text": "This is a multi-step form",
                "size": "Large",
                "weight": "Bolder"
            },
            {
                "type": "Input.Text",
                "id": "name",
                "label": "Name",
                "placeholder": "Enter your name",
                "isRequired": true
            }
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "Submit",
                "data": {"submissiondialogtype": "webpage_dialog_step_1"}
            }
        ]
    }
    """;

    var dialogCard = JsonSerializer.Deserialize<AdaptiveCard>(cardJson)
        ?? throw new InvalidOperationException("Failed to deserialize multi-step form card");

    var taskInfo = new TaskInfo
    {
        Title = "Multi-step Form Dialog",
        Card = new Attachment
        {
            ContentType = new ContentType("application/vnd.microsoft.card.adaptive"),
            Content = dialogCard
        }
    };

    return new Response(new ContinueTask(taskInfo));
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.api import (
    TaskFetchInvokeActivity, TaskModuleResponse,
    TaskModuleContinueResponse, CardTaskModuleTaskInfo,
    AdaptiveCardAttachment, card_attachment,
)
from microsoft_teams.apps import ActivityContext
from microsoft_teams.cards import AdaptiveCard, TextBlock, TextInput, SubmitAction, SubmitData
# ...

@app.on_dialog_open("multi_step_form")
async def handle_multi_step_open(ctx: ActivityContext[TaskFetchInvokeActivity]):
    dialog_card = AdaptiveCard(
        schema="http://adaptivecards.io/schemas/adaptive-card.json",
        body=[
            TextBlock(text="This is a multi-step form", size="Large", weight="Bolder"),
            TextInput().with_label("Name").with_is_required(True).with_id("name").with_placeholder("Enter your name"),
        ],
        # Route to a step-specific submit handler
        actions=[
            SubmitAction().with_title("Submit").with_data(SubmitData("multi_step_1"))
        ]
    )

    return TaskModuleResponse(
        task=TaskModuleContinueResponse(
            value=CardTaskModuleTaskInfo(
                title="Multi-step Form Dialog",
                card=card_attachment(AdaptiveCardAttachment(content=dialog_card)),
            )
        )
    )
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { cardAttachment } from '@microsoft/teams.api';
import { AdaptiveCard, TextInput, SubmitAction, SubmitData } from '@microsoft/teams.cards';
// ...

app.on('dialog.open.multi_step_form', async () => {
  const dialogCard = new AdaptiveCard(
    {
      type: 'TextBlock',
      text: 'This is a multi-step form',
      size: 'Large',
      weight: 'Bolder',
    },
    new TextInput()
      .withLabel('Name')
      .withIsRequired()
      .withId('name')
      .withPlaceholder('Enter your name')
  ).withActions(
    // Route to a step-specific submit handler
    new SubmitAction()
      .withTitle('Submit')
      .withData(new SubmitData('multi_step_1'))
  );

  return {
    task: {
      type: 'continue',
      value: {
        title: 'Multi-step Form Dialog',
        card: cardAttachment('adaptive', dialogCard),
      },
    },
  };
});
```
::: zone-end



::: zone pivot="csharp"
Then in the submission handler, you can choose to `continue` the dialog with a different card.

```csharp
using System.Text.Json;
using Microsoft.Teams.Api;
using Microsoft.Teams.Api.TaskModules;
using Microsoft.Teams.Cards;

//...

// Add these cases to your OnTaskSubmit method
case "webpage_dialog_step_1":
    var nameStep1 = GetFormValue("name") ?? "Unknown";
    var nextStepCardJson = $$"""
    {
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "TextBlock",
                "text": "Email",
                "size": "Large",
                "weight": "Bolder"
            },
            {
                "type": "Input.Text",
                "id": "email",
                "label": "Email",
                "placeholder": "Enter your email",
                "isRequired": true
            }
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "Submit",
                "data": {"submissiondialogtype": "webpage_dialog_step_2", "name": "{{nameStep1}}"}
            }
        ]
    }
    """;

    var nextStepCard = JsonSerializer.Deserialize<AdaptiveCard>(nextStepCardJson)
        ?? throw new InvalidOperationException("Failed to deserialize next step card");

    var nextStepTaskInfo = new TaskInfo
    {
        Title = $"Thanks {nameStep1} - Get Email",
        Card = new Attachment
        {
            ContentType = new ContentType("application/vnd.microsoft.card.adaptive"),
            Content = nextStepCard
        }
    };

    return new Response(new ContinueTask(nextStepTaskInfo));

case "webpage_dialog_step_2":
    var nameStep2 = GetFormValue("name") ?? "Unknown";
    var emailStep2 = GetFormValue("email") ?? "No email";
    await client.Send($"Hi {nameStep2}, thanks for submitting the form! We got that your email is {emailStep2}");
    return new Response(new MessageTask("Multi-step form completed successfully"));
```
::: zone-end

::: zone pivot="python"
Then in the submission handler, return `type: "continue"` with the next card to keep the dialog open. Pass state forward using `SubmitData`'s extra data parameter.

```python
from microsoft_teams.api import (
    TaskSubmitInvokeActivity, TaskModuleResponse, TaskModuleMessageResponse,
    TaskModuleContinueResponse, CardTaskModuleTaskInfo,
    AdaptiveCardAttachment, card_attachment,
)
from microsoft_teams.apps import ActivityContext
from microsoft_teams.cards import AdaptiveCard, TextBlock, TextInput, SubmitAction, SubmitData
# ...

# Step 1 submit — show step 2
@app.on_dialog_submit("multi_step_1")
async def handle_multi_step_1_submit(ctx: ActivityContext[TaskSubmitInvokeActivity]):
    data = ctx.activity.value.data
    name = data.get("name")

    next_step_card = AdaptiveCard(
        schema="http://adaptivecards.io/schemas/adaptive-card.json",
        body=[
            TextBlock(text="Email", size="Large", weight="Bolder"),
            TextInput().with_label("Email").with_is_required(True).with_id("email").with_placeholder("Enter your email"),
        ],
        actions=[
            # Carry forward data from step 1 via extra data
            SubmitAction().with_title("Submit").with_data(
                SubmitData("multi_step_2", {"name": name})
            )
        ]
    )

    return TaskModuleResponse(
        task=TaskModuleContinueResponse(
            value=CardTaskModuleTaskInfo(
                title=f"Thanks {name} - Get Email",
                card=card_attachment(AdaptiveCardAttachment(content=next_step_card)),
            )
        )
    )

# Step 2 submit — final step, close the dialog
@app.on_dialog_submit("multi_step_2")
async def handle_multi_step_2_submit(ctx: ActivityContext[TaskSubmitInvokeActivity]):
    data = ctx.activity.value.data
    name = data.get("name")
    email = data.get("email")
    await ctx.send(f"Hi {name}, thanks for submitting the form! We got that your email is {email}")
    return TaskModuleResponse(task=TaskModuleMessageResponse(value="Multi-step form completed successfully"))
```
::: zone-end

::: zone pivot="typescript"
Then in the submission handler, return `type: 'continue'` with the next card to keep the dialog open. Pass state forward using `SubmitData`'s extra data parameter.

```typescript
import { cardAttachment } from '@microsoft/teams.api';
import { App } from '@microsoft/teams.apps';
import { AdaptiveCard, TextInput, SubmitAction, SubmitData } from '@microsoft/teams.cards';
// ...

// Step 1 submit — show step 2
app.on('dialog.submit.multi_step_1', async ({ activity }) => {
  const name = activity.value.data.name;
  const nextStepCard = new AdaptiveCard(
    {
      type: 'TextBlock',
      text: 'Email',
      size: 'Large',
      weight: 'Bolder',
    },
    new TextInput()
      .withLabel('Email')
      .withIsRequired()
      .withId('email')
      .withPlaceholder('Enter your email')
  ).withActions(
    new SubmitAction().withTitle('Submit').withData(
      // Carry forward data from step 1 via extra data
      new SubmitData('multi_step_2', { name })
    )
  );

  return {
    task: {
      type: 'continue',
      value: {
        title: `Thanks ${name} - Get Email`,
        card: cardAttachment('adaptive', nextStepCard),
      },
    },
  };
});

// Step 2 submit — final step, close the dialog
app.on('dialog.submit.multi_step_2', async ({ activity, send }) => {
  const name = activity.value.data.name;
  const email = activity.value.data.email;
  await send(`Hi ${name}, thanks for submitting the form! We got that your email is ${email}`);
  return { status: 200 };
});
```
::: zone-end



::: zone pivot="csharp"
### Complete Multi-Step Form Handler

Here's the complete example showing how to handle a multi-step form:

```csharp
using System.Text.Json;
using Microsoft.Teams.Api;
using Microsoft.Teams.Api.TaskModules;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities.Invokes;
using Microsoft.Teams.Apps.Annotations;
using Microsoft.Teams.Cards;
using Microsoft.Teams.Common.Logging;

//...

[TaskSubmit]
public async Task<Response> OnTaskSubmit([Context] Tasks.SubmitActivity activity, [Context] IContext.Client client, [Context] ILogger log)
{
    log.Info("[TASK_SUBMIT] Task submit request received");

    var data = activity.Value?.Data as JsonElement?;
    if (data == null)
    {
        log.Info("[TASK_SUBMIT] No data found in the activity value");
        return new Response(new MessageTask("No data found in the activity value"));
    }

    var submissionType = data.Value.TryGetProperty("submissiondialogtype", out var submissionTypeObj) && submissionTypeObj.ValueKind == JsonValueKind.String
        ? submissionTypeObj.ToString()
        : null;

    log.Info($"[TASK_SUBMIT] Submission type: {submissionType}");

    string? GetFormValue(string key)
    {
        if (data.Value.TryGetProperty(key, out var val))
        {
            if (val is JsonElement element)
                return element.GetString();
            return val.ToString();
        }
        return null;
    }

    switch (submissionType)
    {
        case "webpage_dialog_step_1":
            var nameStep1 = GetFormValue("name") ?? "Unknown";
            var nextStepCardJson = $$"""
            {
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": "Email",
                        "size": "Large",
                        "weight": "Bolder"
                    },
                    {
                        "type": "Input.Text",
                        "id": "email",
                        "label": "Email",
                        "placeholder": "Enter your email",
                        "isRequired": true
                    }
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                        "data": {"submissiondialogtype": "webpage_dialog_step_2", "name": "{{nameStep1}}"}
                    }
                ]
            }
            """;

            var nextStepCard = JsonSerializer.Deserialize<AdaptiveCard>(nextStepCardJson)
                ?? throw new InvalidOperationException("Failed to deserialize next step card");

            var nextStepTaskInfo = new TaskInfo
            {
                Title = $"Thanks {nameStep1} - Get Email",
                Card = new Attachment
                {
                    ContentType = new ContentType("application/vnd.microsoft.card.adaptive"),
                    Content = nextStepCard
                }
            };

            return new Response(new ContinueTask(nextStepTaskInfo));

        case "webpage_dialog_step_2":
            var nameStep2 = GetFormValue("name") ?? "Unknown";
            var emailStep2 = GetFormValue("email") ?? "No email";
            await client.Send($"Hi {nameStep2}, thanks for submitting the form! We got that your email is {emailStep2}");
            return new Response(new MessageTask("Multi-step form completed successfully"));

        default:
            return new Response(new MessageTask("Unknown submission type"));
    }
}
```
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
<!-- Not applicable -->
::: zone-end
