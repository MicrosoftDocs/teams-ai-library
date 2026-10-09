---
title: App Authentication
description: Configure app authentication in your Teams SDK application using client secrets, user assigned managed identities, or federated identity credentials
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---

# App Authentication

Your application needs to authenticate to send messages to Teams as your bot. Authentication allows your app service to certify that it is _allowed_ to send messages as your Azure Bot.

> [!NOTE]
> Azure Setup Required. Before configuring your application, you must first set up authentication in Azure. See the [App Authentication Setup](../../teams/app-authentication/overview.md) guide for instructions on creating the necessary Azure resources.

## Authentication Methods

There are 3 main ways of authenticating:

1. **Client Secret** - Simple password-based authentication using a client secret
2. **User Assigned Managed Identity** - Passwordless authentication using Azure managed identities
3. **Federated Identity Credentials** - Advanced identity federation using managed identities

## Configuration Reference

The Teams SDK automatically detects which authentication method to use based on the environment variables you set:

| CLIENT_ID | CLIENT_SECRET | MANAGED_IDENTITY_CLIENT_ID | Authentication Method |
|-|-|-|-|
| not_set | | | No-Auth (local development only) |
| set | set | | Client Secret |
| set | not_set | | User Assigned Managed Identity |
| set | not_set | set (same as CLIENT_ID) | User Assigned Managed Identity |
| set | not_set | set (different from CLIENT_ID) | Federated Identity Credentials (UMI) |
| set | not_set | "system" | Federated Identity Credentials (System Identity) |

> [!NOTE]
> SDK 2.1. SDK 2.1 uses MSAL with standard ASP.NET Core configuration. Developers can authenticate their bot with any supported Microsoft Entra authentication solution by configuring the app according to the [`Microsoft.Identity.Web` credential format](/entra/msidweb/authentication/credentials-overview#configure-credentials-in-appsettingsjson).

## Client Secret

The simplest authentication method using a password-like secret.

### Setup

First, complete the [Client Secret Setup](../../teams/app-authentication/client-secret.md) in Azure Portal or Azure CLI.

### Configuration


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
Set the following environment variables in your application:

- `CLIENT_ID`: Your Application (client) ID
- `CLIENT_SECRET`: The client secret value you created
- `TENANT_ID`: The tenant id where your bot is registered

```env
CLIENT_ID=your-client-id-here
CLIENT_SECRET=your-client-secret-here
TENANT_ID=your-tenant-id
```

---

# [SDK 2.1 (current)](#tab/core)
Configure the following settings in `appsettings.json`:

```json title="appsettings.json"
{
  "AzureAd": {
    "ClientId": "your-client-id-here",
    "TenantId": "your-tenant-id",
    "ClientCredentials": [
      {
        "SourceType": "ClientSecret",
        "ClientSecret": "your-client-secret-here"
      }
    ]
  }
}
```
::: zone-end

::: zone pivot="python,typescript"
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
::: zone-end


## User Assigned Managed Identity

Passwordless authentication using Azure managed identities - no secrets to rotate or manage.

### Setup

First, complete the [User Assigned Managed Identity Setup](../../teams/app-authentication/user-managed-identity.md) in Azure Portal or Azure CLI.

### Configuration


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
> [!NOTE]
> The environment file approach is not yet supported for C#. You need to configure authentication programmatically in your code.

In your `Program.cs`, replace the initialization:
```csharp
var builder = WebApplication.CreateBuilder(args);
builder.AddTeams();
```
with the following code to enable User Assigned Managed Identity authentication:
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

Set the following environment variables:

- `CLIENT_ID`: Your Application (client) ID

---

# [SDK 2.1 (current)](#tab/core)
Your application should automatically use User Assigned Managed Identity authentication when you provide the `ClientId` without a `ClientSecret`.

Configure the following settings in `appsettings.json`:

```json title="appsettings.json"
{
  "AzureAd": {
    "ClientId": "your-client-id-here",
    "TenantId": "your-tenant-id"
  }
}
```
::: zone-end

::: zone pivot="python,typescript"
Your application should automatically use User Assigned Managed Identity authentication when you provide the `CLIENT_ID` environment variable without a `CLIENT_SECRET`.

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

### Setup

First, complete the [Federated Identity Credentials Setup](../../teams/app-authentication/federated-identity-credentials.md) in Azure Portal or Azure CLI.

### Configuration


::: zone pivot="csharp"
# [SDK 2.0 (Legacy)](#tab/legacy)
> [!NOTE]
> The environment file approach is not yet supported for C#. You need to configure authentication programmatically in your code.

In your `Program.cs`, replace the initialization:

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.AddTeams();
```
with the following code to enable User Assigned Managed Identity authentication:
```csharp
var builder = WebApplication.CreateBuilder(args);

Func<string[], string?, Task<ITokenResponse>> createTokenFactory = async (string[] scopes, string? tenantId) =>
{
    var managedIdentityClientIdRaw = Environment.GetEnvironmentVariable("MANAGED_IDENTITY_CLIENT_ID");
    var managedIdentityClientId =
        string.IsNullOrWhiteSpace(managedIdentityClientIdRaw) ||
        string.Equals(managedIdentityClientIdRaw, "system", StringComparison.OrdinalIgnoreCase)
            ? null
            : managedIdentityClientIdRaw;
    var managedIdentityCredential = new ManagedIdentityCredential(managedIdentityClientId);
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
        async (tenantId, scopes) => await createTokenFactory(scopes, tenantId)));

builder.AddTeams(appBuilder);
```

The `createTokenFactory` function provides a method to retrieve access tokens from Azure on demand, and `TokenCredentials` passes this method to the app.

Set the following environment variables:

- `CLIENT_ID`: Your Application (client) ID
- `MANAGED_IDENTITY_CLIENT_ID`: The managed identity client ID, or `system` for system-assigned identity
- `TENANT_ID`: The tenant id where your bot is registered

---

# [SDK 2.1 (current)](#tab/core)
Depending on the type of managed identity you select, configure the corresponding settings in `appsettings.json`.

```json title="appsettings.json"
{
  "AzureAd": {
    "ClientId": "your-app-client-id-here",
    "TenantId": "your-tenant-id",
    "ClientCredentials": [
      {
        "SourceType": "SignedAssertionFromManagedIdentity",
        "ManagedIdentityClientId": "your-managed-identity-client-id-here"
      }
    ]
  }
}
```

For system-assigned identity, omit `ManagedIdentityClientId`:

```json title="appsettings.json"
{
  "AzureAd": {
    "ClientId": "your-app-client-id-here",
    "TenantId": "your-tenant-id",
    "ClientCredentials": [
      {
        "SourceType": "SignedAssertionFromManagedIdentity"
      }
    }
  }
}
```
::: zone-end

::: zone pivot="python,typescript"
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
::: zone-end


## Troubleshooting

If you encounter authentication errors, see the [Authentication Troubleshooting](../../teams/app-authentication/troubleshooting.md) guide for common issues and solutions.
