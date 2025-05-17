---
title: Graph API Client (TypeScript)
description: Learn about Graph API Client (TypeScript)
ms.topic: how-to
ms.date: 05/17/2025
---

# Graph API Client (TypeScript)

[Microsoft Graph](/graph/overview) gives you access to the wider Microsoft 365 ecosystem. You can enrich your application with data from across Microsoft 365.

The library gives your application easy access to the Microsoft Graph API via the `@microsoft/teams.graph` package.

Microsoft Graph can be accessed by your application using its own application token, or by using the user's token. If you need access to resources that your application may not have, but your user does, you will need to use the user's scoped graph client. To grant explicit consent for your application to access resources on behalf of a user, follow the [auth guide](../in-depth-guides/user-authentication/overview.md).

To access the graph using the Graph using the app, you may use the `app.graph` object. 

```typescript
// Equivalent of /graph/api/user-get
// Gets the details of the bot-user
app.graph.me.get().then((user) => {
  console.log(`User ID: ${user.id}`);
  console.log(`User Display Name: ${user.displayName}`);
  console.log(`User Email: ${user.mail}`);
  console.log(`User Job Title: ${user.jobTitle}`);
});
```

To access the graph using the user's token, you need to do this as part of a message handler:

```typescript
app.on('message', async ({ activity, userGraph }) => {
  const me = await userGraph.me.get();
  console.log(`User ID: ${me.id}`);
  console.log(`User Display Name: ${me.displayName}`);
  console.log(`User Email: ${me.mail}`);
  console.log(`User Job Title: ${me.jobTitle}`);
});
```

Here, the `userGraph` object is a scoped graph client for the user that sent the message.

> [!TIP]
> You also have access to the `appGraph` object in the activity handler. This is equivalent to `app.graph`.

## The Graph Client

The Graph Client is a wrapper around the Microsoft Graph API. It provides a fluent API for accessing the Graph API and is scoped to a specific user or application. Having an understanding of [how the graph API works](/graph/use-the-api) will help you make the most of the library. Microsoft Graph exposes resources using the OData standard, and the graph client exposes type-safe access to these resources.

For example, to get the `id` of the chat instance between a user and an app, [Microsoft Graph](/graph/api/userscopeteamsappinstallation-get-chat) exposes it via:

```
GET /users/{user-id | user-principal-name}/teamwork/installedApps/{app-installation-id}/chat
```

The equivalent using the graph client would look like this:

```ts
const chat = await userGraph.teamwork(user.id).installedApps.chat(appInstallationId).get({
  "user-id": user.id,
  "userScopeTeamsAppInstallation-id": appInstallationId,
  "$select": ["id"],
})
```

Here, the client takes care of using the correct token, provides helpful hints via intellisense, and performs the fetch request for you.

## Currently exposed Graph clients

The following clients are currently exposed:

| Client Name | Graph endpoint | Description |
|-------------|----------------|-------------|
| appCatalogs | [/appCatalogs](/graph/api/appcatalogs-list-teamsapps) | Apps from Teams App Catalog |
| appRoleAssignments | [/appRoleAssignments](/graph/api/serviceprincipal-list-approleassignments) | List app role assignments |
| applicationTemplates | [/applicationTemplates](/graph/api/resources/applicationtemplate) | Application in the Microsoft Entra App Gallery |
| applications | [/applications](/graph/api/resources/application) | Application Resources |
| chats | [/chats](/graph/api/chat-list) | Chat resources between users |
| communications | [/communications](/graph/api/application-post-calls) | Calls and Online meetings |
| employeeExperience | [/employeeExperience](/graph/api/resources/engagement-api-overview) |  Employee Experience and Engagement |
| me | [/me](/graph/api/user-get) | Same as `/users` but scoped to one user (who is making the request) |
| teams | [/teams](/graph/api/resources/team) | A Team resource  |
| teamsTemplates | [/teamsTemplates](/microsoftteams/get-started-with-teams-templates) | A Team Template resource |
| teamwork | [/teamwork](/graph/api/resources/teamwork) | A range of Microsoft Teams functionalities |
| users | [/users](/graph/api/resources/users) | A user resource |