---
title: Activity - Adaptive Card Invoke
description: Activity - Adaptive Card Invoke
ms.topic: how-to
ms.date: 05/15/2025
---

# Activity: Adaptive Card Invoke

[Adaptive Cards](/microsoftteams/platform/task-modules-and-cards/cards/cards-reference#adaptive-card) are a way to send rich content to users. They can be used to send messages, notifications, or to display information.

Invokes on Adaptive Cards are used to perform some action dependent on interaction from the user.

```
    // Long-hand form of retrieving the invoke value
    app.on('invoke', async ({ activity }) > {
        if (activity.name  'adaptiveCard/action') {
            const { action }  activity.value;
        }
    });
```

The name of the invoke activity for Adaptive Cards is `adaptiveCard/action`. However, the `@microsoft/teams.api` package includes an alias for this invoke activity, `card.action`.

See the next section for more information on the `value` field of the invoke activity.

### Resources

*   [Microsoft Learn: AC invokes](/microsoftteams/platform/task-modules-and-cards/cards/cards-actions?tabsjson#action-type-invoke)

## Activity: Adaptive Card Action Invoke

The invoke `name` for Adaptive Cards is `adaptiveCard/action`. However, it is also possible to use the alias `card.action` to invoke an adaptive card.

```
    // Short-hand form of invoking an adaptive card
    app.on('card.action', async ({ activity }) > {});
```

### Invoke value

The `Activity.value` field of the invoke activity for an Adaptive Card is `AdaptiveCardInvokeValue`. This structure of this type of invoke includes:

*   `action`: `AdaptiveCardInvokeAction` - The action that was performed on the card.
*   `authentication`: `AdaptiveCardAuthentication` - The authentication request for the card.
*   `state`: `string` - magic code for OAuth.
*   `trigger`: `'manual'` - what triggered the action.

### Resources

*   [Microsoft Learn: `AdaptiveCardInvokeValue`](https://learn.microsoft.com/en-us/javascript/api/botframework-schema/adaptivecardinvokevalue?viewbotbuilder-ts-latest)
