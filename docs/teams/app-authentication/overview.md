---
title: App Authentication Setup
description: Set up authentication for your Teams bot using client secrets, user assigned managed identities, or federated identity credentials
ms.topic: how-to
ms.date: 07/27/2026
---



# App Authentication Setup

Your Teams bot needs to authenticate with Azure to send messages. This involves configuring your Azure Bot Service and App Registration correctly.

## Authentication Methods

Choose one of the following authentication methods based on your security requirements:

1. **[Client Secret](client-secret.md)** - Simple password-based authentication using a client secret
2. **[User Assigned Managed Identity](user-managed-identity.md)** - Passwordless authentication using Azure managed identities
3. **[Federated Identity Credentials](federated-identity-credentials.md)** - Advanced identity federation using managed identities assigned to App Registration

Each method has different setup requirements in Azure Portal or Azure CLI.

## Sovereign Cloud

If your bot runs in a US Government (GCC-High, DoD) or China (21Vianet) cloud environment, see the [Sovereign Cloud](../../essentials/app-configuration/sovereign-cloud.md) configuration guide.

## After Setup

Once you've completed the Azure setup for your chosen authentication method, you'll need to configure your application code. See the [App Authentication configuration guide](../../essentials/app-authentication/overview.md) for details on environment variables and code configuration.

## Troubleshooting

If you encounter authentication errors, see the [Troubleshooting](troubleshooting.md) guide for common issues and solutions.
