---
title: Tabs (preview) (TypeScript)
description: Overview of tabs functionality in the Microsoft Teams AI Library for
 TypeScript.
ms.topic: overview
ms.date: 07/16/2025
---
# Tabs (preview) (TypeScript)

[This article is prerelease documentation and is subject to change.]

Tabs are host-aware webpages embedded in Microsoft Teams, Outlook, and Microsoft 365. Tabs are commonly implemented as Single Page Applications that use the Teams [JavaScript client library](/microsoftteams/platform/tabs/how-to/using-teams-client-library) (TeamsJS) to interact with the app host.

Tab apps will often need to interact with remote services. They may need to fetch data from [Microsoft Graph](/graph/overview) or invoke remote agent functions, using the [Nested App Authentication](/microsoftteams/platform/concepts/authentication/nested-authentication) (NAA) and the [Microsoft Authentication Library](/entra/identity-platform/msal-overview) (MSAL) to ensure user consent and to allow the remote service authenticate the user.

The `@microsoft/teams.client` package in this library builds on TeamsJS and MSAL to streamline these common scenarios. It aims to simplify:

- **Remote Service Authentication** through MSAL-based authentication and token acquisition.
- **Graph API Integration** by offering a pre-configured and type-safe Microsoft Graph client.
- **Agent Function Calling** by handling authentication and including app context when calling server-side functions implemented Teams AI agents.
- **Scope Consent Management** by providing simple APIs to test for and request user consent.

## Resources
- [Tabs overview](/microsoftteams/platform/tabs/what-are-tabs?tabs=personal)
- [Teams JavaScript client library](/microsoftteams/platform/tabs/how-to/using-teams-client-library)
- [Microsoft Graph overview](/graph/overview)
- [Microsoft Authentication Library (MSAL)](/entra/identity-platform/msal-overview)
- [Nested App Authentication (NAA)](/microsoftteams/platform/concepts/authentication/nested-authentication)
