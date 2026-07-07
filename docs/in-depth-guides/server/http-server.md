---
title: 'Self-Managing Your Server'
description: 'How to self-manage the HTTP server  bring your own Express, FastAPI, or any framework by implementing the HttpServerAdapter interface.'
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 06/29/2026
---

# Self-Managing Your Server

::: zone pivot="csharp"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="python"
By default, `app.start()` spins up an HTTP server, registers the Teams endpoint, and manages the full lifecycle for you. Under the hood, the SDK uses [FastAPI](https://fastapi.tiangolo.com/) as its built-in HTTP framework. But if you need to self-manage your server  because you have an existing app, need custom server configuration (TLS, workers, middleware), or use a different HTTP framework  the SDK supports that through the `HttpServerAdapter` interface.
::: zone-end

::: zone pivot="typescript"
By default, `app.start()` spins up an HTTP server, registers the Teams endpoint, and manages the full lifecycle for you. Under the hood, the SDK uses [Express](https://expressjs.com/) as its built-in HTTP framework. But if you need to self-manage your server  because you have an existing app, need custom server configuration (TLS, workers, middleware), or use a different HTTP framework  the SDK supports that through the `HttpServerAdapter` interface.
::: zone-end

::: zone pivot="typescript,python"
## How It Works

The SDK splits HTTP handling into two layers:

- **HttpServer** handles Teams protocol concerns: JWT authentication, activity parsing, and routing to your handlers.
- **HttpServerAdapter** handles framework concerns: translating between your HTTP framework's request/response model and the SDK's pure handler pattern.

:::image type="content" source="~/assets/diagrams/in-depth-guides-server-http-server-1.png" alt-text="Flowchart showing How It Works" lightbox="~/assets/diagrams/in-depth-guides-server-http-server-1.png" :::
The adapter interface is intentionally simple  implement `registerRoute` and the SDK handles the rest.

## The Adapter Interface
::: zone-end

::: zone pivot="python"
```python
class HttpServerAdapter(Protocol):
    def register_route(self, method: HttpMethod, path: str, handler: HttpRouteHandler) -> None: ...
    def serve_static(self, path: str, directory: str) -> None: ...
    async def start(self, port: int) -> None: ...
    async def stop(self) -> None: ...

class HttpRouteHandler(Protocol):
    async def __call__(self, request: HttpRequest) -> HttpResponse: ...
```
::: zone-end

::: zone pivot="typescript"
```typescript
interface IHttpServerAdapter {
  registerRoute(method: HttpMethod, path: string, handler: HttpRouteHandler): void;
  serveStatic?(path: string, directory: string): void;
  start?(port: number): Promise<void>;
  stop?(): Promise<void>;
}

type HttpRouteHandler = (request: { body: unknown; headers: Record<string, string | string[]> })
  => Promise<{ status: number; body?: unknown }>;
```
::: zone-end

::: zone pivot="typescript,python"
- **`registerRoute`**  Required. Routes are registered dynamically (`/api/messages`, `/api/functions/{name}`, etc.).
- **`serveStatic`**  Optional. Only needed for tabs or static pages.
- **`start` / `stop`**  Optional. Omit when you manage the server lifecycle yourself.

## Self-Managing Your Server

To add Teams to an existing server:

1. Create your server with your own routes and middleware.
2. Wrap it in an adapter (or use the built-in one with your server instance).
3. Call `app.initialize()`  this registers the Teams routes on your server. Do **not** call `app.start()`.
4. Start the server yourself.
::: zone-end

::: zone pivot="python"
```python
import asyncio
import uvicorn
from fastapi import FastAPI
from microsoft_teams.apps import App, FastAPIAdapter

# 1. Create your FastAPI app with your own routes
my_fastapi = FastAPI(title="My App + Teams Bot")

@my_fastapi.get("/health")
async def health():
    return {"status": "healthy"}

# 2. Wrap it in the FastAPIAdapter
adapter = FastAPIAdapter(app=my_fastapi)

# 3. Create the Teams app with the adapter
app = App(http_server_adapter=adapter)

@app.on_message
async def handle_message(ctx):
    await ctx.send(f"Echo: {ctx.activity.text}")

async def main():
    # 4. Initialize — registers /api/messages on your FastAPI app (does NOT start a server)
    await app.initialize()

    # 5. Start the server yourself
    config = uvicorn.Config(app=my_fastapi, host="0.0.0.0", port=3978)
    server = uvicorn.Server(config)
    await server.serve()

asyncio.run(main())
```

> See the full example: [FastAPI non-managed example](https://github.com/microsoft/teams.py/tree/main/examples/http-adapters/src/fastapi_non_managed.py)
::: zone-end

::: zone pivot="typescript"
```typescript
import http from 'http';
import express from 'express';
import { App, ExpressAdapter } from '@microsoft/teams.apps';

// 1. Create your Express app with your own routes
const expressApp = express();
const httpServer = http.createServer(expressApp);

expressApp.get('/health', (_req, res) => {
  res.json({ status: 'healthy' });
});

// 2. Wrap it in the ExpressAdapter
const adapter = new ExpressAdapter(httpServer);

// 3. Create the Teams app with the adapter
const app = new App({ httpServerAdapter: adapter });

app.on('message', async ({ send, activity }) => {
  await send(`Echo: ${activity.text}`);
});

// 4. Initialize — registers /api/messages on your Express app (does NOT start a server)
await app.initialize();

// 5. Start the server yourself
httpServer.listen(3978, () => console.log('Server ready on http://localhost:3978'));
```

> **Note:** `app.initialize()` runs each plugin's `onInit` hook but not its `onStart` hook
> `onStart` only fires from `app.start()`. When you take over the HTTP lifecycle with a custom
> adapter, plugins that do their setup in `onStart` won't run. If you're using such a plugin,
> either call `app.start()` (and let it manage the server) or invoke that plugin's `onStart`
> yourself after `app.initialize()`:
>
> ```ts
> await app.initialize();
> await myPlugin.onStart({ port: 3978 });
> ```

> See the full [Express adapter example](https://github.com/microsoft/teams.ts/tree/main/examples/http-adapters/express)
::: zone-end

::: zone pivot="typescript,python"
## Using a Different Framework

If you use a framework other than the built-in default, implement the adapter interface for your framework. The core work is in `registerRoute`  translate incoming requests to `{ body, headers }`, call the handler, and write the response back. Since you manage the server lifecycle yourself, `start`/`stop` aren't needed. And `serveStatic` is only required if you serve tabs or static pages.
::: zone-end

::: zone pivot="python"
Here is a Starlette adapter  only `register_route` is needed:

```python
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from microsoft_teams.apps.http.adapter import HttpMethod, HttpRequest, HttpResponse, HttpRouteHandler

class StarletteAdapter:
    def __init__(self, app: Starlette):
        self._app = app

    def register_route(self, method: HttpMethod, path: str, handler: HttpRouteHandler) -> None:
        # Teams only sends POST requests to your bot endpoint
        async def starlette_handler(request: Request) -> Response:
            body = await request.json()
            headers = dict(request.headers)
            result: HttpResponse = await handler(HttpRequest(body=body, headers=headers))
            if result.get("body") is not None:
                return JSONResponse(content=result["body"], status_code=result["status"])
            return Response(status_code=result["status"])

        route = Route(path, starlette_handler, methods=[method])
        self._app.routes.insert(0, route)
```

Usage:

```python
starlette_app = Starlette()
adapter = StarletteAdapter(starlette_app)
app = App(http_server_adapter=adapter)
await app.initialize()
# Start Starlette with uvicorn yourself
```

> See the full implementation: [Starlette adapter example](https://github.com/microsoft/teams.py/tree/main/examples/http-adapters/src/starlette_adapter.py)
::: zone-end

::: zone pivot="typescript"
Here is a Restify adapter  only `registerRoute` is needed:

```typescript
import restify from 'restify';
import { HttpMethod, IHttpServerAdapter, HttpRouteHandler } from '@microsoft/teams.apps';

class RestifyAdapter implements IHttpServerAdapter {
  constructor(private server: restify.Server) {
    this.server.use(restify.plugins.bodyParser());
  }

  registerRoute(method: HttpMethod, path: string, handler: HttpRouteHandler): void {
    // Teams only sends POST requests to your bot endpoint
    assert(method === 'POST', `Unsupported method: ${method}`);
    this.server.post(path, async (req: restify.Request, res: restify.Response) => {
      const response = await handler({
        body: req.body,
        headers: req.headers as Record<string, string | string[]>,
      });
      res.send(response.status, response.body);
    });
  }
}
```

Usage:

```typescript
const server = restify.createServer();
const adapter = new RestifyAdapter(server);
const app = new App({ httpServerAdapter: adapter });
await app.initialize();
server.listen(3978);
```

> See the full implementation: [Restify adapter example](https://github.com/microsoft/teams.ts/tree/main/examples/http-adapters/restify)
::: zone-end



