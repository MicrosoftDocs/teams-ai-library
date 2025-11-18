---
title: User Authentication
description: API guide to implement User Authentication with SSO in Teams Apps.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 11/17/2025
---

# User Authentication

At times agents must access secured online resources on behalf of the user, such as checking email, checking on flight status, or placing an order. To enable this, the user must authenticate their identity and grant consent for the application to access these resources. This process results in the application receiving a token, which the application can then use to access the permitted resources on the user's behalf.

> [!NOTE]
> This is an advanced guide. It is highly recommended that you are familiar with [Teams Core Concepts](../teams/core-concepts.md) before attempting this guide.

> [!WARNING]
> User authentication does not work with the developer tools setup. You have to run the app in Teams. Follow these [instructions](../getting-started/running-in-teams/overview.md#debugging-in-teams) to run your app in Teams.

> [!NOTE]
> It is possible to authenticate the user into [other auth providers](/azure/bot-service/bot-builder-concept-identity-providers#other-identity-providers) like Facebook, Github, Google, Dropbox, and so on.

Once you have configured your Azure Bot resource OAuth settings, as described in the [official documentation](/azure/bot-service/bot-builder-concept-authentication), add the following code to your `App`:

## Project Setup

### Create an app with the `graph` template

> [!TIP]
> Skip this step if you want to add the auth configurations to an existing app.


::: zone pivot="csharp"
Use your terminal to run the following command:

```sh
npx @microsoft/teams.cli@latest new csharp oauth-app --template graph
```
::: zone-end

::: zone pivot="python"
Use your terminal to run the following command:

```sh
npx @microsoft/teams.cli@latest new python oauth-app --template graph
```

This command:

1. Creates a new directory called `oauth-app`.
2. Bootstraps the graph agent template files into it under `oauth-app/src`.
3. Creates your agent's manifest files, including a `manifest.json` file and placeholder icons in the `oauth-app/appPackage` directory.
::: zone-end

::: zone pivot="typescript"
Use your terminal to run the following command:

```sh
npx @microsoft/teams.cli@latest new typescript oauth-app --template graph
```

This command:

1. Creates a new directory called `oauth-app`.
2. Bootstraps the graph agent template files into it under `oauth-app/src`.
3. Creates your agent's manifest files, including a `manifest.json` file and placeholder icons in the `oauth-app/appPackage` directory.
::: zone-end


### Add Agents Toolkit auth configuration

Open your terminal with the project folder set as the current working directory and run the following command:

```sh
npx @microsoft/teams.cli config add atk.oauth
```

The `atk.oauth` configuration is a basic setup for Agents Toolkit along with configurations to authenticate the user with Microsoft Entra ID to access Microsoft Graph APIs.

This [CLI](/developer-tools/cli) command adds configuration files required by Agents Toolkit, including:

- Azure Application Entra ID manifest file `aad.manifest.json`.
- Azure bicep files to provision Azure bot in `infra/` folder.

> [!NOTE]
> Agents Toolkit, in the debugging flow, will deploy the `aad.manifest.json` and `infra/azure.local.bicep` file to provision the Application Entra ID and Azure bot with oauth configurations.

## Configure the OAuth connection


::: zone pivot="csharp"
```cs
var builder = WebApplication.CreateBuilder(args);

var appBuilder = App.Builder()
    .AddOAuth("graph");

builder.AddTeams(appBuilder);
var app = builder.Build();
var teams = app.UseTeams();
```
::: zone-end

::: zone pivot="python"
```python
from teams import App
from teams.api import MessageActivity, SignInEvent
from teams.apps import ActivityContext
from teams.logger import ConsoleLogger, ConsoleLoggerOptions

app = App(
    # The name of the auth connection to use.
    # It should be the same as the Oauth connection name defined in the Azure Bot configuration.
    default_connection_name="graph",
    logger=ConsoleLogger().create_logger("auth", options=ConsoleLoggerOptions(level="debug")))
```
::: zone-end

::: zone pivot="typescript"
```ts
import { App } from '@microsoft/teams.apps';
import * as endpoints from '@microsoft/teams.graph-endpoints';

const app = new App({
  oauth: {
    defaultConnectionName: 'graph',
  },
});
```
::: zone-end


> [!TIP]
> Make sure you use the same name you used when creating the OAuth connection in the Azure Bot Service resource.

> [!NOTE]
> In many templates, `graph` is the default name of the OAuth connection, but you can change that by supplying a different connection name in your app configuration.

## Signing In

> [!NOTE]
> This uses the Single Sign-On (SSO) authentication flow. To learn more about all the available flows and their differences see the [official documentation](/azure/bot-service/bot-builder-concept-authentication).

You must call the `signin` method inside your route handler, for example: to signin when receiving the `/signin` message:


::: zone pivot="csharp"
```cs
teams.OnMessage("/signin", async context =>
{
    if (context.IsSignedIn)
    {
        await context.Send("you are already signed in!");
        return;
    }
    else
    {
        await context.SignIn();
    }
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_signin_message(ctx: ActivityContext[MessageActivity]):
    """Handle message activities for signing in."""
    ctx.logger.info("User requested sign-in.")
    if ctx.is_signed_in:
        await ctx.send("You are already signed in.")
    else:
        await ctx.sign_in()
```
::: zone-end

::: zone pivot="typescript"
```ts
app.message('/signin', async ({ send, signin, isSignedIn }) => {
  if (isSignedIn) {
    send('you are already signed in!');
  } else {
    await signin();
  }
});
```
::: zone-end


## Subscribe to the SignIn event

You can subscribe to the `signin` event, that will be triggered once the OAuth flow completes.


::: zone pivot="csharp"
```cs
teams.OnSignIn(async (_, teamsEvent) =>
{
    var context = teamsEvent.Context;
    await context.Send($"Signed in using OAuth connection {context.ConnectionName}. Please type **/whoami** to see your profile or **/signout** to sign out.");
});
```
::: zone-end

::: zone pivot="python"
```python
@app.event("sign_in")
async def handle_sign_in(event: SignInEvent):
    """Handle sign-in events."""
    await event.activity_ctx.send("You are now signed in!")
```
::: zone-end

::: zone pivot="typescript"
```ts
app.event('signin', async ({ send, token }) => {
  await send(
    `Signed in using OAuth connection ${token.connectionName}. Please type **/whoami** to see your profile or **/signout** to sign out.`
  );
});
```
::: zone-end


## Start using the graph client

From this point, you can use the `IsSignedIn` flag and the `userGraph` client to query graph, for example to reply to the `/whoami` message, or in any other route.

> [!NOTE]
> The default OAuth configuration requests the `User.ReadBasic.All` permission. It is possible to request other permissions by modifying the App Registration for the bot on Azure.


::: zone pivot="csharp"
```cs
teams.OnMessage("/whoami", async context =>
{
    if (!context.IsSignedIn)
    {
        await context.Send("you are not signed in!. Please type **/signin** to sign in");
        return;
    }
    var me = await context.GetUserGraphClient().Me.GetAsync();
    await context.Send($"user \"{me!.DisplayName}\" signed in.");
});

teams.OnMessage(async context =>
{
    if (context.IsSignedIn)
    {
        await context.Send($"You said : {context.Activity.Text}.  Please type **/whoami** to see your profile or **/signout** to sign out.");
    }
    else
    {
        await context.Send($"You said : {context.Activity.Text}.  Please type **/signin** to sign in.");
    }
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_whoami_message(ctx: ActivityContext[MessageActivity]):
    """Handle messages to show user information from Microsoft Graph."""
    if not ctx.is_signed_in:
        await ctx.send("You are not signed in! Please sign in to continue.")
        return

    # Access user's Microsoft Graph data
    me = await ctx.user_graph.me.get()
    await ctx.send(f"Hello {me.display_name}! Your email is {me.mail or me.user_principal_name}")

@app.on_message
async def handle_all_messages(ctx: ActivityContext[MessageActivity]):
    """Handle all other messages."""
    if ctx.is_signed_in:
        await ctx.send(f'You said: "{ctx.activity.text}". Please type **/whoami** to see your profile or **/signout** to sign out.')
    else:
        await ctx.send(f'You said: "{ctx.activity.text}". Please type **/signin** to sign in.')
```
::: zone-end

::: zone pivot="typescript"
```ts
import * as endpoints from '@microsoft/teams.graph-endpoints';

app.message('/whoami', async ({ send, userGraph, isSignedIn }) => {
  if (!isSignedIn) {
    await send('you are not signed in! please type **/signin** to sign in.');
    return;
  }
  const me = await userGraph.call(endpoints.me.get);
  await send(
    `you are signed in as "${me.displayName}" and your email is "${me.mail || me.userPrincipalName}"`
  );
});

app.on('message', async ({ send, activity, isSignedIn }) => {
  if (isSignedIn) {
    await send(
      `You said: "${activity.text}". Please type **/whoami** to see your profile or **/signout** to sign out.`
    );
  } else {
    await send(`You said: "${activity.text}". Please type **/signin** to sign in.`);
  }
});
```
::: zone-end


## Signing Out

You can signout by calling the `signout` method, this will remove the token from the User Token service cache


::: zone pivot="csharp"
```cs
teams.OnMessage("/signout", async context =>
{
    if (!context.IsSignedIn)
    {
        await context.Send("you are not signed in!");
        return;
    }

    await context.SignOut();
    await context.Send("you have been signed out!");
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_signout_message(ctx: ActivityContext[MessageActivity]):
    """Handle sign out requests."""
    if not ctx.is_signed_in:
        await ctx.send("You are not signed in!")
        return

    await ctx.sign_out()
    await ctx.send("You have been signed out!")
```
::: zone-end

::: zone pivot="typescript"
```ts
app.message('/signout', async ({ send, signout, isSignedIn }) => {
  if (!isSignedIn) {
    await send('you are not signed in! please type **/signin** to sign in.');
    return;
  }
  await signout(); // call signout for your auth connection...
  await send('you have been signed out!');
});
```
::: zone-end


## Resources

[User Authentication Basics](/azure/bot-service/bot-builder-concept-authentication)
