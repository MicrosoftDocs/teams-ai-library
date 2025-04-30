# Building Adaptive Cards

Adaptive Cards are JSON payloads that describe rich, interactive UI fragments.  
With `@microsoft/teams.cards` you can build these cards entirely in TypeScript / JavaScript while enjoying full IntelliSense and compiler safety.

---

## 1 The Builder Pattern

`@microsoft/teams.cards` exposes small **builder helpers** (`Card`, `TextBlock`, `ToggleInput`, `ExecuteAction`, _etc._).  
Each helper wraps raw JSON and provides fluent, chainable methods that keep your code concise and readable.

```ts
/**
 import {
  Card,
  TextBlock,
  ToggleInput,
  ExecuteAction,
  ActionSet,
} from "@microsoft/teams.cards";
*/

const card = new Card(
  new TextBlock('Hello world', { wrap: true, weight: 'bolder' }),
  new ToggleInput('Notify me').withId('notify'),
  new ActionSet(
    new ExecuteAction({ title: 'Submit' })
      .withData({ action: 'submit_basic' })
      .withAssociatedInputs('auto')
  )
);

```

Benefits:

| Benefit     | Description                                                                   |
| ----------- | ----------------------------------------------------------------------------- |
| Readability | No deep JSON trees—just chain simple methods.                                 |
| Re‑use      | Extract snippets to functions or classes and share across cards.              |
| Safety      | Builders validate every property against the Adaptive Card schema (see next). |

> Source code lives in `teams.ts/packages/cards/src/`. Feel free to inspect or extend the helpers for your own needs.

---

## 2 Type‑safe Authoring & IntelliSense

The package bundles the **Adaptive Card v1.5 schema** as strict TypeScript types.  
While coding you get:

- **Autocomplete** for every element and attribute.
- **In‑editor validation**—invalid enum values or missing required properties produce build errors.
- Automatic upgrades when the schema evolves; simply update the package.

```ts
// @ts-expect-error: "huge" is not a valid size for TextBlock
const textBlock = new TextBlock('Valid', { size: 'huge' });

```

---

## 3 The Visual Designer

Prefer a drag‑and‑drop approach? Use [Microsoft's Adaptive Card Designer](https://adaptivecards.microsoft.com/designer.html):

1. Add elements visually until the card looks right.
2. Copy the JSON payload from the editor pane.
3. Paste the JSON into your project **or** convert it to builder calls:

```ts
const cardJson = /* copied JSON */;
const card = new Card().withBody(cardJson);
```

```ts
const rawCard: ICard = {
  type: 'AdaptiveCard',
  body: [
    {
      text: 'Please fill out the below form to send a game purchase request.',
      wrap: true,
      type: 'TextBlock',
      style: 'heading',
    },
    {
      columns: [
        {
          width: 'stretch',
          items: [
            {
              choices: [
                { title: 'Call of Duty', value: 'call_of_duty' },
                { title: "Death's Door", value: 'deaths_door' },
                { title: 'Grand Theft Auto V', value: 'grand_theft' },
                { title: 'Minecraft', value: 'minecraft' },
              ],
              style: 'filtered',
              placeholder: 'Search for a game',
              id: 'choiceGameSingle',
              type: 'Input.ChoiceSet',
              label: 'Game:',
            },
          ],
          type: 'Column',
        },
      ],
      type: 'ColumnSet',
    },
  ],
  actions: [
    {
      title: 'Request purchase',
      type: 'Action.Execute',
      data: { action: 'purchase_item' },
    },
  ],
  version: '1.5',
};

```

This method leverages the full Adaptive Card schema and ensures that the payload adheres strictly to `ICard`.

> [!TIP]
> You can use a combination of raw JSON and builder helpers depending on whatever you find easier.

---

## 4 End‑to‑end Example – Task Form Card

Below is a complete example showing a task management form. Notice how the builder pattern keeps the file readable and maintainable:

```ts
app.on(
  'message',
  async ({
    send,
    activity,
  }) => {
    await send({ type: 'typing' });
    const card: ICard = new Card().withBody(new TextBlock(`Hello ${activity.from.name}`));

    await send(card);

    // Or send it with some text
    await send(new MessageActivity('Got your message!').addCard('adaptive', card));
  }
);

```

---

## 5 Additional Resources

- **Official Adaptive Card Documentation** — <https://adaptivecards.microsoft.com/>
- **Adaptive Cards Designer** — <https://adaptivecards.microsoft.com/designer.html>

---

### Summary

- Use **builder helpers** for readable, maintainable card code.
- Enjoy **full type safety** and IDE assistance.
- Prototype quickly in the **visual designer** and refine with builders.

Check out [this](https://github.com/microsoft/teams.ts/tree/main/samples/cards) sample demonstrating all the above features.

Happy card building! 🎉
