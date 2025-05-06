---
title: Activity - Adaptive Card Action Invoke (preview)
description: Learn about Activity - Adaptive Card Action Invoke (preview)
ms.topic: reference
ms.date: 05/05/2025
---

# Activity: Adaptive Card Action Invoke (preview)

[This article is prerelease documentation and is subject to change.]

The invoke `name` for Adaptive Cards is `adaptiveCard/action`. However, it is also possible to use the alias `card.action` to invoke an Adaptive Card.

<!-- langtabs-start -->
```typescript
// Short-hand form of invoking an Adaptive Card
app.on('card.action', async ({ activity }) => {});
```
<!-- langtabs-end -->

## Invoke value

The `Activity.value` field of the invoke activity for an Adaptive Card is `AdaptiveCardInvokeValue`. This structure of this type of invoke includes:

- `action`: `AdaptiveCardInvokeAction` - The action that was performed on the card.
- `authentication`: `AdaptiveCardAuthentication` - The authentication request for the card.
- `state`: `string` - magic code for OAuth.
- `trigger`: `'manual'` - what triggered the action.

## Resources

- [Microsoft Learn: `AdaptiveCardInvokeValue`](/javascript/api/botframework-schema/adaptivecardinvokevalue?view=botbuilder-ts-latest)