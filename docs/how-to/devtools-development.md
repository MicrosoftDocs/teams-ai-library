---
title: Devtools development
description: Devtools development
ms.topic: how-to
ms.date: 05/15/2025
---

# Devtools development


If you are making contributions to the devtools package, there are a few shortcuts that will help develop faster.

## Default send message

When in development mode, setting `VITE_DEV_MESSAGE` will send a message from the user on first render of the chat window. There is a delay of 1 second before sending to give the page the chance to render.

> .env file of `/packages/devtools`:

```
    NODE_ENVdevelopment
    LOG*
    VITE_DEV_MESSAGE"hi there"
    

```
![Automatically sent message](../assets/screenshots/devtools-default-send.png?rawtrue)

Clicking on the Teams icon in the upper left corner will refresh the page, bring you back to the Chat screen, and send the first message.

If you want to explore this functionality, see the `dev` utils in the devtools package.