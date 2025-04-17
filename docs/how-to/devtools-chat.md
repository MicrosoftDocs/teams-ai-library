---
title: Devtools Chat
description: Devtools Chat
ms.topic: how-to
ms.date: 05/15/2025
---

# Devtools Chat


![Blank Devtools chat](../assets/images/devtools_blank_chat.png?rawtrue) Chat with your app the same way you would in teams

Chat with your app the same way you would in teams without the need for an app id or authentication. This is useful for testing and debugging your app. You can also use this feature to test your app in different environments, such as production or staging. As time goes on, we plan to add more features to devtools that will allow a wider variety of testing.

## Getting Started

You can use the devtools package as a plugin for your app.

### Installation

Add the package to your Teams app.

```
    $: npm install @microsoft/teams.devtools
    

```
### Usage

In your app's main file, make sure DevTools plugin is added to the app.

```
    import { App } from '@microsoft/teams.apps';
    import { ConsoleLogger } from '@microsoft/teams.common/logging';
    import { DevtoolsPlugin } from '@microsoft/teams.dev';
    //... Other imports here
    const app  new App({
        logger: new ConsoleLogger('@samples/echo', { level: 'debug' }),
        plugins: [new DevtoolsPlugin()],
    });
    

```
When you run your app, for example `npm run dev`, devtools will be running on port 3001

```
    [nodemon] watching extensions: ts
    [nodemon] starting `node -r ts-node/register -r dotenv/config ./src/index.ts`
    [INFO] @samples/echo/http listening on port 3000 🚀
    [INFO] @samples/echo/devtools available at http://localhost:3001/devtools
    

```
When you open the page, you will see a Teams-like chat window and you can immediately talk to your app.

![Devtools chat](../assets/images/devtools_with_chat.png?rawtrue)

### Developer tools

For an easier debugging experience, we have added a features to the compose box that will store the last five messages sent to the app. To access this, simply press ↑ in the compose box and you can cycle through your message history and send that message.

![Devtools Up Arrow Feature](../assets/images/devtools_uparrow_feature.gif?rawtrue)

## Available features

*   **Send messages**: You can send messages to your app just like you would in Teams. The app will respond to the message and you can see the response in the chat window.
*   **Message reactions** : You can react to messages in the chat window. This is useful for testing how your app handles reactions and/or examining the reactions payload.

![Devtools Up Arrow Feature](../assets/images/devtools_message_reaction.gif?rawtrue)