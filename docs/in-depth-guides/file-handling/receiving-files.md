---
title: Receiving Files
description: Read files a user attaches to a message in your Teams app. List attached files on an incoming message, download or stream their bytes, and handle expired links and unsupported scopes.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---

# Receiving Files

::: zone pivot="csharp"
Teams users can send files to agents by attaching them to chat messages. When users send files to an agent in 1:1 chat, or to an agentic user in a group chat or channel, they arrive as part of the context of the received message activity. `context.Files` provides lazy access to the metadata and bytes of each attached file.
::: zone-end

::: zone pivot="python,typescript"
Teams users can send files to agents by attaching them to chat messages. When users send files to an agent in 1:1 chat, or to an agentic user in a group chat or channel, they arrive as part of the context of the received message activity. `ctx.files` provides lazy access to the metadata and bytes of each attached file.
::: zone-end

An attached file is not delivered inline with the message. Teams stores the file in OneDrive or SharePoint and hands your agent a small metadata attachment describing it, including a short-lived, pre-authorized URL in personal scopes for traditional bots, while agentic users must make a Graph call via the `contentUrl`. Reading the contents means fetching the bytes from either URL over the network, so the download itself is deferred until explicitly called.

This API covers file downloads in **personal (1:1) chats** for every agent. Agentic users can also download files in **group chats** and **channels** starting in version 2.2.0; traditional bots don't receive files there. See [Conversation scope support](#conversation-scope-support).

## Enable file support in your manifest for traditional bots

::: zone pivot="csharp"
Teams only offers users the option to attach a file in 1:1 with a bot when your app manifest opts in. Set `supportsFiles` to `true` on your bot entry; without it the compose box shows no attach affordance for your agent, no file reaches your handler, and `context.Files.ListAsync()` is always empty:
::: zone-end

::: zone pivot="python,typescript"
Teams only offers users the option to attach a file in 1:1 with a bot when your app manifest opts in. Set `supportsFiles` to `true` on your bot entry; without it the compose box shows no attach affordance for your agent, no file reaches your handler, and `ctx.files.list()` is always empty:
::: zone-end

```json
"bots": [
  {
    "botId": "${{BOT_ID}}",
    "scopes": ["personal"],
    "supportsFiles": true
  }
]
```

## Enable file support on the blueprint for agentic users

Agentic users need a Graph file permission consented on the agent's blueprint by an administrator in order to access files. See [inheritable permissions](/entra/agent-id/concept-inheritable-permissions) for how an agent acquires those scopes.

## Access attached files

::: zone pivot="csharp"
The accessor `context.Files` is available on every activity context, but only inbound message activities carry attachments, so it is empty everywhere else. Use `ListAsync()` to get all files attached to the current message, or `FirstAsync()` for the common single-file case. Both hand back the file's metadata rather than its contents, so listing is cheap even when the attached files are large:
::: zone-end

::: zone pivot="python,typescript"
The accessor `ctx.files` is available on every activity context, but only inbound message activities carry attachments, so it is empty everywhere else. Use `list()` to get all files attached to the current message, or `first()` for the common single-file case. Both hand back the file's metadata rather than its contents, so listing is cheap even when the attached files are large:
::: zone-end


::: zone pivot="csharp"
```csharp
teamsApp.OnMessage(async (context, cancellationToken) =>
{
    IList<IncomingFile> attached = await context.Files.ListAsync(cancellationToken);

    if (attached.Count == 0)
    {
        await context.ReplyAsync("Send me a file and I will read it.", cancellationToken);
        return;
    }

    string names = string.Join(", ", attached.Select(f => f.Name));
    await context.ReplyAsync($"You sent {attached.Count} file(s): {names}", cancellationToken);
});
```
::: zone-end

::: zone pivot="python"
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]) -> None:
    attached = await ctx.files.list()

    if not attached:
        await ctx.reply("Send me a file and I will read it.")
        return

    names = ", ".join(f.name for f in attached)
    await ctx.reply(f"You sent {len(attached)} file(s): {names}")
```
::: zone-end

::: zone pivot="typescript"
```typescript
app.on('message', async ({ files, send }) => {
  const attached = await files.list();

  if (attached.length === 0) {
    await send('Send me a file and I will read it.');
    return;
  }

  await send(`You sent ${attached.length} file(s): ${attached.map((f) => f.name).join(', ')}`);
});
```
::: zone-end


::: zone pivot="csharp"
Listing with `ListAsync()` returns the attached files in the same order they arrived. It never throws: activities with no attachments (or non-message activities) return an empty list, and malformed file entries are skipped rather than failing the whole batch.
::: zone-end

::: zone pivot="python,typescript"
Listing with `list()` returns the attached files in the same order they arrived. It never throws: activities with no attachments (or non-message activities) return an empty list, and malformed file entries are skipped rather than failing the whole batch.
::: zone-end


::: zone pivot="csharp"
```csharp
IncomingFile? file = await context.Files.FirstAsync(cancellationToken);

if (file is not null)
{
    await context.ReplyAsync($"Reading {file.Name}...", cancellationToken);
}
```
::: zone-end

::: zone pivot="python"
```python
file = await ctx.files.first()

if file:
    await ctx.reply(f"Reading {file.name}...")
```
::: zone-end

::: zone pivot="typescript"
```typescript
const file = await files.first();

if (file) {
  await send(`Reading ${file.name}...`);
}
```
::: zone-end


### File metadata

::: zone pivot="csharp,python"
Each `IncomingFile` carries metadata describing the file, populated from what the platform reports:
::: zone-end

::: zone pivot="typescript"
Each `IIncomingFile` carries metadata describing the file, populated from what the platform reports:
::: zone-end


::: zone pivot="csharp"
| Property | Description |
|---|---|
| `UniqueId` | The OneDrive/SharePoint drive-item id, when the platform provides it. Present only for files backed by ODSP storage. |
| `Name` | File name including its extension (e.g. `report.pdf`). |
| `Extension` | File extension without the dot (e.g. `pdf`), from the platform-supplied `fileType`. Absent when the platform omits it. |
| `ContentType` | The file's MIME type, when the source provides one. Always unset for files received from a bot activity (every file today): the `file.download.info` attachment carries no MIME type, only the extension surfaced as `Extension`. To learn the type of the bytes you actually received, read `ContentType` on the downloaded file, which is resolved from the download response. |
| `Scope` | The conversation scope the file arrived in (`personal`, `groupChat`, or `channel`). |
| `Source` | Where the SDK found the file. Currently always `botActivity`. |
| `ContentUrl` | A browsable link to the file in OneDrive/SharePoint, when known. Not a fetchable download URL. |
| `Raw` | The original wire attachment (the metadata object, not the bytes) — see [Access the raw attachment](#access-the-raw-attachment). |
::: zone-end

::: zone pivot="python"
| Property | Description |
|---|---|
| `unique_id` | The OneDrive/SharePoint drive-item id, when the platform provides it. Present only for files backed by ODSP storage. |
| `name` | File name including its extension (e.g. `report.pdf`). |
| `extension` | File extension without the dot (e.g. `pdf`), from the platform-supplied `file_type`. Absent when the platform omits it. |
| `content_type` | The file's MIME type, when the source provides one. Always unset for files received from a bot activity (every file today): the `file.download.info` attachment carries no MIME type, only the extension surfaced as `extension`. To learn the type of the bytes you actually received, read `content_type` on the downloaded file, which is resolved from the download response. |
| `scope` | The conversation scope the file arrived in (`personal`, `groupChat`, or `channel`). |
| `source` | Where the SDK found the file. Currently always `botActivity`. |
| `content_url` | A browsable link to the file in OneDrive/SharePoint, when known. Not a fetchable download URL. |
| `raw` | The original wire attachment (the metadata object, not the bytes) — see [Access the raw attachment](#access-the-raw-attachment). |
::: zone-end

::: zone pivot="typescript"
| Property | Description |
|---|---|
| `uniqueId` | The OneDrive/SharePoint drive-item id, when the platform provides it. Present only for files backed by ODSP storage. |
| `name` | File name including its extension (e.g. `report.pdf`). |
| `extension` | File extension without the dot (e.g. `pdf`), from the platform-supplied `fileType`. Absent when the platform omits it. |
| `contentType` | The file's MIME type, when the source provides one. Always unset for files received from a bot activity (every file today): the `file.download.info` attachment carries no MIME type, only the extension surfaced as `extension`. To learn the type of the bytes you actually received, read `contentType` on the downloaded file, which is resolved from the download response. |
| `scope` | The conversation scope the file arrived in (`personal`, `groupChat`, or `channel`). |
| `source` | Where the SDK found the file. Currently always `botActivity`. |
| `contentUrl` | A browsable link to the file in OneDrive/SharePoint, when known. Not a fetchable download URL. |
| `raw` | The original wire attachment (the metadata object, not the bytes) — see [Access the raw attachment](#access-the-raw-attachment). |
::: zone-end


## Read a file

::: zone pivot="csharp"
The most common path is `DownloadAsync()`, which fetches the whole file and buffers it into an in-memory copy you own:
::: zone-end

::: zone pivot="python,typescript"
The most common path is `download()`, which fetches the whole file and buffers it into an in-memory copy you own:
::: zone-end


::: zone pivot="csharp"
```csharp
IncomingFile? file = await context.Files.FirstAsync(cancellationToken);

if (file is not null)
{
    DownloadedFile downloaded = await file.DownloadAsync(cancellationToken);

    await context.ReplyAsync($"Downloaded {downloaded.Filename} ({downloaded.Bytes.Length} bytes, {downloaded.ContentType})", cancellationToken);
}
```
::: zone-end

::: zone pivot="python"
```python
file = await ctx.files.first()

if file:
    downloaded = await file.download()

    await ctx.reply(f"Downloaded {downloaded.filename} ({len(downloaded.bytes)} bytes, {downloaded.content_type})")
```
::: zone-end

::: zone pivot="typescript"
```typescript
const file = await files.first();

if (file) {
  const downloaded = await file.download();

  await send(`Downloaded ${downloaded.filename} (${downloaded.bytes.length} bytes, ${downloaded.contentType})`);
}
```
::: zone-end


::: zone pivot="csharp"
For text files, `TextAsync()` is a shortcut for `DownloadAsync()` followed by decoding:
::: zone-end

::: zone pivot="python,typescript"
For text files, `text()` is a shortcut for `download()` followed by decoding:
::: zone-end


::: zone pivot="csharp"
```csharp
IncomingFile? file = await context.Files.FirstAsync(cancellationToken);

if (file is not null)
{
    string contents = await file.TextAsync(cancellationToken: cancellationToken);
    await context.ReplyAsync($"The file starts with: {contents[..Math.Min(100, contents.Length)]}", cancellationToken);
}
```
::: zone-end

::: zone pivot="python"
```python
file = await ctx.files.first()

if file:
    contents = await file.text()
    await ctx.reply(f"The file starts with: {contents[:100]}")
```
::: zone-end

::: zone pivot="typescript"
```typescript
const file = await files.first();

if (file) {
  const contents = await file.text();
  await send(`The file starts with: ${contents.slice(0, 100)}`);
}
```
::: zone-end


::: zone pivot="csharp"
> [!NOTE]
> Decoding with `TextAsync()` reads the downloaded bytes as UTF-8 by default, and is lossy: bytes that are not valid for the encoding become the replacement character (`U+FFFD`) instead of throwing. To decode a different encoding, pass an `Encoding` (e.g. `file.TextAsync(Encoding.Latin1)`). For binary files, read the raw bytes instead.

::: zone-end

::: zone pivot="python"
> [!NOTE]
> Decoding with `text()` reads the downloaded bytes as UTF-8 by default, and is lossy: bytes that are not valid for the encoding become the replacement character (`U+FFFD`) instead of throwing. To decode a different encoding, pass an encoding name (e.g. `file.text("latin1")`). For binary files, read the raw bytes instead.

::: zone-end

::: zone pivot="typescript"
> [!NOTE]
> Decoding with `text()` reads the downloaded bytes as UTF-8 by default, and is lossy: bytes that are not valid for the encoding become the replacement character (`U+FFFD`) instead of throwing. To decode a different encoding, pass an encoding name (e.g. `file.text('latin1')`). For binary files, read the raw bytes instead.

::: zone-end

::: zone pivot="csharp"
To save a file to disk without holding it all in memory, use `SaveAsAsync()`, which streams straight to the path:
::: zone-end

::: zone pivot="python"
To save a file to disk without holding it all in memory, use `save_as()`, which streams straight to the path:
::: zone-end

::: zone pivot="typescript"
To save a file to disk without holding it all in memory, use `saveAs()`, which streams straight to the path:
::: zone-end


::: zone pivot="csharp"
```csharp
await file.SaveAsAsync("./downloads/report.pdf", cancellationToken);
```
::: zone-end

::: zone pivot="python"
```python
await file.save_as("./downloads/report.pdf")
```
::: zone-end

::: zone pivot="typescript"
```typescript
await file.saveAs('./downloads/report.pdf');
```
::: zone-end


The path is resolved relative to the process working directory, overwrites an existing file, and does not create missing parent directories.

::: zone pivot="csharp"
> [!WARNING]
> A file's `Name` comes off the wire and is set by the uploader, so treat it as untrusted input rather than a destination. It may contain `/` or `\`, a drive or UNC prefix, or `..` segments, and no sanitization is performed on the developer's behalf. Therefore, no assumptions are made related to the destination like illegal characters based on operating system or naming collisions.

::: zone-end

::: zone pivot="python,typescript"
> [!WARNING]
> A file's `name` comes off the wire and is set by the uploader, so treat it as untrusted input rather than a destination. It may contain `/` or `\`, a drive or UNC prefix, or `..` segments, and no sanitization is performed on the developer's behalf. Therefore, no assumptions are made related to the destination like illegal characters based on operating system or naming collisions.

::: zone-end

::: zone pivot="csharp"
For large files or streaming pipelines, `StreamAsync()` hands you the raw byte stream so you can process it as it arrives:
::: zone-end

::: zone pivot="python,typescript"
For large files or streaming pipelines, `stream()` hands you the raw byte stream so you can process it as it arrives:
::: zone-end


::: zone pivot="csharp"
```csharp
await using Stream stream = await file.StreamAsync(cancellationToken);

byte[] buffer = new byte[8192];
int read;
while ((read = await stream.ReadAsync(buffer, cancellationToken)) > 0)
{
    // process only the bytes read this iteration (e.g. pipe to a parser)
    ReadOnlyMemory<byte> chunk = buffer.AsMemory(0, read);
}
```
::: zone-end

::: zone pivot="python"
```python
async for chunk in file.stream():
    ...  # process each chunk (e.g. pipe to a parser)
```
::: zone-end

::: zone pivot="typescript"
```typescript
const stream = await file.stream();

for await (const chunk of stream) {
  // process each chunk (e.g. pipe to a parser)
}
```
::: zone-end


::: zone pivot="csharp"
An `IncomingFile` handle holds no cached bytes: each call to `DownloadAsync()`, `TextAsync()`, `StreamAsync()`, or `SaveAsAsync()` fetches the file again. This matters because a file's download link is short-lived: the URL embeds its own pre-authorized `tempauth` credential, which can expire between reads. To read the same file several ways, call `DownloadAsync()` once and reuse the downloaded file it returns, which is a point-in-time copy whose readers never re-fetch:
::: zone-end

::: zone pivot="python"
An `IncomingFile` handle holds no cached bytes: each call to `download()`, `text()`, `stream()`, or `save_as()` fetches the file again. This matters because a file's download link is short-lived: the URL embeds its own pre-authorized `tempauth` credential, which can expire between reads. To read the same file several ways, call `download()` once and reuse the downloaded file it returns, which is a point-in-time copy whose readers never re-fetch:
::: zone-end

::: zone pivot="typescript"
An `IIncomingFile` handle holds no cached bytes: each call to `download()`, `text()`, `stream()`, or `saveAs()` fetches the file again. This matters because a file's download link is short-lived: the URL embeds its own pre-authorized `tempauth` credential, which can expire between reads. To read the same file several ways, call `download()` once and reuse the downloaded file it returns, which is a point-in-time copy whose readers never re-fetch:
::: zone-end


::: zone pivot="csharp"
```csharp
DownloadedFile downloaded = await file.DownloadAsync(cancellationToken);

string text = downloaded.Text();                               // decode as UTF-8
byte[] bytes = downloaded.Bytes;                               // the raw bytes
await downloaded.SaveAsAsync("./copy.bin", cancellationToken); // write to disk, no re-fetch
```
::: zone-end

::: zone pivot="python"
```python
downloaded = await file.download()

text = downloaded.text()               # decode as UTF-8
data = downloaded.bytes                # the raw bytes
await downloaded.save_as("./copy.bin") # write to disk, no re-fetch
```
::: zone-end

::: zone pivot="typescript"
```typescript
const downloaded = await file.download();

const text = downloaded.text();          // decode as UTF-8
const buffer = downloaded.arrayBuffer(); // the raw bytes
await downloaded.saveAs('./copy.bin');   // write to disk, no re-fetch
```
::: zone-end



::: zone pivot="csharp"
| Property / method | Description |
|---|---|
| `Bytes` | The buffered file bytes as a `byte[]`. |
| `ContentType` | MIME type resolved from the download response header, or the incoming file's metadata type if the response omits one. Falls back to `application/octet-stream` when neither provides a type, so this is never empty. |
| `Filename` | The resolved file name. |
| `SourceUrl` | The URL the bytes were fetched from. |
| `Text(encoding?)` | Decode the bytes as UTF-8 (or a given encoding). Lossy; never throws. |
| `SaveAsAsync(path)` | Write the buffered bytes to a local path (no re-fetch). |
::: zone-end

::: zone pivot="python"
| Property / method | Description |
|---|---|
| `bytes` | The buffered file bytes. |
| `content_type` | MIME type resolved from the download response header, or the incoming file's metadata type if the response omits one. Falls back to `application/octet-stream` when neither provides a type, so this is never empty. |
| `filename` | The resolved file name. |
| `source_url` | The URL the bytes were fetched from. |
| `text(encoding="utf-8")` | Decode the bytes as UTF-8 (or a given encoding). Lossy; never throws. |
| `save_as(path)` | Write the buffered bytes to a local path (no re-fetch). |
::: zone-end

::: zone pivot="typescript"
| Property / method | Description |
|---|---|
| `bytes` | The buffered file bytes as a `Uint8Array`. |
| `contentType` | MIME type resolved from the download response header, or the incoming file's metadata type if the response omits one. Falls back to `application/octet-stream` when neither provides a type, so this is never empty. |
| `filename` | The resolved file name. |
| `sourceUrl` | The URL the bytes were fetched from. |
| `text(encoding?)` | Decode the bytes as UTF-8 (or a given encoding). Lossy; never throws. |
| `arrayBuffer()` | Return the bytes as an `ArrayBuffer`. |
| `saveAs(path)` | Write the buffered bytes to a local path (no re-fetch). |
::: zone-end


## Handle errors

Byte retrieval can fail for a few well-defined reasons. All of them share a common base error, so a single check catches any of them and a new one can be added later without callers changing:


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.Apps.Files;
```
::: zone-end

::: zone pivot="python"
```python
from microsoft_teams.apps import (
    FileAccessError,
    FileCredentialError,
    FileError,
    FileScopeNotSupportedError,
    FileUrlExpiredError,
)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import {
  FileAccessError,
  FileCredentialError,
  FileError,
  FileScopeNotSupportedError,
  FileUrlExpiredError,
} from '@microsoft/teams.apps';
```
::: zone-end


| Error | Raised when | Carries |
|---|---|---|
| **File URL expired** | The short-lived, pre-authorized download link lapsed before the bytes were fetched. | `reason`: <br/> **first fetch**, the link had already lapsed so no bytes were retrieved; <br /> **re-read**, an earlier download succeeded, but a later read through the same handle came after expiry. Avoid this by downloading once and reusing the downloaded file. |
| **No Graph credential** | The Graph read an agentic user's file needs was ruled out before the request, because no credential was available. | `actor`<sup><a href="#actor">2</a></sup>: the identity a credential was being resolved for. <br /> `cause`: why acquiring the token failed, when it failed rather than simply returning nothing. |
| **File access denied** | The Graph read an agentic user's file needs was refused by the storage service. | `status`: `401` when the token itself was rejected, `403` when the identity lacks the grant<sup><a href="#access-denied">1</a></sup>. <br/> `actor`<sup><a href="#actor">2</a></sup>: the identity that was refused. <br /> `details`: what the service said, if anything. |
| **File scope not supported** | Download was called on a file from a conversation scope this API does not yet support, meaning anything other than personal, group chat, or channel for an agentic user. A traditional bot receives files only in personal (1:1) chats. | `scope`: the conversation scope. |

<sup id="access-denied">1</sup> A **`403`** deliberately collapses causes the SDK cannot differentiate: an unconsented permission, a file the identity was never granted, and an item that does not exist all arrive the same way. There is no separate "file not found" case to branch on; `details` carries the service's own text for diagnosis. In a standard channel, a file picked from OneDrive or SharePoint, rather than uploaded, can be refused this way, because Teams does not grant the agent access to the picked item (see [Group chats and channels](#group-chats-and-channels)). A `401` is a different problem, which is why the status is reported rather than folded in: the token was rejected, so the fix is the token rather than the sharing.

<sup id="actor">2</sup> `actor` names which identity the read was attempted as. The SDK chooses it, and today there are two:

- **Agentic user**, chosen whenever the inbound activity carries an agentic identity. An agentic user reads as itself rather than as an app. Its Graph scopes come from its blueprint's inheritable permissions set by a tenant administrator or from a direct grant by a user with permissions to share it.
- **App**, chosen for every other activity. Graph file retrieval is supported for agentic users, which read as their own identity; an app identity and user-delegated permissions may be used, but are not supported through the SDK at this time.

The actor is absent when the failure came before any identity was selected, which is the case when the app has no Graph route configured at all.

A transport or service failure, such as a Graph 5xx, is not one of these and surfaces as an ordinary error.

You may add error handling based on the type of error:


::: zone pivot="csharp"
```csharp
try
{
    DownloadedFile downloaded = await file.DownloadAsync(cancellationToken);
    // ...
}
catch (FileUrlExpiredException err) when (err.Reason == FileUrlExpiredReason.FirstFetch)
{
    await context.ReplyAsync("That file link has expired before it could be read.", cancellationToken);
}
catch (FileCredentialException err)
{
    await context.ReplyAsync($"Could not read that file as {err.Actor?.ToString() ?? "the identity used"}: no Graph credential was available.", cancellationToken);
}
catch (FileAccessException err)
{
    await context.ReplyAsync($"Could not read that file as {err.Actor?.ToString() ?? "the identity used"}: the service returned {err.Status}.", cancellationToken);
}
catch (FileScopeNotSupportedException err)
{
    await context.ReplyAsync($"Downloading files from {err.Scope} conversations is not supported yet.", cancellationToken);
}
catch (FileException)
{
    // Any future inbound-file failure lands here rather than escaping unhandled.
    await context.ReplyAsync("That file could not be read.", cancellationToken);
}
```
::: zone-end

::: zone pivot="python"
```python
try:
    downloaded = await file.download()
    # ...
except FileUrlExpiredError as err:
    if err.reason == "first_fetch":
        await ctx.reply("That file link has expired before it could be read.")
except FileCredentialError as err:
    await ctx.reply(f"Could not read that file as {err.actor or 'the identity used'}: no Graph credential was available.")
except FileAccessError as err:
    await ctx.reply(f"Could not read that file as {err.actor or 'the identity used'}: the service returned {err.status}.")
except FileScopeNotSupportedError as err:
    await ctx.reply(f"Downloading files from {err.scope} conversations is not supported yet.")
except FileError:
    # Any future inbound-file failure lands here rather than escaping unhandled.
    await ctx.reply("That file could not be read.")
```
::: zone-end

::: zone pivot="typescript"
```typescript
try {
  const downloaded = await file.download();
  // ...
} catch (err) {
  if (err instanceof FileUrlExpiredError && err.reason === 'firstFetch') {
    await send('That file link has expired before it could be read.');
  } else if (err instanceof FileCredentialError) {
    await send(`Could not read that file as ${err.actor ?? 'the identity used'}: no Graph credential was available.`);
  } else if (err instanceof FileAccessError) {
    await send(`Could not read that file as ${err.actor ?? 'the identity used'}: the service returned ${err.status}.`);
  } else if (err instanceof FileScopeNotSupportedError) {
    await send(`Downloading files from ${err.scope} conversations is not supported yet.`);
  } else if (err instanceof FileError) {
    // Any future inbound-file failure lands here rather than escaping unhandled.
    await send('That file could not be read.');
  }
}
```
::: zone-end


## Access the raw attachment

::: zone pivot="csharp"
Every file the accessor returns retains its original wire attachment on `Raw`, for diagnostics or for the rare case where you need a field the typed surface does not expose:
::: zone-end

::: zone pivot="python,typescript"
Every file the accessor returns retains its original wire attachment on `raw`, for diagnostics or for the rare case where you need a field the typed surface does not expose:
::: zone-end


::: zone pivot="csharp"
```csharp
using System.Text.Json;

IncomingFile? file = await context.Files.FirstAsync(cancellationToken);

if (file is not null)
{
    // `Raw` is the untyped wire attachment: the escape hatch when you need a
    // field the typed surface does not expose. Here we serialize the whole
    // attachment to inspect exactly what the platform sent.
    string wire = JsonSerializer.Serialize(file.Raw);
    await context.ReplyAsync($"raw attachment: {wire}", cancellationToken);
}
```
::: zone-end

::: zone pivot="python"
```python
file = await ctx.files.first()

if file:
    # `raw` is the untyped wire attachment: the escape hatch when you need a
    # field the typed surface does not expose. Here we log the whole attachment
    # to inspect exactly what the platform sent.
    ctx.logger.debug("raw file attachment: %s", file.raw)
```
::: zone-end

::: zone pivot="typescript"
```typescript
const file = await files.first();

if (file) {
  // `raw` is the untyped wire attachment: the escape hatch when you need a
  // field the typed surface does not expose. Here we log the whole attachment
  // to inspect exactly what the platform sent.
  log.debug('raw file attachment', file.raw);
}
```
::: zone-end


::: zone pivot="csharp"
Attachments that are **not** files (inline images, Adaptive Cards, mentions, link previews), and malformed file entries the accessor skips, are not returned by `ListAsync()` and therefore have no `IncomingFile`. Reach those directly through `context.Activity.Attachments`. For image attachments, see [Receiving Inline Images](./receiving-inline-images.md).
::: zone-end

::: zone pivot="python"
Attachments that are **not** files (inline images, Adaptive Cards, mentions, link previews), and malformed file entries the accessor skips, are not returned by `list()` and therefore have no `IncomingFile`. Reach those directly through `ctx.activity.attachments`. For image attachments, see [Receiving Inline Images](./receiving-inline-images.md).
::: zone-end

::: zone pivot="typescript"
Attachments that are **not** files (inline images, Adaptive Cards, mentions, link previews), and malformed file entries the accessor skips, are not returned by `list()` and therefore have no `IIncomingFile`. Reach those directly through `ctx.activity.attachments`. For image attachments, see [Receiving Inline Images](./receiving-inline-images.md).
::: zone-end

## Conversation scope support

::: zone pivot="csharp"
Listing with `ListAsync()` surfaces the files Teams delivers on the incoming activity. What gets delivered and downloaded depends on the conversation scope and on whether your agent is a traditional bot or an agentic user.
::: zone-end

::: zone pivot="python,typescript"
Listing with `list()` surfaces the files Teams delivers on the incoming activity. What gets delivered and downloaded depends on the conversation scope and on whether your agent is a traditional bot or an agentic user.
::: zone-end

### Personal chats

Downloading in personal (1:1) chats depends on the URL the platform sends, not on who is reading. A traditional bot receives a short-lived, pre-authorized download link, which the SDK fetches directly with no token attached.

An **agentic user** receives no pre-authorized link. Its attachment data carries only a `contentUrl` locating the item in OneDrive or SharePoint, so the SDK resolves the bytes through Microsoft Graph's `/shares` endpoint using the agent's own credential. The call behavior is unchanged from above; only the downloading route underneath differs.

::: zone pivot="csharp"
If an agentic user has no usable Graph credential, the read fails with `FileCredentialException`; if the storage service refuses the read, for example because the file isn't shared with the agent, it fails with `FileAccessException` (see [Handle errors](#handle-errors)). Both name the identity involved rather than reporting the file as missing.
::: zone-end

::: zone pivot="python,typescript"
If an agentic user has no usable Graph credential, the read fails with `FileCredentialError`; if the storage service refuses the read, for example because the file isn't shared with the agent, it fails with `FileAccessError` (see [Handle errors](#handle-errors)). Both name the identity involved rather than reporting the file as missing.
::: zone-end

### Group chats and channels

> [!NOTE]
> Coming Soon. Receiving files as an agentic user in group chats and channels is planned for the next SDK release, version 2.2.0.

::: zone pivot="csharp"
In **group chats** and **channels**, the attachment has the same shape, carrying only a `contentUrl`. The SDK reads it through Graph `/shares` using the agent's own credential. Your handler code is the same too: call `ListAsync()` and then `DownloadAsync()`, and the SDK chooses the agent's credential.
::: zone-end

::: zone pivot="python,typescript"
In **group chats** and **channels**, the attachment has the same shape, carrying only a `contentUrl`. The SDK reads it through Graph `/shares` using the agent's own credential. Your handler code is the same too: call `list()` and then `download()`, and the SDK chooses the agent's credential.
::: zone-end

Outside personal chats, only messages that @mention the agent reach it, so a file posted without an @mention is never delivered.

A file can be attached by uploading it from the device or by picking it from OneDrive or SharePoint. Whether each kind downloads depends on the conversation:

::: zone pivot="csharp"
- In **group chats**, both kinds download.
- In **private channels**, both kinds download. A picked file is delivered as a copy in the channel's site.
- In **non-private channels**, files uploaded from the device download, but a picked file can be refused, because Teams does not grant the agent access to the picked item. The refusal surfaces as `FileAccessException` with a `403` status (see [Handle errors](#handle-errors)).
::: zone-end

::: zone pivot="python,typescript"
- In **group chats**, both kinds download.
- In **private channels**, both kinds download. A picked file is delivered as a copy in the channel's site.
- In **non-private channels**, files uploaded from the device download, but a picked file can be refused, because Teams does not grant the agent access to the picked item. The refusal surfaces as `FileAccessError` with a `403` status (see [Handle errors](#handle-errors)).
::: zone-end

The SDK reads each file as the agent, so a download succeeds only when the agent already has access to that file. A sharing link that doesn't name the agent, such as an "Anyone" link or an organization-wide link, doesn't give it that access.

Files attached to a reply in a channel thread follow the same rules as files on a new post.

::: zone pivot="csharp"
A traditional bot cannot receive files in group chats or channels: the attached file isn't delivered to it on the activity, so `ListAsync()` doesn't surface it.
::: zone-end

::: zone pivot="python,typescript"
A traditional bot cannot receive files in group chats or channels: the attached file isn't delivered to it on the activity, so `list()` doesn't surface it.
::: zone-end

## Next steps

- See [Files in Teams bots](/microsoftteams/platform/bots/how-to/bots-filesv4) for the platform-side file model.
