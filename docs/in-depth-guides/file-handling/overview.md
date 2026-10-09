---
title: File and Image Handling
description: Learn how your Teams app receives files and inline images, reads their bytes, and sends images back.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 10/09/2026
---

# File and Image Handling

This section covers how your app receives files and inline images and reads their bytes, and how it sends images back.

> [!NOTE]
> Preview. The high-level file API is being rolled out incrementally. Today it supports **receiving** files attached to messages via the TypeScript, Python, and C# SDKs: in personal (1:1) chats for every agent, and soon in group chats and channels for agentic users. Inline images use the raw activity attachments instead.

## Files vs. attachments

::: zone pivot="csharp"
In personal scope, `Activity.Attachments` carries every non-text part: files the user attached, inline images, Adaptive Cards, `@mentions`, link previews, and other content the client or the platform adds. A **file** is the specific subset of attachments that describes a document the user attached, one whose `ContentType` is `file.download.info`.
::: zone-end

::: zone pivot="python"
In personal scope, `activity.attachments` carries every non-text part: files the user attached, inline images, Adaptive Cards, `@mentions`, link previews, and other content the client or the platform adds. A **file** is the specific subset of attachments that describes a document the user attached, one whose `content_type` is `file.download.info`.
::: zone-end

::: zone pivot="typescript"
In personal scope, `activity.attachments` carries every non-text part: files the user attached, inline images, Adaptive Cards, `@mentions`, link previews, and other content the client or the platform adds. A **file** is the specific subset of attachments that describes a document the user attached, one whose `contentType` is `file.download.info`.
::: zone-end

::: zone pivot="csharp"
The `context.Files` accessor is the attached-file view over that raw array. It maps each attached file to a lazy handle you can download from, and skips everything else. The original `Activity.Attachments` array is always available when you need the raw payload or a non-file attachment.
::: zone-end

::: zone pivot="python,typescript"
The `ctx.files` accessor is the attached-file view over that raw array. It maps each attached file to a lazy handle you can download from, and skips everything else. The original `activity.attachments` array is always available when you need the raw payload or a non-file attachment.
::: zone-end

An **inline image** is an image attachment with an authenticated download URL, commonly paired with an HTML attachment that describes where the image appeared in the composed message. Inline images are not surfaced by the high-level file API.

Sending works similarly: an image you send is an attachment whose content type is an image MIME type, which is why it renders inline rather than arriving as a document.

## In this section

- **[Receiving Files](./receiving-files.md)** — read files a user attaches to a message, stream or download their bytes, and handle unsupported scopes, expired links, and agentic users.
- **[Receiving Inline Images](./receiving-inline-images.md)** — identify images pasted into a message and download their bytes with the authenticated HTTP client.
- **[Sending Inline Images](./sending-inline-images.md)** — send an image that renders directly in the conversation, from a hosted URL or as base64-encoded bytes, within the platform's size and format limits.

## Resources

- [Files in Teams bots](/microsoftteams/platform/bots/how-to/bots-filesv4)
- [Picture messages](/microsoftteams/platform/bots/how-to/conversations/conversation-messages#use-picture-messages)
