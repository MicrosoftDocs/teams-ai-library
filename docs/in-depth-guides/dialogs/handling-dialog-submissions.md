---
title: Handling Dialog Submissions
description: Guide to processing dialog submissions in Teams applications, showing how to handle form data from both Adaptive Cards and web pages using dialog submission event handlers.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 11/17/2025
---

# Handling Dialog Submissions


::: zone pivot="csharp"
Dialogs have a specific `TaskSubmit` event to handle submissions. When a user submits a form inside a dialog, the app is notified via this event, which is then handled to process the submission values, and can either send a response or proceed to more steps in the dialogs (see [Multi-step Dialogs](./handling-multi-step-forms.md)).

:::warning Return Type Requirement
Methods decorated with `[TaskSubmit]` **must** return `Task<Microsoft.Teams.Api.TaskModules.Response>`. Every code path must return a Response object containing either a `MessageTask` (to show a message and close the dialog) or a `ContinueTask` (to show another dialog). Using just `Task` or `void` will compile but fail at runtime when the Teams client expects a Response object.
:::

## Basic Example
::: zone-end

::: zone pivot="python"
Dialogs have a specific `dialog_submit` event to handle submissions. When a user submits a form inside a dialog, the app is notified via this event, which is then handled to process the submission values, and can either send a response or proceed to more steps in the dialogs (see [Multi-step Dialogs](./handling-multi-step-forms.md)).
::: zone-end

::: zone pivot="typescript"
Dialogs have a specific `dialog.submit` event to handle submissions. When a user submits a form inside a dialog, the app is notified via this event, which is then handled to process the submission values, and can either send a response or proceed to more steps in the dialogs (see [Multi-step Dialogs](./handling-multi-step-forms.md)).
::: zone-end


In this example, we show how to handle dialog submissions from an Adaptive Card form:


::: zone pivot="csharp"
```csharp
using System.Text.Json;
using Microsoft.Teams.Api.TaskModules;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities.Invokes;
using Microsoft.Teams.Apps.Annotations;
using Microsoft.Teams.Common.Logging;

//...

[TaskSubmit]
public async Task<Microsoft.Teams.Api.TaskModules.Response> OnTaskSubmit([Context] Tasks.SubmitActivity activity, [Context] IContext.Client client, [Context] ILogger log)
{
    var data = activity.Value?.Data as JsonElement?;
    if (data == null)
    {
        log.Info("[TASK_SUBMIT] No data found in the activity value");
        return new Microsoft.Teams.Api.TaskModules.Response(
            new Microsoft.Teams.Api.TaskModules.MessageTask("No data found in the activity value"));
    }

    var submissionType = data.Value.TryGetProperty("submissiondialogtype", out var submissionTypeObj) && submissionTypeObj.ValueKind == JsonValueKind.String
        ? submissionTypeObj.ToString()
        : null;


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
        case "simple_form":
            var name = GetFormValue("name") ?? "Unknown";
            await client.Send($"Hi {name}, thanks for submitting the form!");
            return new Microsoft.Teams.Api.TaskModules.Response(
                new Microsoft.Teams.Api.TaskModules.MessageTask("Form was submitted"));
        // More examples below
        default:
            return new Microsoft.Teams.Api.TaskModules.Response(
                new Microsoft.Teams.Api.TaskModules.MessageTask("Unknown submission type"));
    }
}
```
::: zone-end

::: zone pivot="python"
```python
from typing import Optional, Any
from microsoft.teams.api import TaskSubmitInvokeActivity, TaskModuleResponse, TaskModuleMessageResponse
from microsoft.teams.apps import ActivityContext
# ...

@app.on_dialog_submit
async def handle_dialog_submit(ctx: ActivityContext[TaskSubmitInvokeActivity]):
    """Handle dialog submit events for all dialog types."""
    data: Optional[Any] = ctx.activity.value.data
    dialog_type = data.get("submissiondialogtype") if data else None

    if dialog_type == "simple_form":
        name = data.get("name") if data else None
        await ctx.send(f"Hi {name}, thanks for submitting the form!")
        return TaskModuleResponse(task=TaskModuleMessageResponse(value="Form was submitted"))
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
// ...

app.on('dialog.submit', async ({ activity, send, next }) => {
  const dialogType = activity.value.data?.submissiondialogtype;

  if (dialogType === 'simple_form') {
    // This is data from the form that was submitted
    const name = activity.value.data.name;
    await send(`Hi ${name}, thanks for submitting the form!`);
    return {
      task: {
        type: 'message',
        // This appears as a final message in the dialog
        value: 'Form was submitted',
      },
    };
  }
});
```
::: zone-end


Similarly, handling dialog submissions from rendered webpages is also possible:


::: zone pivot="csharp"
```csharp
// Add this case to the switch statement in OnTaskSubmit method
case "webpage_dialog":
    var webName = GetFormValue("name") ?? "Unknown";
    var email = GetFormValue("email") ?? "No email";
    await client.Send($"Hi {webName}, thanks for submitting the form! We got that your email is {email}");
    return new Microsoft.Teams.Api.TaskModules.Response(
        new Microsoft.Teams.Api.TaskModules.MessageTask("Form submitted successfully"));
```
::: zone-end

::: zone pivot="python"
```python
from typing import Optional, Any
from microsoft.teams.api import TaskSubmitInvokeActivity, InvokeResponse, TaskModuleResponse, TaskModuleMessageResponse
from microsoft.teams.apps import ActivityContext
# ...

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
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
// ...

// The submission from a webpage happens via the microsoftTeams.tasks.submitTask(formData)
// call.
app.on('dialog.submit', async ({ activity, send, next }) => {
  const dialogType = activity.value.data.submissiondialogtype;

  if (dialogType === 'webpage_dialog') {
    // This is data from the form that was submitted
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
### Complete TaskSubmit Handler Example

Here's the complete example showing how to handle multiple submission types:

```csharp
using System.Text.Json;
using Microsoft.Teams.Api.TaskModules;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.Activities.Invokes;
using Microsoft.Teams.Apps.Annotations;
using Microsoft.Teams.Common.Logging;

//...

[TaskSubmit]
public async Task<Microsoft.Teams.Api.TaskModules.Response> OnTaskSubmit([Context] Tasks.SubmitActivity activity, [Context] IContext.Client client, [Context] ILogger log)
{
    var data = activity.Value?.Data as JsonElement?;
    if (data == null)
    {
        log.Info("[TASK_SUBMIT] No data found in the activity value");
        return new Microsoft.Teams.Api.TaskModules.Response(
            new Microsoft.Teams.Api.TaskModules.MessageTask("No data found in the activity value"));
    }

    var submissionType = data.Value.TryGetProperty("submissiondialogtype", out var submissionTypeObj) && submissionTypeObj.ValueKind == JsonValueKind.String
        ? submissionTypeObj.ToString()
        : null;

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
        case "simple_form":
            var name = GetFormValue("name") ?? "Unknown";
            await client.Send($"Hi {name}, thanks for submitting the form!");
            return new Microsoft.Teams.Api.TaskModules.Response(
                new Microsoft.Teams.Api.TaskModules.MessageTask("Form was submitted"));

        case "webpage_dialog":
            var webName = GetFormValue("name") ?? "Unknown";
            var email = GetFormValue("email") ?? "No email";
            await client.Send($"Hi {webName}, thanks for submitting the form! We got that your email is {email}");
            return new Microsoft.Teams.Api.TaskModules.Response(
                new Microsoft.Teams.Api.TaskModules.MessageTask("Form submitted successfully"));

        default:
            return new Microsoft.Teams.Api.TaskModules.Response(
                new Microsoft.Teams.Api.TaskModules.MessageTask("Unknown submission type"));
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
