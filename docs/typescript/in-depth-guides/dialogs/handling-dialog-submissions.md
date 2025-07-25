---
title: Handling Dialog Submissions (preview) (TypeScript)
description: Handle dialog submissions using the Teams AI Library for TypeScript.
ms.topic: how-to
ms.date: 07/16/2025
---
# Handling Dialog Submissions (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

Dialogs have a specific `dialog.submit` event to handle submissions. When a user submits a form inside a dialog, the app is notified via this event, which is then handled to process the submission values, and can either send a response or proceed to more steps in the dialogs (see [Multi-step Dialogs](./handling-multi-step-forms.md)).

In this example, we show how to handle dialog submissions from an Adaptive Card form:

```ts
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

Similarly, handling dialog submissions from rendered webpages is also possible:

```ts
// The submission from a webpage happens via the microsoftTeams.tasks.submitTask(formData)
// call.
app.on('dialog.submit', async ({ activity, send, next }) => {
  const dialogType = activity.value.data.submissiondialogtype;

  if (dialogType === 'webpage_dialog') {
    // This is data from the form that was submitted
    const name = activity.value.data.name;
    const email = activity.value.data.email;
    await send(
      `Hi ${name}, thanks for submitting the form! We got that your email is ${email}`
    );
    // You can also return a blank response
    return {
      status: 200,
    };
  }

});
```