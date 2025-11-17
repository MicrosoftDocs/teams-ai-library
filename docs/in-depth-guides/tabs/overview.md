---
title: Tabs
zone_pivot_groups: dev-lang
description: Build Teams tab apps with Graph integration, authentication, and remote agent function calling capabilities.
---
# Tabs

::: zone pivot="python"
This page isn't available for Python
::: zone-end

::: zone pivot="csharp,typescript"
Tabs are host-aware webpages embedded in Microsoft Teams, Outlook, and Microsoft 365. Tabs are commonly implemented as Single Page Applications that use the Teams [JavaScript client library](https://learn.microsoft.com/en-us/microsoftteams/platform/tabs/how-to/using-teams-client-library) (TeamsJS) to interact with the app host.
::: zone-end

::: zone pivot="csharp"
This SDK does not offer features for implementing Tab apps in C#. It does however let you host tab apps and implement functions that can be called by Tab apps.
::: zone-end

::: zone pivot="typescript"
Tab apps will often need to interact with remote services. They may need to fetch data from [Microsoft Graph](https://learn.microsoft.com/en-us/graph/overview) or invoke remote agent functions, using the [Nested App Authentication](https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/authentication/nested-authentication) (NAA) and the [Microsoft Authentication Library](https://learn.microsoft.com/en-us/entra/identity-platform/msal-overview) (MSAL) to ensure user consent and to allow the remote service authenticate the user.

The `@microsoft/teams.client` package in this SDK builds on TeamsJS and MSAL to streamline these common scenarios. It aims to simplify:

- **Remote Service Authentication** through MSAL-based authentication and token acquisition.
- **Graph API Integration** by offering a pre-configured and type-safe Microsoft Graph client.
- **Agent Function Calling** by handling authentication and including app context when calling server-side functions implemented Teams SDK agents.
- **Scope Consent Management** by providing simple APIs to test for and request user consent.
::: zone-end

::: zone pivot="csharp,typescript"
## Resources

- [Tabs overview](https://learn.microsoft.com/en-us/microsoftteams/platform/tabs/what-are-tabs?tabs=personal)
- [Teams JavaScript client library](https://learn.microsoft.com/en-us/microsoftteams/platform/tabs/how-to/using-teams-client-library)
- [Microsoft Graph overview](https://learn.microsoft.com/en-us/graph/overview)
- [Microsoft Authentication Library (MSAL)](https://learn.microsoft.com/en-us/entra/identity-platform/msal-overview)
- [Nested App Authentication (NAA)](https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/authentication/nested-authentication)
::: zone-end

::: zone pivot="csharp"
### Additional resources

- [Hosting Apps/Static Pages](../../essentials/hosting-static-pages)
- [TypeScript Tabs in-depth guide](../../../typescript/in-depth-guides/tabs)
::: zone-end

::: zone pivot="typescript"
### Additional resources

- [Hosting Apps/Static Pages](../../essentials/hosting-static-pages)
::: zone-end

