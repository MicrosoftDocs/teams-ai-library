---
sidebar_label: Hosting Static Pages
title: Hosting Static Pages
zone_pivot_groups: dev-lang
description: Shows how to host web apps.
---
# Hosting Apps/Static Pages

The `App` class lets you host web apps in the agent. This can be used for an efficient inner loop when building a complex app using Microsoft 365 Agents Toolkit, as it lets you build, deploy, and sideload both an agent and a Tab app inside of Teams in a single step. It's also useful in production scenarios, as it makes it straight-forward to host a simple experience such as an agent configuration page or a Dialog.

::: zone pivot="csharp"
To host a static tab web app, call the `app.AddTab()` function and provide an app name and a path to a folder containing an `index.html` file to be served up.
::: zone-end

::: zone pivot="python,typescript"
To host a static tab web app, call the `app.tab()` function and provide an app name and a path to a folder containing an `index.html` file to be served up.
::: zone-end


::: zone pivot="csharp"
```csharp
app.AddTab("myApp", "Web/bin");
```
::: zone-end

::: zone pivot="python"
```python
app.tab("my_app", os.path.abspath("dist/client"))
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.tab('myApp', path.resolve('dist/client'));
```
::: zone-end


::: zone pivot="csharp,typescript"
This registers a route that is hosted at `http://localhost:{PORT}/tabs/myApp` or `https://{BOT_DOMAIN}/tabs/myApp`.
::: zone-end

::: zone pivot="python"
This registers a route that is hosted at `http://localhost:{PORT}/tabs/my_app` or `https://{BOT_DOMAIN}/tabs/my_app`.
::: zone-end

## Additional resources


::: zone pivot="csharp"
- For more details about Tab apps, see the [Tabs](../in-depth-guides/tabs/) in-depth guide.
- For an example of hosting a Dialog, see the [Creating Dialogs](../in-depth-guides/dialogs/creating-dialogs) in-depth guide.
::: zone-end

::: zone pivot="python"
- For an example of hosting a Dialog, see the [Creating Dialogs](../in-depth-guides/dialogs/creating-dialogs) in-depth guide.
::: zone-end

::: zone pivot="typescript"
- For more details about Tab apps, see the [Tabs](../in-depth-guides/tabs) in-depth guide.
- For an example of hosting a Dialog, see the [Creating Dialogs](../in-depth-guides/dialogs/creating-dialogs) in-depth guide.
::: zone-end
