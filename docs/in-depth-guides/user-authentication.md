---
title: User Authentication Concepts
description: API guide to implement User Authentication with SSO in Teams Apps.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---

# User Authentication Concepts

At times agents must access secured online resources on behalf of the user, such as checking email, checking on flight status, or placing an order. To enable this, the user must authenticate their identity and grant consent for the application to access these resources. This process results in the application receiving a token, which the application can then use to access the permitted resources on the user's behalf.

> [!NOTE]
> This is an advanced guide. It is highly recommended that you are familiar with [Teams Core Concepts](../teams/core-concepts.md) before attempting this guide.

> [!WARNING]
> User authentication does not work with the developer tools setup. You have to run the app in Teams. Follow [Quickstart: Register your app](../get-started/quickstart-register.md) to register and sideload your bot.

> [!NOTE]
> It is possible to authenticate the user into [other auth providers](/azure/bot-service/bot-builder-concept-identity-providers?tabs=adv2%2Cga2#other-identity-providers) like Facebook, Github, Google, Dropbox, and so on.


::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
## Project Setup

> [!TIP]
> If you're creating a new app, use the `graph` template. Skip this if you're adding auth to an existing app.

Use your terminal to run the following command:

```sh
teams project new python oauth-app --template graph
```

This command:

1. Creates a new directory called `oauth-app`.
2. Bootstraps the graph agent template files into it under `oauth-app/src`.
::: zone-end

::: zone pivot="typescript"
## Project Setup

> [!TIP]
> If you're creating a new app, use the `graph` template. Skip this if you're adding auth to an existing app.

Use your terminal to run the following command:

```sh
teams project new typescript oauth-app --template graph
```

This command:

1. Creates a new directory called `oauth-app`.
2. Bootstraps the graph agent template files into it under `oauth-app/src`.
::: zone-end


### Set up the OAuth connection

User authentication requires an **Azure-managed bot** (Teams-managed bots don't support OAuth connections). If you registered with `--teams-managed`, migrate first:

```sh
teams app bot migrate <appId> --subscription <id> --resource-group <your-resource-group>
```

Then follow the [SSO Setup guide](../teams/user-authentication/sso-setup.md) to configure the AAD app, create the Azure Bot OAuth connection, and update the manifest. The guide covers both SSO (silent token exchange) and generic OAuth.

> [!TIP]
> If you'd rather have an AI coding assistant run the setup, install the [`teams-dev` skill](../developer-tools/agent-skills.md) and ask it to "set up SSO for my Teams bot".

## Configure the OAuth connection


::: zone pivot="csharp"

# [SDK 2.0 (Legacy)](#tab/legacy)
```csharp
using Microsoft.Teams.Apps;
using Microsoft.Teams.Plugins.AspNetCore.Extensions;

var builder = WebApplication.CreateBuilder(args);

var appBuilder = App.Builder()
    .AddOAuth("graph"); // default connection

builder.AddTeams(appBuilder);
var app = builder.Build();
var teams = app.UseTeams();
```

---

# [SDK 2.1 (current)](#tab/core)
> [!NOTE]
> In SDK 2.1, you can register and use multiple OAuth connections in one bot (for example, Graph + GitHub) by adding multiple `AddOAuthFlow(...)` entries.

```csharp
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.OAuth;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddTeamsBotApplication(options =>
{
    options.AddOAuthFlow("graph", oauth =>
    {
        oauth.OAuthCardText = "Sign in to Microsoft Graph";
        oauth.SignInButtonText = "Sign in to Graph";
    });
    options.AddOAuthFlow("github", oauth =>
    {
        oauth.OAuthCardText = "Sign in to GitHub";
        oauth.SignInButtonText = "Sign in to GitHub";
    });
});

var app = builder.Build();
var teams = app.UseTeamsBotApplication();

OAuthFlow graphAuth = teams.GetOAuthFlow("graph");
OAuthFlow githubAuth = teams.GetOAuthFlow("github");
```
::: zone-end

::: zone pivot="python"

# [SDK 2.0 (Legacy)](#tab/legacy)
```python
from microsoft_teams.apps import App

app = App(
    # The name of the auth connection to use.
    # It should be the same as the OAuth connection name defined in the Azure Bot configuration.
    default_connection_name="graph",
)
```

---

# [SDK 2.1 (current)](#tab/core)
Register the connections you plan to use. `add_oauth_flow` returns the object that owns one.

```python
from microsoft_teams.apps import App

app = App()

graph = app.add_oauth_flow(
    "graph",
    oauth_card_text="Sign in to your account",
    sign_in_button_text="Sign in",
)
```

Both card options are optional. Use `app.get_oauth_flow("graph")` to get the flow again from another module.

> [!NOTE]
> Registering a flow enables per-turn state unless you set `state` yourself, so sign-in callbacks that don't name a connection can be traced back to the one that started them.

::: zone-end

::: zone pivot="typescript"

# [SDK 2.0 (Legacy)](#tab/legacy)
```ts
import { App } from '@microsoft/teams.apps';

const app = new App({
  oauth: {
    // The name of the auth connection to use.
    // It should be the same as the OAuth connection name defined in the Azure Bot configuration.
    defaultConnectionName: 'graph',
  },
});
```

---

# [SDK 2.1 (current)](#tab/core)
Register the connections you plan to use. `addOAuthFlow` returns the object that owns one.

```ts
import { App } from '@microsoft/teams.apps';

const app = new App();

// Or register up front: new App({ oauthFlows: ['graph'] })
const graph = app.addOAuthFlow('graph', {
  oauthCardText: 'Sign in to your account',
  signInButtonText: 'Sign in',
});
```

Both card options are optional. Use `app.getOAuthFlow('graph')` to get the flow again from another module.

> [!NOTE]
> Registering a flow enables per-turn state unless you set `state` yourself, so sign-in callbacks that don't name a connection can be traced back to the one that started them. `oauth.defaultConnectionName` can't be combined with registered flows.

::: zone-end


> [!TIP]
> Make sure you use the same name you used when creating the OAuth connection in the Azure Bot Service resource.


> [!NOTE]
> In many templates, `graph` is the default name of the OAuth connection, but you can register the connection under any name — it just has to match the OAuth connection configured on the Azure Bot.


## Signing In

Start sign-in from inside a route handler, for example when receiving the `/signin` message:


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
> [!NOTE]
> This uses the Single Sign-On (SSO) authentication flow. To learn more about all the available flows and their differences see the [official documentation](/azure/bot-service/bot-builder-concept-authentication).

```csharp
teams.OnMessage("/signin", async (context, cancellationToken) =>
{
    if (context.IsSignedIn)
    {
        await context.Send("you are already signed in!", cancellationToken);
        return;
    }

    await context.SignIn(new OAuthOptions
    {
        ConnectionName = "graph",
        OAuthCardText = "Sign in to your account",
        SignInButtonText = "Sign in"
    }, cancellationToken);
});
```

---

# [SDK 2.1 (current)](#tab/core)
Call `SignInAsync` on the flow directly — each flow manages its own sign-in state independently.

  > [!NOTE]
  > The graph connection uses the Single Sign-On (SSO) authentication flow whereas the Github connection uses the oauth flow. To learn more about all the available flows and their differences see the [official documentation](/azure/bot-service/bot-builder-concept-authentication).

```csharp
teams.OnMessage("/signin graph", async (context, cancellationToken) =>
{
    string? token = await graphAuth.SignInAsync(context, cancellationToken);
    if (token is not null)
    {
        await context.SendAsync("you are already signed in to Graph!", cancellationToken);
    }
});

teams.OnMessage("/signin github", async (context, cancellationToken) =>
{
    string? token = await githubAuth.SignInAsync(context, cancellationToken);
    if (token is not null)
    {
        await context.SendAsync("you are already signed in to GitHub!", cancellationToken);
    }
});
```
::: zone-end

::: zone pivot="python"
> [!NOTE]
> This uses the Single Sign-On (SSO) authentication flow. To learn more about all the available flows and their differences see the [official documentation](/azure/bot-service/bot-builder-concept-authentication).

# [SDK 2.0 (Legacy)](#tab/legacy)
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

---

# [SDK 2.1 (current)](#tab/core)
```python
@app.on_message_pattern("/signin")
async def handle_signin_message(ctx: ActivityContext[MessageActivity]):
    """Handle message activities for signing in."""
    token = await graph.sign_in(ctx)
    if token:
        await ctx.send("You are already signed in.")
```
::: zone-end

::: zone pivot="typescript"
> [!NOTE]
> This uses the Single Sign-On (SSO) authentication flow. To learn more about all the available flows and their differences see the [official documentation](/azure/bot-service/bot-builder-concept-authentication).

# [SDK 2.0 (Legacy)](#tab/legacy)
```ts
app.message('/signin', async ({ signin, send }) => {
  if (await signin()) {
    await send('you are already signed in!');
  }
});
```

---

# [SDK 2.1 (current)](#tab/core)
```ts
app.message('/signin', async (ctx) => {
  const token = await graph.signIn(ctx);
  if (token) {
    await ctx.send('you are already signed in!');
  }
});
```
::: zone-end


## Handling sign-in completion

The sign-in method returns a token when the user already has one, and otherwise sends an OAuth card and returns nothing. The flow finishes on a later turn, so completion is delivered through a callback.


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
```csharp
teams.OnSignIn(async (_, teamsEvent, cancellationToken) =>
{
    var context = teamsEvent.Context;
    await context.Send(
        $"Signed in using OAuth connection {context.ConnectionName}. Please type **/whoami** to see your profile or **/signout** to sign out.",
        cancellationToken);
});
```

---

# [SDK 2.1 (current)](#tab/core)
Success and failure callbacks are scoped per flow — no branching on connection name needed.
```csharp
graphAuth.OnSignInComplete(async (context, tokenResponse, cancellationToken) =>
{
    await context.SendAsync(
        $"Signed in to Graph ({tokenResponse.ConnectionName}). Type **/whoami** to continue.",
        cancellationToken);
});

githubAuth.OnSignInComplete(async (context, tokenResponse, cancellationToken) =>
{
    await context.SendAsync(
        $"Signed in to GitHub ({tokenResponse.ConnectionName}).",
        cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
# [SDK 2.0 (Legacy)](#tab/legacy)
```python
@app.event("sign_in")
async def handle_sign_in(event: SignInEvent):
    """Handle sign-in events."""
    await event.activity_ctx.send("You are now signed in!")
```

---

# [SDK 2.1 (current)](#tab/core)
The handler is scoped to its connection, so there's no need to branch on the connection name.

```python
@graph.on_signin
async def on_graph_signin(event: SignInEvent):
    """Only fires for the `graph` connection."""
    await event.activity_ctx.send(
        f"Signed in on {event.connection_name}. "
        "Type **/whoami** to see your profile or **/signout** to sign out."
    )
```

> [!NOTE]
> A flow can have more than one handler. They run in registration order and are isolated — if one raises, the error is logged and the rest still run. The app-wide `sign_in` event also still fires for every connection.

::: zone-end

::: zone pivot="typescript"
# [SDK 2.0 (Legacy)](#tab/legacy)
```ts
app.event('signin', async ({ send, token }) => {
  await send(
    `Signed in using OAuth connection ${token.connectionName}. Please type **/whoami** to see your profile or **/signout** to sign out.`
  );
});
```

---

# [SDK 2.1 (current)](#tab/core)
The callback is scoped to its connection, so there's no need to branch on the connection name.

```ts
graph.onSignInComplete(async (ctx, token) => {
  await ctx.send(
    `Signed in on ${token.connectionName}. Please type **/whoami** to see your profile or **/signout** to sign out.`
  );
});
```

> [!NOTE]
> Each flow holds a single completion callback — registering again replaces the previous one. The app-wide `signin` event still fires for every connection if you need one place to observe them all.

::: zone-end


## Start using the client

> [!NOTE]
> The default graph configuration requests the `User.ReadBasic.All` permission. It is possible to request other permissions by modifying the App Registration for the bot on Azure.


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
```csharp
teams.OnMessage("/whoami", async (context, cancellationToken) =>
{
    if (!context.IsSignedIn)
    {
        await context.Send("you are not signed in. Please type **/signin** to sign in.", cancellationToken);
        return;
    }

    var me = await context.GetUserGraphClient().Me.GetAsync(cancellationToken: cancellationToken);
    await context.Send($"user \"{me!.DisplayName}\" signed in.", cancellationToken);
});
```

---

# [SDK 2.1 (current)](#tab/core)
```csharp
using System.Net.Http.Headers;

teams.OnMessage("/whoami", async (context, cancellationToken) =>
{
    string? token = await graphAuth.SignInAsync(context, cancellationToken);
    if (token is null) return; // OAuth card sent / waiting for callback turn

    using var http = new HttpClient();
    http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

    string meJson = await http.GetStringAsync(
        "https://graph.microsoft.com/v1.0/me?$select=displayName,mail,userPrincipalName",
        cancellationToken);

    await context.SendAsync(meJson, cancellationToken);
});

teams.OnMessage("(?i)^my gh user$", async (context, cancellationToken) =>
{
    string? token = await githubAuth.SignInAsync(context, cancellationToken);
    if (token is null) return;

    using HttpClient http = new();
    http.DefaultRequestHeaders.Authorization = new("Bearer", token);
    http.DefaultRequestHeaders.UserAgent.ParseAdd("TeamsBot/1.0");

    string response = await http.GetStringAsync(
        "https://api.github.com/user", ct);
    await context.SendAsync($"Your GitHub user :\n```json\n{response}\n```", ct);
});

```
::: zone-end

::: zone pivot="python"
From this point, you can query graph for the signed-in user, for example to reply to the `/whoami` message, or in any other route.

# [SDK 2.0 (Legacy)](#tab/legacy)
Use the `is_signed_in` flag and the `user_graph` client.

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
```

---

# [SDK 2.1 (current)](#tab/core)
Build the client from the flow's token, so it always talks to the connection that owns it.

```python
from microsoft_teams.graph import get_graph_client

@app.on_message_pattern("/whoami")
async def handle_whoami_message(ctx: ActivityContext[MessageActivity]):
    """Handle messages to show user information from Microsoft Graph."""
    token = await graph.sign_in(ctx)
    if token is None:
        return  # OAuth card sent — resumes on the callback turn

    client = get_graph_client(token)
    me = await client.me.get()
    await ctx.send(f"Hello {me.display_name}! Your email is {me.mail or me.user_principal_name}")
```
::: zone-end

::: zone pivot="typescript"
From this point, you can query graph for the signed-in user, for example to reply to the `/whoami` message, or in any other route.

# [SDK 2.0 (Legacy)](#tab/legacy)
Use the `isSignedIn` flag and the `userGraph` client.

```ts
import * as endpoints from '@microsoft/teams.graph-endpoints';

app.message('/whoami', async ({ send, userGraph, signin }) => {
  if (!await signin()) {
    return;
  }
  const me = await userGraph.call(endpoints.me.get);
  await send(
    `you are signed in as "${me.displayName}" and your email is "${me.mail || me.userPrincipalName}"`
  );
});

app.on('message', async ({ send, activity, signin }) => {
  if (await signin()) {
    await send(
      `You said: "${activity.text}". Please type **/whoami** to see your profile or **/signout** to sign out.`
    );
  } else {
    await send(`You said: "${activity.text}". Please type **/signin** to sign in.`);
  }
});
```

---

# [SDK 2.1 (current)](#tab/core)
Build the client from the flow's token, so it always talks to the connection that owns it.

```ts
import { Client as GraphClient } from '@microsoft/teams.graph';
import * as endpoints from '@microsoft/teams.graph-endpoints';

app.message('/whoami', async (ctx) => {
  const token = await graph.signIn(ctx);
  if (!token) return; // OAuth card sent — resumes on the callback turn

  const client = new GraphClient({ token: () => token }, { baseUrlRoot: app.graphBaseUrl });
  const me = await client.call(endpoints.me.get);
  await ctx.send(
    `you are signed in as "${me.displayName}" and your email is "${me.mail || me.userPrincipalName}"`
  );
});
```
::: zone-end


## Signing Out

You can signout by calling the `signout` method, this will remove the token from the User Token service cache


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
```csharp
teams.OnMessage("/signout", async (context, cancellationToken) =>
{
    if (!context.IsSignedIn)
    {
        await context.Send("you are not signed in!", cancellationToken);
        return;
    }

    await context.SignOut(cancellationToken: cancellationToken);
    await context.Send("you have been signed out!", cancellationToken);
});
```

---

# [SDK 2.1 (current)](#tab/core)
```csharp
teams.OnMessage("/signout graph", async (context, cancellationToken) =>
{
    await graphAuth.SignOutAsync(context, cancellationToken);
    await context.SendAsync("you have been signed out from Graph!", cancellationToken);
});

teams.OnMessage("/signout github", async (context, cancellationToken) =>
{
    await githubAuth.SignOutAsync(context, cancellationToken);
    await context.SendAsync("you have been signed out from GitHub!", cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
# [SDK 2.0 (Legacy)](#tab/legacy)
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

---

# [SDK 2.1 (current)](#tab/core)
```python
@app.on_message_pattern("/signout")
async def handle_signout_message(ctx: ActivityContext[MessageActivity]):
    """Handle sign out requests."""
    await graph.sign_out(ctx)
    await ctx.send("You have been signed out!")
```
::: zone-end

::: zone pivot="typescript"
# [SDK 2.0 (Legacy)](#tab/legacy)
```ts
app.message('/signout', async ({ send, signout, isSignedIn }) => {
  if (!isSignedIn) return;
  await signout();
  await send('you have been signed out!');
});
```

---

# [SDK 2.1 (current)](#tab/core)
```ts
app.message('/signout', async (ctx) => {
  await graph.signOut(ctx);
  await ctx.send('you have been signed out!');
});
```
::: zone-end


## Using multiple OAuth connections

An agent may need more than one identity — for example Graph for the user's profile and GitHub for their repos. Each connection is registered separately, so tokens, callbacks and sign-out are scoped to the connection that owns them.


::: zone pivot="csharp"
```csharp
builder.Services.AddTeamsBotApplication(options =>
{
    options.AddOAuthFlow("graph", oauth => oauth.OAuthCardText = "Sign in with Microsoft");
    options.AddOAuthFlow("github", oauth => oauth.OAuthCardText = "Sign in with GitHub");
});

OAuthFlow graphAuth = teams.GetOAuthFlow("graph");
OAuthFlow githubAuth = teams.GetOAuthFlow("github");

teams.OnMessage("/graph", async (context, cancellationToken) =>
{
    string? token = await graphAuth.SignInAsync(context, cancellationToken);
    if (token is not null)
    {
        await SendGraphProfileAsync(context, token, cancellationToken);
    }
});

teams.OnMessage("/github", async (context, cancellationToken) =>
{
    string? token = await githubAuth.SignInAsync(context, cancellationToken);
    if (token is not null)
    {
        await SendGitHubProfileAsync(context, token, cancellationToken);
    }
});

graphAuth.OnSignInComplete(async (context, tokenResponse, cancellationToken) =>
    await SendGraphProfileAsync(context, tokenResponse.Token, cancellationToken));

githubAuth.OnSignInComplete(async (context, tokenResponse, cancellationToken) =>
    await SendGitHubProfileAsync(context, tokenResponse.Token, cancellationToken));

teams.OnMessage("/signout github", async (context, cancellationToken) =>
{
    await githubAuth.SignOutAsync(context, cancellationToken);
    await context.SendAsync("Signed out of GitHub.", cancellationToken);
});
```

Signing out of one connection leaves the other signed in.
::: zone-end

::: zone pivot="python"
```python
app = App()

graph = app.add_oauth_flow("graph", oauth_card_text="Sign in with Microsoft")
github = app.add_oauth_flow("github", oauth_card_text="Sign in with GitHub")

@app.on_message_pattern("/graph")
async def handle_graph(ctx: ActivityContext[MessageActivity]):
    token = await graph.sign_in(ctx)
    if token:
        await send_graph_profile(ctx, token)

@app.on_message_pattern("/github")
async def handle_github(ctx: ActivityContext[MessageActivity]):
    token = await github.sign_in(ctx)
    if token:
        await send_github_profile(ctx, token)

@graph.on_signin
async def on_graph_signin(event: SignInEvent):
    await send_graph_profile(event.activity_ctx, event.token_response.token)

@github.on_signin
async def on_github_signin(event: SignInEvent):
    await send_github_profile(event.activity_ctx, event.token_response.token)

@app.on_message_pattern("/signout github")
async def handle_signout_github(ctx: ActivityContext[MessageActivity]):
    await github.sign_out(ctx)
    await ctx.send("Signed out of GitHub.")
```

Signing out of one connection leaves the other signed in.
::: zone-end

::: zone pivot="typescript"
```ts
const app = new App();

const graph = app.addOAuthFlow('graph', { oauthCardText: 'Sign in with Microsoft' });
const github = app.addOAuthFlow('github', { oauthCardText: 'Sign in with GitHub' });

app.message('/graph', async (ctx) => {
  const token = await graph.signIn(ctx);
  if (token) await sendGraphProfile(ctx, token);
});

app.message('/github', async (ctx) => {
  const token = await github.signIn(ctx);
  if (token) await sendGitHubProfile(ctx, token);
});

graph.onSignInComplete(async (ctx, token) => sendGraphProfile(ctx, token.token));
github.onSignInComplete(async (ctx, token) => sendGitHubProfile(ctx, token.token));

app.message('/signout github', async (ctx) => {
  await github.signOut(ctx);
  await ctx.send('Signed out of GitHub.');
});
```

Signing out of one connection leaves the other signed in.
::: zone-end


> [!NOTE]
> Each connection must exist on the Azure Bot resource under the name you register it with. Follow the [SSO Setup guide](../teams/user-authentication/sso-setup.md) once per connection.

## Checking connection status

One call returns the status of every registered connection, so you don't have to probe them individually.


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Core;

teams.OnMessage("/status", async (context, cancellationToken) =>
{
    IList<GetTokenStatusResult> statuses = await graphAuth.GetConnectionStatusAsync(context, cancellationToken);
    IEnumerable<string> lines = statuses.Select(status =>
        $"- `{status.ConnectionName}`: {(status.HasToken == true ? "signed in" : "signed out")}");
    await context.SendAsync(string.Join("\n", lines), cancellationToken);
});
```

`GetConnectionStatusAsync` reports every connection registered on the bot, so calling it on any flow returns the same list.
::: zone-end

::: zone pivot="python"
```python
@app.on_message_pattern("/status")
async def handle_status(ctx: ActivityContext[MessageActivity]):
    statuses = await ctx.get_connection_status()
    lines = [
        f"- `{status.connection_name}`: {'signed in' if status.has_token else 'signed out'}"
        for status in statuses
    ]
    await ctx.send("\n".join(lines))
```
::: zone-end

::: zone pivot="typescript"
```ts
app.message('/status', async (ctx) => {
  const statuses = await ctx.getConnectionStatus();
  const lines = statuses.map(
    (status) => `- \`${status.connectionName}\`: ${status.hasToken ? 'signed in' : 'signed out'}`
  );
  await ctx.send(lines.join('\n'));
});
```
::: zone-end


## Resuming Pending Messages After Sign-In

When a user isn't signed in and your message handler calls the sign-in method, an OAuth card is sent and the current turn ends. The sign-in completes on a *separate turn* — meaning the original message text is not available in the sign-in success context.

To avoid ignoring what the user originally asked, store the pending message before initiating sign-in, then retrieve and process it once sign-in succeeds:


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
```csharp
using System.Collections.Concurrent;

var pendingMessages = new ConcurrentDictionary<string, string>();

teams.OnMessage(async (context, cancellationToken) =>
{
    if (!context.IsSignedIn)
    {
        var userId = context.Activity.From?.Id ?? string.Empty;
        pendingMessages[userId] = context.Activity.Text ?? string.Empty;

        await context.SignIn(cancellationToken: cancellationToken);
        return;
    }

    await ProcessMessage(context.Activity.Text, context, cancellationToken);
});

teams.OnSignIn(async (_, teamsEvent, cancellationToken) =>
{
    var context = teamsEvent.Context;
    var userId = context.Activity.From?.Id ?? string.Empty;

    if (pendingMessages.TryRemove(userId, out var text))
    {
        await context.Send("Successfully signed in! Processing your original request...", cancellationToken);
        await ProcessMessage(text, context, cancellationToken);
    }
});
```

---

# [SDK 2.1 (current)](#tab/core)
```csharp
using System.Collections.Concurrent;
using Microsoft.Teams.Apps;
using Microsoft.Teams.Apps.OAuth;

var pendingMessages = new ConcurrentDictionary<string, string>();

teams.OnMessage("(?i)^my ad user$", async (context, cancellationToken) =>
{
    var userId = context.Activity.From?.Id ?? string.Empty;
    string? token = await graphAuth.SignInAsync(context, cancellationToken);
    if (token is null)
    {
        pendingMessages[userId] = context.Activity.Text ?? string.Empty;
        return;
    }

    await ProcessGraphMessage(context.Activity.Text, context, token, cancellationToken);
});

graphAuth.OnSignInComplete(async (context, tokenResponse, cancellationToken) =>
{
    var userId = context.Activity.From?.Id ?? string.Empty;
    if (pendingMessages.TryRemove(userId, out var text))
    {
        await context.SendAsync("Successfully signed in to Graph! Processing your request...", cancellationToken);
        await ProcessGraphMessage(text, context, tokenResponse.Token, cancellationToken);
    }
});
```
::: zone-end

::: zone pivot="python"
# [SDK 2.0 (Legacy)](#tab/legacy)
```python
from microsoft_teams.apps import App, ActivityContext, SignInEvent
from microsoft_teams.apps.routing import SignInOptions
from microsoft_teams.api import MessageActivity

app = App()

pending_messages: dict[str, str] = {}

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    # sign_in() returns the token if already signed in, or None if OAuth card was sent
    token = await ctx.sign_in(SignInOptions(
        oauth_card_text="To help with that, I need to sign you in first."
    ))

    if token is None:
        # OAuth card sent — store the original message for later
        pending_messages[ctx.activity.from_.id] = ctx.activity.text
        return

    # User is already signed in — process normally
    await process_message(ctx.activity.text, ctx)

@app.event("sign_in")
async def handle_sign_in(event: SignInEvent):
    user_id = event.activity_ctx.activity.from_.id
    pending = pending_messages.pop(user_id, None)

    if pending:
        await event.activity_ctx.send("Successfully signed in! Processing your original request...")
        await process_message(pending, event.activity_ctx)
    else:
        await event.activity_ctx.send("You are now signed in!")
```

---

# [SDK 2.1 (current)](#tab/core)
```python
from microsoft_teams.apps import App, ActivityContext, SignInEvent
from microsoft_teams.apps.routing import SignInOptions
from microsoft_teams.api import MessageActivity

app = App()
graph = app.add_oauth_flow("graph")

pending_messages: dict[str, str] = {}

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    # sign_in() returns the token if already signed in, or None if an OAuth card was sent
    token = await graph.sign_in(ctx, SignInOptions(
        oauth_card_text="To help with that, I need to sign you in first."
    ))

    if token is None:
        pending_messages[ctx.activity.from_.id] = ctx.activity.text
        return

    await process_message(ctx.activity.text, ctx, token)

@graph.on_signin
async def on_graph_signin(event: SignInEvent):
    user_id = event.activity_ctx.activity.from_.id
    pending = pending_messages.pop(user_id, None)

    if pending:
        await event.activity_ctx.send("Successfully signed in! Processing your original request...")
        await process_message(pending, event.activity_ctx, event.token_response.token)
    else:
        await event.activity_ctx.send("You are now signed in!")
```
::: zone-end

::: zone pivot="typescript"
# [SDK 2.0 (Legacy)](#tab/legacy)
```ts
const pendingMessages = new Map<string, { text: string; activity: any }>();

app.on('message', async ({ signin, activity, send }) => {
  // signin() returns the token if already signed in, or undefined if OAuth card was sent
  const token = await signin({
    oauthCardText: 'To help with that, I need to sign you in first.',
  });

  if (!token) {
    // OAuth card sent — store the original message for later
    pendingMessages.set(activity.from.id, {
      text: activity.text,
      activity,
    });
    return;
  }

  // User is already signed in — process normally
  await processMessage(activity.text, { send });
});

app.event('signin', async ({ send, userGraph, activity }) => {
  const userId = activity.from.id;
  const pending = pendingMessages.get(userId);

  if (pending) {
    pendingMessages.delete(userId);
    await send('Successfully signed in! Processing your original request...');
    await processMessage(pending.text, { send, userGraph });
  } else {
    await send('You are now signed in!');
  }
});
```

---

# [SDK 2.1 (current)](#tab/core)
```ts
const pendingMessages = new Map<string, string>();

app.on('message', async (ctx) => {
  // signIn() returns the token if already signed in, or undefined if an OAuth card was sent
  const token = await graph.signIn(ctx, {
    oauthCardText: 'To help with that, I need to sign you in first.',
  });

  if (!token) {
    pendingMessages.set(ctx.activity.from.id, ctx.activity.text);
    return;
  }

  await processMessage(ctx.activity.text, ctx, token);
});

graph.onSignInComplete(async (ctx, token) => {
  const userId = ctx.activity.from.id;
  const pending = pendingMessages.get(userId);

  if (!pending) {
    await ctx.send('You are now signed in!');
    return;
  }

  pendingMessages.delete(userId);
  await ctx.send('Successfully signed in! Processing your original request...');
  await processMessage(pending, ctx, token.token);
});
```
::: zone-end


> [!TIP]
> For production apps, consider using a persistent store (database, Redis, etc.) instead of an in-memory map so pending messages survive restarts. You should also implement expiration or cleanup logic (e.g., a TTL) to discard stale entries when sign-in is cancelled, times out, or fails.

## Handling Sign-In Failures

When using SSO, if the token exchange fails Teams sends a `signin/failure` invoke activity to your app. The SDK includes a built-in default handler that logs a warning with actionable troubleshooting guidance. You can optionally register your own handler to customize the behavior:


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
```csharp
teams.OnSignInFailure(async (context, cancellationToken) =>
{
    var failure = context.Activity.Value;
    context.Log.Error($"sign-in failed: {failure?.Code} - {failure?.Message}");
    await context.Send("Sign-in failed.", cancellationToken);
});
```

---

# [SDK 2.1 (current)](#tab/core)
```csharp
graphAuth.OnSignInFailure(async (context, failure, cancellationToken) =>
{
    await context.SendAsync(
        $"Graph sign-in failed: {failure?.Code} - {failure?.Message}",
        cancellationToken);
});

githubAuth.OnSignInFailure(async (context, failure, cancellationToken) =>
{
    await context.SendAsync(
        $"GitHub sign-in failed: {failure?.Code} - {failure?.Message}",
        cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
# [SDK 2.0 (Legacy)](#tab/legacy)
```python
@app.on_signin_failure()
async def handle_signin_failure(ctx):
    failure = ctx.activity.value
    print(f"Sign-in failed: {failure.code} - {failure.message}")
    await ctx.send("Sign-in failed.")
```

> [!NOTE]
> Registering a custom handler does **not** replace the built-in default handler. Both will run as part of the middleware chain.

---

# [SDK 2.1 (current)](#tab/core)
```python
from microsoft_teams.apps import SignInFailureEvent

@graph.on_signin_failure
async def on_graph_signin_failure(event: SignInFailureEvent):
    ctx = event.activity_ctx
    ctx.logger.error(f"Graph sign-in failed: {event.code} - {event.message}")
    await ctx.send("Graph sign-in failed.")
```

A flow can have more than one failure handler; they run in registration order and are isolated from each other.
::: zone-end

::: zone pivot="typescript"
# [SDK 2.0 (Legacy)](#tab/legacy)
```ts
app.on('signin.failure', async ({ activity, send }) => {
  const { code, message } = activity.value;
  console.log(`Sign-in failed: ${code} - ${message}`);
  await send('Sign-in failed.');
});
```

---

# [SDK 2.1 (current)](#tab/core)
```ts
graph.onSignInFailure(async (ctx, failure) => {
  ctx.log.error(`Graph sign-in failed: ${failure?.code} - ${failure?.message}`);
  await ctx.send('Graph sign-in failed.');
});
```

`failure` is undefined for token-service and token-exchange failures, which carry no Teams payload.
::: zone-end


> [!TIP]
> The most common failure codes are `installedappnotfound` (bot app not installed for the user) and `resourcematchfailed` (Token Exchange URL doesn't match the Application ID URI). See [SSO Setup - Troubleshooting](../teams/user-authentication/sso-setup.md#troubleshooting) for a full list of failure codes and troubleshooting steps.

> [!WARNING]
> A `signin/failure` activity doesn't name its connection. The SDK attributes it from the pending sign-in recorded when the flow started; if that can't be resolved, *every* registered connection's failure handler is notified. Check the connection first if your handler does something destructive.
>
> Registering a flow also turns on per-turn state unless you configure `state` yourself, defaulting to local, in-process storage. Configure shared state storage before running more than one instance — otherwise pending sign-in attribution and token-exchange dedup don't cross processes, and sign-in fails intermittently.


::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="python"
## Regional Configs
You may be building a regional bot that is deployed in a specific Azure region (such as West Europe, East US, etc.) rather than global. This is important for organizations that have data residency requirements or want to reduce latency by keeping data and authentication flows within a specific area.

These examples use West Europe, but follow the equivalent for other regions.

# [Azure Portal](#tab/portal)
To configure a new regional bot in Azure, you must setup your resoures in the desired region. Your resource group must also be in the same region.

1. Deploy a new App Registration in `westeurope`.
2. Deploy and link a new Enterprise Application (Service Principal) on Microsoft Entra in `westeurope`.
3. Deploy and link a new Azure Bot in `westeurope`.
4. In your App Registration, in the `Authentication (Preview)` tab, add a `Redirect URI` for the Platform Type `Web` to your regional endpoint (e.g., `https://europe.token.botframework.com/.auth/web/redirect`)

:::image type="content" source="~/assets/screenshots/regional-auth.png" alt-text="Authentication Tab" lightbox="~/assets/screenshots/regional-auth.png" :::

5. In your `.env` file (or wherever you set your environment variables), add your `OAUTH_URL`. For example:
`OAUTH_URL=https://europe.token.botframework.com`

---

# [Agents Toolkit](#tab/atk)
To configure a new regional bot with ATK, you will need to make a few updates. Note that this assumes you have not yet deployed the bot previously.

1. In `azurebot.bicep`, replace all `global` occurrences to `westeurope`
2. In `manifest.json`, in `validDomains`, `*.botframework.com` should be replaced by `europe.token.botframework.com`
3. In `aad.manifest.json`, replace `https://token.botframework.com/.auth/web/redirect` with `https://europe.token.botframework.com/.auth/web/redirect`
4. In your `.env` file, add your `OAUTH_URL`. For example:
`OAUTH_URL=https://europe.token.botframework.com`.
::: zone-end

::: zone pivot="typescript"
## Regional Configs
You may be building a regional bot that is deployed in a specific Azure region (such as West Europe, East US, etc.) rather than global. This is important for organizations that have data residency requirements or want to reduce latency by keeping data and authentication flows within a specific area.

These examples use West Europe, but follow the equivalent for other regions.

# [Azure Portal](#tab/portal)
To configure a new regional bot in Azure, you must setup your resoures in the desired region. Your resource group must also be in the same region.

1. Deploy a new App Registration in `westeurope`.
2. Deploy and link a new Enterprise Application (Service Principal) on Microsoft Entra in `westeurope`.
3. Deploy and link a new Azure Bot in `westeurope`.
4. In your App Registration, in the `Authentication (Preview)` tab, add a `Redirect URI` for the Platform Type `Web` to your regional endpoint (e.g., `https://europe.token.botframework.com/.auth/web/redirect`)

:::image type="content" source="~/assets/screenshots/regional-auth.png" alt-text="Authentication Tab" lightbox="~/assets/screenshots/regional-auth.png" :::

5. In your `.env` file (or wherever you set your environment variables), add your `OAUTH_URL`. For example:
`OAUTH_URL=https://europe.token.botframework.com`

---

# [Agents Toolkit](#tab/atk)
To configure a new regional bot with ATK, you will need to make a few updates. Note that this assumes you have not yet deployed the bot previously.

1. In `azurebot.bicep`, replace all `global` occurrences to `westeurope`
2. In `manifest.json`, in `validDomains`, `*.botframework.com` should be replaced by `europe.token.botframework.com`
3. In `aad.manifest.json`, replace `https://token.botframework.com/.auth/web/redirect` with `https://europe.token.botframework.com/.auth/web/redirect`
4. In your `.env` file, add your `OAUTH_URL`. For example:
`OAUTH_URL=https://europe.token.botframework.com`
::: zone-end


## Resources

[User Authentication Basics](/azure/bot-service/bot-builder-concept-authentication)
