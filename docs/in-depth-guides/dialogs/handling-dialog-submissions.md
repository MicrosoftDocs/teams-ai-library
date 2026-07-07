---
title: 'Handling Dialog Submissions'
description: 'Guide to processing dialog submissions in Teams applications, showing how to handle form data from both Adaptive Cards and web pages using dialog submission event handlers.'
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 06/29/2026
---

# Handling Dialog Submissions


::: zone pivot="csharp"
Dialogs have a specific `TaskSubmit` event to handle submissions. When a user submits a form inside a dialog, the app is notified via this event, which is then handled to process the submission values, and can either send a response or proceed to more steps in the dialogs (see [Multi-step Dialogs](./handling-multi-step-forms.md)).

> [!WARNING]
>
> Return Type Requirement
> Methods decorated with `[TaskSubmit]` **must** return `Task<Microsoft.Teams.Api.TaskModules.Response>`. Every code path must return a Response object containing either a `MessageTask` (to show a message and close the dialog) or a `ContinueTask` (to show another dialog). Using just `Task` or `void` will compile but fail at runtime when the Teams client expects a Response object.

## Basic Example
::: zone-end

::: zone pivot="python"
When a user submits a form inside a dialog, your app receives a `dialog_submit` event. Use `@app.on_dialog_submit("action")` to handle a specific submission (where `action` matches the value passed via `SubmitData`), or `@app.on_dialog_submit()` for a catch-all. You can either send a response or proceed to more steps in the dialog (see [Multi-step Dialogs](./handling-multi-step-forms.md)).
::: zone-end

::: zone pivot="typescript"
When a user submits a form inside a dialog, your app receives a `dialog.submit` event. Use `dialog.submit.<action>` to handle a specific submission (where `action` matches the value passed via `SubmitData`), or `dialog.submit` for a catch-all. You can either send a response or proceed to more steps in the dialog (see [Multi-step Dialogs](./handling-multi-step-forms.md)).
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
from microsoft_teams.api import TaskSubmitInvokeActivity, TaskModuleResponse, TaskModuleMessageResponse
from microsoft_teams.apps import ActivityContext
# ...

# The "action" field in SubmitData("simple_form") routes here
@app.on_dialog_submit("simple_form")
async def handle_simple_form_submit(ctx: ActivityContext[TaskSubmitInvokeActivity]):
    data = ctx.activity.value.data
    name = data.get("name")
    await ctx.send(f"Hi {name}, thanks for submitting the form!")
    return TaskModuleResponse(task=TaskModuleMessageResponse(value="Form was submitted"))
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
// ...

// The "action" field in SubmitData('simple_form') routes here
app.on('dialog.submit.simple_form', async ({ activity, send }) => {
  const name = activity.value.data.name;
  await send(`Hi ${name}, thanks for submitting the form!`);
  return {
    task: {
      type: 'message',
      // This appears as a final message in the dialog
      value: 'Form was submitted',
    },
  };
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
from microsoft_teams.api import TaskSubmitInvokeActivity, TaskModuleResponse, TaskModuleMessageResponse
from microsoft_teams.apps import ActivityContext
# ...

# Webpage submissions route the same way — the webpage must include
# the "action" field in the data passed to microsoftTeams.dialog.url.submit()
@app.on_dialog_submit("webpage_dialog")
async def handle_webpage_dialog_submit(ctx: ActivityContext[TaskSubmitInvokeActivity]):
    data = ctx.activity.value.data
    name = data.get("name")
    email = data.get("email")
    await ctx.send(f"Hi {name}, thanks for submitting the form! We got that your email is {email}")
    return TaskModuleResponse(task=TaskModuleMessageResponse(value="Form submitted successfully"))
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
// ...

// Webpage submissions route the same way — the webpage must include
// the "action" field in the data passed to microsoftTeams.tasks.submitTask()
app.on('dialog.submit.webpage_dialog', async ({ activity, send }) => {
  const name = activity.value.data.name;
  const email = activity.value.data.email;
  await send(`Hi ${name}, thanks for submitting the form! We got that your email is ${email}`);
  // Return status 200 to close the dialog without showing a message
  return {
    status: 200,
  };
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


