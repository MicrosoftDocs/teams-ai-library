---
sidebar_label: Handling Multi-Step Forms
title: Handling Multi-Step Forms
zone_pivot_groups: dev-lang
description: Tutorial on implementing multi-step dialogs in Teams, demonstrating how to create dynamic form flows that adapt based on user input, with examples of handling state between steps and conditional navigation.
---
# Handling Multi-Step Forms

Dialogs can become complex yet powerful with multi-step forms. These forms can alter the flow of the survey depending on the user's input or customize subsequent steps based on previous answers.


::: zone pivot="csharp"
## Creating the Initial Dialog

Start off by sending an initial card in the `TaskFetch` event.
::: zone-end

::: zone pivot="python"
Start off by sending an initial card in the `dialog_open` event.
::: zone-end

::: zone pivot="typescript"
Start off by sending an initial card in the `dialog.open` event.
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
dialog_card = AdaptiveCard.model_validate(
            {
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [
                    {"type": "TextBlock", "text": "This is a multi-step form", "size": "Large", "weight": "Bolder"},
                    {
                        "type": "Input.Text",
                        "id": "name",
                        "label": "Name",
                        "placeholder": "Enter your name",
                        "isRequired": True,
                    },
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                        "data": {"submissiondialogtype": "webpage_dialog_step_1"},
                    }
                ],
            }
        )
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { cardAttachment } from '@microsoft/teams.api';
import { AdaptiveCard, TextInput, SubmitAction } from '@microsoft/teams.cards';
// ...

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
)
  // Inside the dialog, the card actions for submitting the card must be
  // of type Action.Submit
  .withActions(
    new SubmitAction()
      .withTitle('Submit')
      .withData({ submissiondialogtype: 'webpage_dialog_step_1' })
  );

// Return an object with the task value that renders a card
return {
  task: {
    type: 'continue',
    value: {
      title: 'Multi-step Form Dialog',
      card: cardAttachment('adaptive', dialogCard),
    },
  },
};
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
Then in the submission handler, you can choose to `continue` the dialog with a different card.

```python

@app.on_dialog_submit
async def handle_dialog_submit(ctx: ActivityContext[TaskSubmitInvokeActivity]):
    """Handle dialog submit events for all dialog types."""
    data: Optional[Any] = ctx.activity.value.data
    dialog_type = data.get("submissiondialogtype") if data else None

    if dialog_type == "webpage_dialog":
        name = data.get("name") if data else None
        email = data.get("email") if data else None
        await ctx.send(f"Hi {name}, thanks for submitting the form! We got that your email is {email}")
        return InvokeResponse(
            body=TaskModuleResponse(task=TaskModuleMessageResponse(value="Form submitted successfully"))
        )

    elif dialog_type == "webpage_dialog_step_1":
        name = data.get("name") if data else None
        next_step_card = AdaptiveCard.model_validate(
            {
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [
                    {"type": "TextBlock", "text": "Email", "size": "Large", "weight": "Bolder"},
                    {
                        "type": "Input.Text",
                        "id": "email",
                        "label": "Email",
                        "placeholder": "Enter your email",
                        "isRequired": True,
                    },
                ],
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                        "data": {"submissiondialogtype": "webpage_dialog_step_2", "name": name},
                    }
                ],
            }
        )

        return InvokeResponse(
            body=TaskModuleResponse(
                task=TaskModuleContinueResponse(
                    value=CardTaskModuleTaskInfo(
                        title=f"Thanks {name} - Get Email",
                        card=card_attachment(AdaptiveCardAttachment(content=next_step_card)),
                    )
                )
            )
        )

    elif dialog_type == "webpage_dialog_step_2":
        name = data.get("name") if data else None
        email = data.get("email") if data else None
        await ctx.send(f"Hi {name}, thanks for submitting the form! We got that your email is {email}")
        return InvokeResponse(
            body=TaskModuleResponse(task=TaskModuleMessageResponse(value="Multi-step form completed successfully"))
        )

    return TaskModuleResponse(task=TaskModuleMessageResponse(value="Unknown submission type"))

```
::: zone-end

::: zone pivot="typescript"
Then in the submission handler, you can choose to `continue` the dialog with a different card.

```typescript
import { cardAttachment } from '@microsoft/teams.api';
import { App } from '@microsoft/teams.apps';
import { AdaptiveCard, TextInput, SubmitAction } from '@microsoft/teams.cards';
// ...

app.on('dialog.submit', async ({ activity, send, next }) => {
  const dialogType = activity.value.data.submissiondialogtype;

  if (dialogType === 'webpage_dialog_step_1') {
    // This is data from the form that was submitted
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
      new SubmitAction().withTitle('Submit').withData({
        // This same handler will get called, so we need to identify the step
        // in the returned data
        submissiondialogtype: 'webpage_dialog_step_2',
        // Carry forward data from previous step
        name,
      })
    );
    return {
      task: {
        // This indicates that the dialog flow should continue
        type: 'continue',
        value: {
          // Here we customize the title based on the previous response
          title: `Thanks ${name} - Get Email`,
          card: cardAttachment('adaptive', nextStepCard),
        },
      },
    };
  } else if (dialogType === 'webpage_dialog_step_2') {
    const name = activity.value.data.name;
    const email = activity.value.data.email;
    await send(`Hi ${name}, thanks for submitting the form! We got that your email is ${email}`);
    // You can also return a blank response
    return {
      status: 200,
    };
  }
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
