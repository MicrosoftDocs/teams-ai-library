---
title: Creating Dialogs (preview)
description: Learn about Creating Dialogs (preview)
ms.topic: how-to
ms.date: 05/05/2025
---

# Creating Dialogs (preview)

[This article is prerelease documentation and is subject to change.]

> [!TIP]
> If you're not familiar with how to build Adaptive Cards, check out [the cards guide](../cards/overview.md). Understanding their basics is a prerequisite for this guide.

## Entry Point

To open a dialog, you need to supply a special type of action as to the Adaptive Card. Once this button is clicked, the dialog will open and ask the application what to show.

<!-- langtabs-start -->
```typescript
app.on('message', async ({ send }) => {
  await send({ type: 'typing' });

  // Create the launcher adaptive card
  const card: ICard = new Card()
    .withBody({
      type: 'TextBlock',
      text: 'Select the examples you want to see!',
      size: 'large',
      weight: 'bolder',
    })
    .addActions(
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
<!-- langtabs-end -->

## Handling Dialog Open Events

Once an action is executed to open a dialog, the Teams client will send an event to the agent to request what the content of the dialog should be. Here is how to handle this event:

<!-- langtabs-start -->
```typescript
app.on('dialog.open', async ({ activity }) => {
  const card: ICard = new Card()...

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
<!-- langtabs-end -->

### Rendering A Card

You can render an Adaptive Card in a dialog by returning a card response.

<!-- langtabs-start -->
```typescript
if (dialogType === 'simple_form') {
  const dialogCard = new Card()
    .withBody(
      {
        type: 'TextBlock',
        text: 'This is a simple form',
        size: 'large',
        weight: 'bolder',
      },
      new TextInput()
        .withLabel('Name')
        .withRequired()
        .withId('name')
        .withPlaceholder('Enter your name')
    )
    // Inside the dialog, the card actions for submitting the card must be
    // of type Action.Submit
    .addActions(
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
<!-- langtabs-end -->

> [!IMPORTANT]
> The action type for submitting a dialog must be `Action.Submit`. This is a requirement of the Teams client. If you use a different action type, the dialog will not be submitted and the agent will not receive the submission event.

### Rendering A Webpage

You can render a webpage in a dialog as well. There are some security requirements to be aware of:

1. The webpage must be hosted on a domain that is allow-listed as `validDomains` in the Teams app [manifest](../../teams/manifest.md) for the agent
2. The webpage must also host the [teams-js client library](https://www.npmjs.com/package/@microsoft/teams-js). The reason for this is that for security purposes, the Teams client will not render arbitrary webpages. As such, the webpage must explicitly opt-in to being rendered in the Teams client. Setting up the teams-js client library handles this for you.

<!-- langtabs-start -->
```typescript
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
<!-- langtabs-end -->