---
sidebar_label: Creating Dialogs
title: Creating Dialogs
zone_pivot_groups: dev-lang
---
# Creating Dialogs

> [!TIP]
> If you're not familiar with how to build Adaptive Cards, check out [the cards guide](../adaptive-cards). Understanding their basics is a prerequisite for this guide.

## Entry Point


::: zone pivot="csharp"
To open a dialog, you need to supply a special type of action to the Adaptive Card. The `TaskFetchAction` is specifically designed for this purpose - it automatically sets up the proper Teams data structure to trigger a dialog. Once this button is clicked, the dialog will open and ask the application what to show.
::: zone-end

::: zone pivot="python,typescript"
To open a dialog, you need to supply a special type of action as to the Adaptive Card. Once this button is clicked, the dialog will open and ask the application what to show.
::: zone-end



::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Api.Activities;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Annotations;
using Microsoft.Teams.Cards;
using Microsoft.Teams.Common.Logging;

//...

[Message]
public async Task OnMessage([Context] MessageActivity activity, [Context] IContext.Client client, [Context] ILogger log)
{
    // Create the launcher adaptive card
    var card = CreateDialogLauncherCard();
    await client.Send(card);
}

private static AdaptiveCard CreateDialogLauncherCard()
{
    var card = new AdaptiveCard
    {
        Body = new List<CardElement>
        {
            new TextBlock("Select the examples you want to see!")
            {
                Size = TextSize.Large,
                Weight = TextWeight.Bolder
            }
        },
        Actions = new List<Action>
        {
            new TaskFetchAction(new { opendialogtype = "simple_form" })
            {
                Title = "Simple form test"
            },
            new TaskFetchAction(new { opendialogtype = "webpage_dialog" })
            {
                Title = "Webpage Dialog"
            },
            new TaskFetchAction(new { opendialogtype = "multi_step_form" })
            {
                Title = "Multi-step Form"
            }
        }
    };

    return card;
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.api import MessageActivity, MessageActivityInput, TypingActivityInput
from microsoft.teams.apps import ActivityContext
from microsoft.teams.cards import AdaptiveCard, TextBlock, TaskFetchAction
# ...

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    await ctx.reply(TypingActivityInput())

    card = AdaptiveCard(
        schema="http://adaptivecards.io/schemas/adaptive-card.json",
        body=[
            TextBlock(
                text="Select the examples you want to see!",
                size="Large",
                weight="Bolder",
            )
        ]
    ).with_actions([
        # Special type of action to open a dialog
        TaskFetchAction(value={"OpenDialogType": "webpage_dialog"}).with_title("Webpage Dialog"),
        # This data will be passed back in an event, so we can handle what to show in the dialog
        TaskFetchAction(value={"OpenDialogType": "multi_step_form"}).with_title("Multi-step Form"),
        TaskFetchAction(value={"OpenDialogType": "mixed_example"}).with_title("Mixed Example")
    ])
    # Send the card as an attachment
    message = MessageActivityInput(text="Enter this form").add_card(card)
    await ctx.send(message)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { cardAttachment, MessageActivity } from '@microsoft/teams.api';
import { App } from '@microsoft/teams.apps';
import {
  AdaptiveCard,
  IAdaptiveCard,
  TaskFetchAction,
  TaskFetchData,
} from '@microsoft/teams.cards';
// ...

app.on('message', async ({ send }) => {
  await send({ type: 'typing' });

  // Create the launcher adaptive card
  const card: IAdaptiveCard = new AdaptiveCard({
    type: 'TextBlock',
    text: 'Select the examples you want to see!',
    size: 'Large',
    weight: 'Bolder',
  }).withActions(
    // raw action
    {
      type: 'Action.Submit',
      title: 'Simple form test',
      data: {
        msteams: {
          type: 'task/fetch',
        },
        opendialogtype: 'simple_form',
      },
    },
    // Special type of action to open a dialog
    new TaskFetchAction({})
      .withTitle('Webpage Dialog')
      // This data will be passed back in an event so we can
      // handle what to show in the dialog
      .withValue(new TaskFetchData({ opendialogtype: 'webpage_dialog' })),
    new TaskFetchAction({})
      .withTitle('Multi-step Form')
      .withValue(new TaskFetchData({ opendialogtype: 'multi_step_form' })),
    new TaskFetchAction({})
      .withTitle('Mixed Example')
      .withValue(new TaskFetchData({ opendialogtype: 'mixed_example' }))
  );

  // Send the card as an attachment
  await send(new MessageActivity('Enter this form').addCard('adaptive', card));
});
```
::: zone-end


## Handling Dialog Open Events


::: zone pivot="csharp"
Once an action is executed to open a dialog, the Teams client will send an event to the agent to request what the content of the dialog should be. When using `TaskFetchAction`, the data is nested inside an `MsTeams` property structure.
::: zone-end

::: zone pivot="python,typescript"
Once an action is executed to open a dialog, the Teams client will send an event to the agent to request what the content of the dialog should be. Here is how to handle this event:
::: zone-end



::: zone pivot="csharp"
```csharp
using System.Text.Json;
using Microsoft.Teams.Api.TaskModules;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities.Invokes;
using Microsoft.Teams.Apps.Annotations;
using Microsoft.Teams.Common.Logging;

//...

[TaskFetch]
public Microsoft.Teams.Api.TaskModules.Response OnTaskFetch([Context] Tasks.FetchActivity activity, [Context] IContext.Client client, [Context] ILogger log)
{
    var data = activity.Value?.Data as JsonElement?;
    if (data == null)
    {
        log.Info("[TASK_FETCH] No data found in the activity value");
        return new Microsoft.Teams.Api.TaskModules.Response(
            new Microsoft.Teams.Api.TaskModules.MessageTask("No data found in the activity value"));
    }

    var dialogType = data.Value.TryGetProperty("opendialogtype", out var dialogTypeElement) && dialogTypeElement.ValueKind == JsonValueKind.String
        ? dialogTypeElement.GetString()
        : null;

    log.Info($"[TASK_FETCH] Dialog type: {dialogType}");

    return dialogType switch
    {
        "simple_form" => CreateSimpleFormDialog(),
        "webpage_dialog" => CreateWebpageDialog(_configuration, log),
        "multi_step_form" => CreateMultiStepFormDialog(),
        "mixed_example" => CreateMixedExampleDialog(),
        _ => new Microsoft.Teams.Api.TaskModules.Response(
            new Microsoft.Teams.Api.TaskModules.MessageTask("Unknown dialog type"))
    };
}
```
::: zone-end

::: zone pivot="python"
```python
@app.on_dialog_open
async def handle_dialog_open(ctx: ActivityContext[TaskFetchInvokeActivity]):
    """Handle dialog open events for all dialog types."""
    card = AdaptiveCard(...)

    # Return an object with the task value that renders a card
    return InvokeResponse(
                body=TaskModuleResponse(
                    task=TaskModuleContinueResponse(
                        value=CardTaskModuleTaskInfo(
                            title="Title of Dialog",
                            card=card_attachment(AdaptiveCardAttachment(content=card)),
                        )
                    )
                )
            )
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { cardAttachment } from '@microsoft/teams.api';
import { App } from '@microsoft/teams.apps';
import { AdaptiveCard, IAdaptiveCard } from '@microsoft/teams.cards';
// ...

app.on('dialog.open', async ({ activity }) => {
  const card: IAdaptiveCard = new AdaptiveCard()...

  // Return an object with the task value that renders a card
  return {
    task: {
      type: 'continue',
      value: {
        title: 'Title of Dialog',
        card: cardAttachment('adaptive', card),
      },
    },
  };
}
```
::: zone-end


### Rendering A Card

You can render an Adaptive Card in a dialog by returning a card response.


::: zone pivot="csharp"
```csharp
using System.Text.Json;
using Microsoft.Teams.Api;
using Microsoft.Teams.Api.TaskModules;
using Microsoft.Teams.Cards;

//...

private static Microsoft.Teams.Api.TaskModules.Response CreateSimpleFormDialog()
{
    var choices = new List<Choice>
    {
        new Choice { Title = "Option 1", Value = "opt1" },
        new Choice { Title = "Option 2", Value = "opt2" },
        new Choice { Title = "Option 3", Value = "opt3" }
    };

    var dialogCard = new AdaptiveCard
    {
        Body = new List<CardElement>
        {
            new TextBlock("This is a simple form")
            {
                Size = TextSize.Large,
                Weight = TextWeight.Bolder
            },
            new TextInput
            {
                Id = "name",
                Label = "Name",
                Placeholder = "Enter your name",
                IsRequired = true
            },
            new ChoiceSetInput
            {
                Id = "preference",
                Label = "Select your preference",
                Choices = choices,
                Style = StyleEnum.Compact
            }
        },
        Actions = new List<Action>
        {
            new SubmitAction
            {
                Title = "Submit",
                Data = new { submissiondialogtype = "simple_form" }
            }
        }
    };

    var taskInfo = new TaskInfo
    {
        Title = "Simple Form Dialog",
        Card = new Attachment
        {
            ContentType = new ContentType("application/vnd.microsoft.card.adaptive"),
            Content = dialogCard
        }
    };

    return new Microsoft.Teams.Api.TaskModules.Response(
        new Microsoft.Teams.Api.TaskModules.ContinueTask(taskInfo));
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.api import AdaptiveCardAttachment, TaskFetchInvokeActivity, InvokeResponse, card_attachment
from microsoft.teams.api import CardTaskModuleTaskInfo, TaskModuleContinueResponse, TaskModuleResponse
from microsoft.teams.apps import ActivityContext
from microsoft.teams.cards import AdaptiveCard, TextBlock, TextInput, SubmitAction, SubmitActionData
# ...

@app.on_dialog_open
async def handle_dialog_open(ctx: ActivityContext[TaskFetchInvokeActivity]):
    """Handle dialog open events for all dialog types."""
    # Return an object with the task value that renders a card
    dialog_card = AdaptiveCard(
        schema="http://adaptivecards.io/schemas/adaptive-card.json",
        body=[
            TextBlock(text="This is a simple form", size="Large", weight="Bolder"),
            TextInput().with_label("Name").with_is_required(True).with_id("name").with_placeholder("Enter your name"),
        ],
        actions=[
            SubmitAction().with_title("Submit").with_data(SubmitActionData(ms_teams={"SubmissionDialogType": "simple_form"}))
        ]
    )


    # Return an object with the task value that renders a card
    return InvokeResponse(
                body=TaskModuleResponse(
                    task=TaskModuleContinueResponse(
                        value=CardTaskModuleTaskInfo(
                            title="Simple Form Dialog",
                            card=card_attachment(AdaptiveCardAttachment(content=dialog_card)),
                        )
                    )
                )
            )
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { cardAttachment } from '@microsoft/teams.api';
import { AdaptiveCard, TextInput, SubmitAction } from '@microsoft/teams.cards';
// ...

if (dialogType === 'simple_form') {
  const dialogCard = new AdaptiveCard(
    {
      type: 'TextBlock',
      text: 'This is a simple form',
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
      new SubmitAction().withTitle('Submit').withData({ submissiondialogtype: 'simple_form' })
    );

  // Return an object with the task value that renders a card
  return {
    task: {
      type: 'continue',
      value: {
        title: 'Simple Form Dialog',
        card: cardAttachment('adaptive', dialogCard),
      },
    },
  };
}
```
::: zone-end


> [!NOTE]
> The action type for submitting a dialog must be `Action.Submit`. This is a requirement of the Teams client. If you use a different action type, the dialog will not be submitted and the agent will not receive the submission event.

### Rendering A Webpage

You can render a webpage in a dialog as well. There are some security requirements to be aware of:

1. The webpage must be hosted on a domain that is allow-listed as `validDomains` in the Teams app [manifest](/teams/manifest) for the agent
2. The webpage must also host the [teams-js client library](https://www.npmjs.com/package/@microsoft/teams-js). The reason for this is that for security purposes, the Teams client will not render arbitrary webpages. As such, the webpage must explicitly opt-in to being rendered in the Teams client. Setting up the teams-js client library handles this for you.


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Api.TaskModules;
using Microsoft.Teams.Common;

//...

private static Microsoft.Teams.Api.TaskModules.Response CreateWebpageDialog(IConfiguration configuration, ILogger log)
{
    var botEndpoint = configuration["BotEndpoint"];
    if (string.IsNullOrEmpty(botEndpoint))
    {
        log.Warn("No remote endpoint detected. Using webpages for dialog will not work as expected");
        botEndpoint = "http://localhost:3978"; // Fallback for local development
    }
    else
    {
        log.Info($"Using BotEndpoint: {botEndpoint}/tabs/dialog-form");
    }

    var taskInfo = new TaskInfo
    {
        Title = "Webpage Dialog",
        Width = new Union<int, Size>(1000),
        Height = new Union<int, Size>(800),
        // Here we are using a webpage that is hosted in the same
        // server as the agent. This server needs to be publicly accessible,
        // needs to set up teams.js client library (https://www.npmjs.com/package/@microsoft/teams-js)
        // and needs to be registered in the manifest.
        Url = $"{botEndpoint}/tabs/dialog-form"
    };

    return new Microsoft.Teams.Api.TaskModules.Response(
        new Microsoft.Teams.Api.TaskModules.ContinueTask(taskInfo));
}
```
::: zone-end

::: zone pivot="python"
```python
import os
from microsoft.teams.api import InvokeResponse, TaskModuleContinueResponse, TaskModuleResponse, UrlTaskModuleTaskInfo
# ...

return InvokeResponse(
                body=TaskModuleResponse(
                    task=TaskModuleContinueResponse(
                        value=UrlTaskModuleTaskInfo(
                            title="Webpage Dialog",
                            # Here we are using a webpage that is hosted in the same
                            # server as the agent. This server needs to be publicly accessible,
                            # needs to set up teams.js client library (https://www.npmjs.com/package/@microsoft/teams-js)
                            # and needs to be registered in the manifest.
                            url=f"{os.getenv('BOT_ENDPOINT')}/tabs/dialog-webpage",
                            width=1000,
                            height=800,
                        )
                    )
                )
            )
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
// ...

return {
  task: {
    type: 'continue',
    value: {
      title: 'Webpage Dialog',
      // Here we are using a webpage that is hosted in the same
      // server as the agent. This server needs to be publicly accessible,
      // needs to set up teams.js client library (https://www.npmjs.com/package/@microsoft/teams-js)
      // and needs to be registered in the manifest.
      url: `${process.env['BOT_ENDPOINT']}/tabs/dialog-form`,
      width: 1000,
      height: 800,
    },
  },
};
```
::: zone-end



::: zone pivot="csharp"
### Setting up Embedded Web Content

To serve web content for dialogs, you can use the `AddTab` functionality to embed HTML files as resources:

```csharp
// In Program.cs when building your app
app.UseTeams();
app.AddTab("dialog-form", "Web/dialog-form");

// Configure project file to embed web resources
// In .csproj:
// <GenerateEmbeddedFilesManifest>true</GenerateEmbeddedFilesManifest>
// <EmbeddedResource Include="Web/**" />
// <Content Remove="Web/**" />
```
::: zone-end
