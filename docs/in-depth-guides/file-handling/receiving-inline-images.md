---
title: Receiving Inline Images
description: Receive images pasted into Teams messages, identify their attachments, and download their bytes with the authenticated HTTP client.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---

# Receiving Inline Images

::: zone pivot="csharp"
When a user pastes an image into the Teams compose box, the image does not arrive inside `Activity.Text`. Teams sends it as an attachment on the inbound message activity.
::: zone-end

::: zone pivot="python,typescript"
When a user pastes an image into the Teams compose box, the image does not arrive inside `activity.text`. Teams sends it as an attachment on the inbound message activity.
::: zone-end

::: zone pivot="csharp"
Inline image attachments are distinct from files attached through the compose box. They do not use the `file.download.info` content type and are not surfaced by `context.Files`.
::: zone-end

::: zone pivot="python,typescript"
Inline image attachments are distinct from files attached through the compose box. They do not use the `file.download.info` content type and are not surfaced by `ctx.files`.
::: zone-end

## Understand the attachment shape

An inbound message with an inline image typically contains two related attachments:

```json
{
  "attachments": [
    {
      "contentType": "image/png",
      "contentUrl": "https://.../v3/attachments/{id}/views/original"
    },
    {
      "contentType": "text/html",
      "content": "<p><img src=\"https://.../objects/{id}/views/imgo\" ...></p>"
    }
  ]
}
```

Use the `image/*` attachment as the canonical source of the image. Its `contentUrl` points to the downloadable image bytes.

The `text/html` attachment preserves layout context, including where the image appeared among the message's text and other content. Do not use the HTML attachment's `<img src>` URL to download the image.

## Download the image

The image attachment's `contentUrl` is authenticated rather than public. Fetch it with the app's authenticated HTTP client:


::: zone pivot="csharp"
```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Teams.Apps.Clients;
using Microsoft.Teams.Apps.Schema;

HttpClient imageClient = app.Services
    .GetRequiredService<IHttpClientFactory>()
    .CreateClient(nameof(ApiClient));

teams.OnMessage(async (context, cancellationToken) =>
{
    TeamsAttachment? image = context.Activity.Attachments?.FirstOrDefault(
        attachment =>
            attachment.ContentType is not null
            && attachment.ContentType.Value.StartsWith("image/", StringComparison.OrdinalIgnoreCase)
            && attachment.ContentUrl is not null);

    if (image?.ContentUrl is Uri contentUrl)
    {
        using HttpResponseMessage response = await imageClient.GetAsync(
            contentUrl,
            HttpCompletionOption.ResponseHeadersRead,
            cancellationToken);
        response.EnsureSuccessStatusCode();

        // Read the response body as raw image bytes.
        byte[] bytes = await response.Content.ReadAsByteArrayAsync(cancellationToken);
        string base64 = Convert.ToBase64String(bytes);

        // Pass bytes or base64 to your image-processing or model client.
    }
});
```
::: zone-end

::: zone pivot="python"
```python
import base64

from microsoft_teams.api import MessageActivity
from microsoft_teams.apps import ActivityContext


@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]) -> None:
    image = next(
        (
            attachment
            for attachment in (ctx.activity.attachments or [])
            if attachment.content_type
            and attachment.content_type.startswith("image/")
            and attachment.content_url
        ),
        None,
    )

    if image and image.content_url:
        response = await app.api.http.get(image.content_url)
        # The response content contains the image body as bytes.
        image_bytes = response.content
        image_base64 = base64.b64encode(image_bytes).decode("ascii")

        # Pass image_bytes or image_base64 to your image-processing or model client.
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ activity }) => {
  const image = activity.attachments?.find(
    (attachment) => attachment.contentType?.startsWith('image/') && attachment.contentUrl
  );

  if (image?.contentUrl) {
    // Request binary data so the client does not decode the image as text or JSON.
    const res = await app.api.http.get<ArrayBuffer>(image.contentUrl, {
      responseType: 'arraybuffer',
    });

    const bytes = Buffer.from(res.data);
    const base64 = bytes.toString('base64');

    // Pass `bytes` or `base64` to your image-processing or model client.
  }
});
```
::: zone-end


The example buffers the complete image in memory. Keep the byte representation when your downstream API accepts it, or convert it to base64 when required by an image-processing or model API.
