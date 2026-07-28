---
title: App Authentication
description: Configure app authentication in your Teams SDK application using client secrets, user assigned managed identities, or federated identity credentials
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 07/27/2026
---

# App Authentication


Your application needs to authenticate to send messages to Teams as your bot. Authentication allows your app service to certify that it is _allowed_ to send messages as your Azure Bot.

:::info Azure Setup Required
Before configuring your application, you must first set up authentication in Azure. See the [App Authentication Setup](../../teams/app-authentication/overview.md) guide for instructions on creating the necessary Azure resources.
:::

## Authentication Methods

There are 3 main ways of authenticating:

1. **Client Secret** - Simple password-based authentication using a client secret
2. **User Assigned Managed Identity** - Passwordless authentication using Azure managed identities
3. **Federated Identity Credentials** - Advanced identity federation using managed identities

## Configuration Reference

The Teams SDK automatically detects which authentication method to use based on the environment variables you set:

| CLIENT_ID | CLIENT_SECRET | MANAGED_IDENTITY_CLIENT_ID | Authentication Method |
| --- | --- | --- | --- |
| not_set | | | No-Auth (local development only) |
| set | set | | Client Secret |
| set | not_set | | User Assigned Managed Identity |
| set | not_set | set (same as CLIENT_ID) | User Assigned Managed Identity |
| set | not_set | set (different from CLIENT_ID) | Federated Identity Credentials (UMI) |
| set | not_set | "system" | Federated Identity Credentials (System Identity) |

## Client Secret

The simplest authentication method using a password-like secret.

### User Assigned Managed Identity Setup

First, complete the [Client Secret Setup](../../teams/app-authentication/client-secret.md) in Azure Portal or Azure CLI.

### User Assigned Managed Identity Configuration

Set the following environment variables in your application:

- `CLIENT_ID`: Your Application (client) ID
- `CLIENT_SECRET`: The client secret value you created
- `TENANT_ID`: The tenant id where your bot is registered

```env

CLIENT_ID=your-client-id-here
CLIENT_SECRET=your-client-secret-here
TENANT_ID=your-tenant-id

```

The SDK will automatically use Client Secret authentication when both `CLIENT_ID` and `CLIENT_SECRET` are provided.

## User Assigned Managed Identity

Passwordless authentication using Azure managed identities - no secrets to rotate or manage.

### Setup

First, complete the [User Assigned Managed Identity Setup](../../teams/app-authentication/user-managed-identity.md) in Azure Portal or Azure CLI.

### Configuration


::: zone pivot="csharp"
> [!NOTE]
>
> The environment file approach is not yet supported for C#. You need to configure authentication programmatically in your code.

In your `Program.cs`, replace the initialization:

```csharp

var builder = WebApplication.CreateBuilder(args);
builder.AddTeams();

```

ith the following code to enable User Assigned Managed Identity authentication:

```csharp

var builder = WebApplication.CreateBuilder(args);

Func<string[], string?, Task<ITokenResponse>> createTokenFactory = async (string[] scopes, string? tenantId) =>
{
    var clientId = Environment.GetEnvironmentVariable("CLIENT_ID");
    var managedIdentityCredential = new ManagedIdentityCredential(clientId);
    var tokenRequestContext = new TokenRequestContext(scopes, tenantId: tenantId);
    var accessToken = await managedIdentityCredential.GetTokenAsync(tokenRequestContext);

    return new TokenResponse
    {
        TokenType = "Bearer",
        AccessToken = accessToken.Token,
    };
};

var appBuilder = App.Builder()
    .AddCredentials(new TokenCredentials(
        Environment.GetEnvironmentVariable("CLIENT_ID") ?? string.Empty,
        async (tenantId, scopes) =>
        {
            return await createTokenFactory(scopes, tenantId);
        }
    ));

builder.AddTeams(appBuilder);

```

The `createTokenFactory` function provides a method to retrieve access tokens from Azure on demand, and `TokenCredentials` passes this method to the app.

## User Assigned Managed Identity Environment Variables

Set the following environment variable:

- `CLIENT_ID`: Your Application (client) ID
::: zone-end

::: zone pivot="python,typescript"
Your application should automatically use User Assigned Managed Identity authentication when you provide the `CLIENT_ID` environment variable without a `CLIENT_SECRET`.

## Federated Identity Credentials Environment Variables

Set the following environment variables in your application:

- `CLIENT_ID`: Your Application (client) ID
- **Do not set** `CLIENT_SECRET`
- `TENANT_ID`: The tenant id where your bot is registered

```env

CLIENT_ID=your-client-id-here
# Do not set CLIENT_SECRET
TENANT_ID=your-tenant-id

```

::: zone-end
## Federated Identity Credentials

Advanced identity federation allowing you to assign managed identities directly to your App Registration.


::: zone pivot="csharp"
> [!NOTE]
>
> C# uses `appsettings.json` and process environment variables via `IConfiguration` (the standard ASP.NET Core pattern). `.env` files are not used.
::: zone-end

::: zone pivot="python"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
<!-- Not applicable -->
::: zone-end


### Federated Identity Credentials Setup

First, complete the [Federated Identity Credentials Setup](../../teams/app-authentication/federated-identity-credentials.md) in Azure Portal or Azure CLI.

### Federated Identity Credentials Configuration

Depending on the type of managed identity you select, set the environment variables accordingly.

**For User Assigned Managed Identity:**

Set the following environment variables:

- `CLIENT_ID`: Your Application (client) ID
- `MANAGED_IDENTITY_CLIENT_ID`: The Client ID for the User Assigned Managed Identity resource
- **Do not set** `CLIENT_SECRET`
- `TENANT_ID`: The tenant id where your bot is registered

```env

CLIENT_ID=your-app-client-id-here
MANAGED_IDENTITY_CLIENT_ID=your-managed-identity-client-id-here
# Do not set CLIENT_SECRET
TENANT_ID=your-tenant-id

```

**For System Assigned Identity:**

Set the following environment variables:

- `CLIENT_ID`: Your Application (client) ID
- `MANAGED_IDENTITY_CLIENT_ID`: `system`
- **Do not set** `CLIENT_SECRET`
- `TENANT_ID`: The tenant id where your bot is registered

```env

CLIENT_ID=your-app-client-id-here
MANAGED_IDENTITY_CLIENT_ID=system
# Do not set CLIENT_SECRET
TENANT_ID=your-tenant-id

```

## Sovereign Cloud

If your bot runs in a US Government (GCC-High, DoD) or China (21Vianet) cloud environment, add the `CLOUD` environment variable to your configuration:

```env

CLOUD=USGov

```

Valid values: `Public` (default), `USGov`, `USGovDoD`, `China`

The SDK automatically configures all authentication endpoints for the specified cloud. No other changes are needed. See the [Sovereign Cloud](../app-configuration/sovereign-cloud.md) guide for details and programmatic configuration options.

## Troubleshooting

If you encounter authentication errors, see the [Authentication Troubleshooting](../../teams/app-authentication/troubleshooting.md) guide for common issues and solutions.


