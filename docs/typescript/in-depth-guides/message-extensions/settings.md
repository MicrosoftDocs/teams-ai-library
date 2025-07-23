---
title: Settings (preview) (TypeScript)
description: Learn about Settings (preview) (TypeScript)
ms.topic: how-to
ms.date: 07/16/2025
---

# Settings (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

You can add a settings page that allows users to configure settings for your app.

The user can access the settings by right-clicking the app item in the compose box

:::image type="content" source="~/assets/screenshots/settings.png" alt-text="Settings control":::

This guide will show how to enable user access to settings, as well as setting up a page that looks like this:

:::image type="content" source="~/assets/screenshots/settings-page.png" alt-text="Settings Page":::

## 1. Update the Teams Manifest

Set the `canUpdateConfiguration` field to `true` in the desired message extension under `composeExtensions`.

```json
"composeExtensions": [
    {
        "botId": "${{BOT_ID}}",
        "canUpdateConfiguration": true,
        ...
    }
]
```

## 2. Serve the settings `html` page

This is the code snippet for the settings `html` page:

<FileCodeBlock
    lang="html"
    src="/generated-snippets/ts/index.snippet.message-ext-settings-page.html"
/>

Save it in the `index.html` file in the same folder as where your app is initialized.

You can serve it by adding the following code to your app:

```ts
app.tab('settings', path.resolve(__dirname));
```

> [!NOTE]
> This will serve the HTML page to the `${BOT_ENDPOINT}/tabs/settings` endpoint as a tab. See [Tabs Guide](../tabs/overview.md) to learn more.

## 3. Specify the URL to the settings page

To enable the settings page, your app needs to handle the `message.ext.query-settings-url` activity that Teams sends when a user right-clicks the app in the compose box. Your app must respond with the URL to your settings page. Here's how to implement this:

```ts
app.on('message.ext.query-settings-url', async ({ activity }) => {
  // Get user settings from storage if available
  const userSettings = await app.storage.get(activity.from.id) || { selectedOption: '' };
  const escapedSelectedOption = encodeURIComponent(userSettings.selectedOption);

  return {
    composeExtension: {
      type: 'config',
      suggestedActions: {
        actions: [
          {
            type: 'openUrl',
            title: 'Settings',
            // ensure the bot endpoint is set in the environment variables
            // process.env.BOT_ENDPOINT is not populated by default in the Teams Toolkit setup. 
            value: `${process.env.BOT_ENDPOINT}/tabs/settings?selectedOption=${escapedSelectedOption}`
          }
        ]
      }
    }
  };
});
```

## 4. Handle Form Submission

When a user submits the settings form, Teams sends a `message.ext.setting` activity with the selected option in the `activity.value.state` property. Handle it to save the user's selection:

```ts
app.on('message.ext.setting', async ({ activity, send }) => {
  const { state } = activity.value;
  if (state == 'CancelledByUser') {
    return {
      status: 400
    };
  }
  const selectedOption = state;
  
  // Save the selected option to storage
  await app.storage.set(activity.from.id, { selectedOption });
  
  await send(`Selected option: ${selectedOption}`);

  return {
    status: 200
  };
});
```