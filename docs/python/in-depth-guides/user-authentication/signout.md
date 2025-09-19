---
title: Signing Out (Python)
description: Learn about Signing Out (Python)
ms.topic: how-to
ms.date: 09/18/2025
---

# Signing Out (Python)

Sign a user out by calling the `sign_out` method to discard the cached access token in the Bot Framework token service.

```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    ctx.logger.info("User requested sign-in.")
    if ctx.is_signed_in:
        await ctx.send("You are already signed in. Logging you out.")
        await ctx.sign_out()

```
