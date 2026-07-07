---
title: 'Enhance the Teams Experience'
description: 'Round out a Teams agent reply with suggested follow-up prompts, inline citations from tool middleware, the AI-generated label, and a custom feedback form  then assemble the full message handler.'
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 06/29/2026
---
<!-- markdownlint-disable-next-line MD024 -->

# Enhance the Teams Experience

::: zone pivot="csharp"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="python"

You can enrich the agent output into a more Teams-native experience — adding structure, interactivity, and metadata on top of the generated text. This guide builds on the agent from [Build an agent in Teams](build-agent-maf.md).

## Streaming

Streaming allows the agent to deliver responses to Teams incrementally as theyre generated,
rather than waiting for the full reply to complete.
Each chunk of text is appended to the stream as it arrives.
```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    async for chunk in agent.run(ctx.activity.text or "", stream=True):
        if chunk.text:
            ctx.stream.emit(chunk.text)
```

See [Streaming](../../essentials/sending-messages/overview.md#streaming) for the full story on how Teams renders chunks and the constraints on stream lifecycle.

## AI-generated label

`add_ai_generated()` marks the message as system-generated, ensuring it is clearly labeled as AI output within Teams.

```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    async for chunk in agent.run(ctx.activity.text or "", stream=True):
        if chunk.text:
            ctx.stream.emit(chunk.text)

    # highlight-success-start
    reply = MessageActivityInput().add_ai_generated()
    ctx.stream.emit(reply)
    # highlight-success-end
```

:::image type="content" source="../../assets/screenshots/streaming.gif" alt-text="Screenshot shows streaming."lightbox="../../assets/screenshots/streaming.gif":::

## User feedback

`add_feedback(mode="custom")` enables built-in thumbs up/down controls on the reply and lets you surface a custom feedback form when users respond.

```python
@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    async for chunk in agent.run(ctx.activity.text or "", stream=True):
        if chunk.text:
            ctx.stream.emit(chunk.text)

    reply = (MessageActivityInput().add_ai_generated()
            # highlight-success-start
            .add_feedback(mode="custom")
            # highlight-success-end
    )
    ctx.stream.emit(reply)
```

See [Feedback](../feedback.md) for the full form-handling story  capturing the submission, persisting it, and following up with the user.

## Clarification cards

When the agent calls the `request_clarification` tool (from [Build an agent](build-agent-maf.md#adding-a-local-tool)), the reply is a card, not text. The model still produces a short wrap-up after the tool returns, so discard the streamed text and send only the card. Clearing the stream's accumulated text before emitting the card-only activity keeps the turn to a single clean reply.
```python
async def _run_agent_and_reply(ctx, session, text: str) -> None:
    cards: list[AdaptiveCard] = []
    pending_cards.set(cards)

    full_text = ""
    async for chunk in agent.run(text, session=session, stream=True):
        if chunk.text:
            ctx.stream.emit(chunk.text)
            full_text += chunk.text

    if cards:
        # Clarification card — discard any streamed text, then emit card-only.
        ctx.stream.clear_text()
        reply = MessageActivityInput().add_ai_generated()
        for card in cards:
            reply.add_card(card)
        ctx.stream.emit(reply)
    else:
        # normal reply: attach follow-ups, citations, feedback (below).
        ...
```

The user's choice is captured by a card-action handler and fed straight back into the agent as the next turn:

```python
@app.on_card_action_execute(CLARIFICATION_VERB)
async def handle_clarification(ctx: ActivityContext[AdaptiveCardInvokeActivity]) -> AdaptiveCardInvokeResponse:
    choice = (ctx.activity.value.action.data or {}).get(CLARIFICATION_INPUT_ID, "")
    if choice:
        session = _sessions[ctx.activity.conversation.id]
        await _run_agent_and_reply(ctx, session, choice)
    return AdaptiveCardActionMessageResponse(
        status_code=200, type="application/vnd.microsoft.activity.message", value="OK",
    )
```

The user's selection arrives as a fresh turn through the card-action route — the same code path as a normal message — so the agent picks up with full context.

:::image type="content" source="../../assets/screenshots/clarification.gif" alt-text="Screenshot shows user selecting an option." lightbox="../../assets/screenshots/clarification.gif":::

## Suggested prompts

Suggested prompts give the user one-click follow-up questions after a reply.
In Teams they render as chips under the message; tapping one sends the `value` back as a normal user message, so the same `on_message` handler picks it up  no extra routing required.

Define prompts using `CardAction` and attach them to the reply via `with_suggested_actions`:

```python
from microsoft_teams.api import CardAction, CardActionType, SuggestedActions

_SUGGESTED_PROMPTS = [
    CardAction(
        type=CardActionType.IM_BACK,
        title="How do I stream in teams.py?",
        value="How do I stream in teams.py?",
    ),
    CardAction(
        type=CardActionType.IM_BACK,
        title="How do I create an Adaptive Card in teams.py?",
        value="How do I create an Adaptive Card in teams.py?",
    ),
]

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    async for chunk in agent.run(ctx.activity.text or "", stream=True):
        if chunk.text:
            ctx.stream.emit(chunk.text)

    reply = (MessageActivityInput().add_ai_generated()
            .add_feedback(mode="custom")
            # highlight-success-start
            .with_suggested_actions(
                SuggestedActions(to=[ctx.activity.from_.id], actions=_SUGGESTED_PROMPTS)
            )
            # highlight-success-end
    )
    ctx.stream.emit(reply)
```

:::image type="content" source="~/assets/screenshots/suggested-prompts.png" alt-text="Screenshot of outgoing agent message to user marked with 'AI generated' badge, with thumbs up/down feedback controls below the message." lightbox="~/assets/screenshots/suggested-prompts.png" :::

## Citations

Citations render as footnote-style references inline with the reply  `[1]`, `[2]`, etc.  surfacing the source title, abstract, and URL on hover. They typically originate from tool outputs, where middleware assigns each result a stable `position` (see the [`CitationMiddleware` example](./build-agent-maf.md#middleware) earlier).

When building the final reply, attach only the citations whose `position` actually appears in the streamed text.
```python
from microsoft_teams.api import CitationAppearance

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    # highlight-success-line
    full_text = ""
    async for chunk in agent.run(text, session=_sessions[conversation_id], stream=True):
        if chunk.text:
            ctx.stream.emit(chunk.text)
            # highlight-success-line
            full_text += chunk.text

    reply = (MessageActivityInput().add_ai_generated()
            .add_feedback(mode="custom")
            .with_suggested_actions(
                SuggestedActions(to=[ctx.activity.from_.id], actions=_SUGGESTED_PROMPTS)
            )
    )
    # highlight-success-start
    citations = tool_logger.get_citations()
    attach_citations(reply, full_text, citations)
    # highlight-success-end

    ctx.stream.emit(reply)

# highlight-success-start
def attach_citations(reply, full_text, citations):
    used = extract_referenced_ids(full_text)

    for c in citations:
        if c.position in used:
            reply.add_citation(
                position=c.position,
                appearance=CitationAppearance(
                    name=c.title,
                    abstract=c.description,
                    url=c.url),
                )
# highlight-success-end
```

:::image type="content" source="~/assets/screenshots/citations.gif" alt-text="Animated screenshot showing user hovering over a footnote citation in agent response, and a pop-up showing explanatory text." lightbox="~/assets/screenshots/citations.gif" :::
::: zone-end

::: zone pivot="typescript"

> [!NOTE]
> **Our AI libraries are deprecated**: The Teams SDK has deprecated its own AI libraries — the `@microsoft/teams.ai` packages (`ChatPrompt`, `Model`, and the older `@microsoft/teams.mcp` / `@microsoft/teams.a2a` plugins) — in favor of dedicated AI frameworks. Use the pattern shown in these guides instead: bring the OpenAI SDK (or any framework you like), and wire MCP and A2A directly into your Teams app.

You can enrich the agent output into a more Teams-native experience — adding structure, interactivity, and metadata on top of the generated text. This guide builds on the agent from [Build an agent in Teams](build-agent-maf.md).

## Streaming

Streaming delivers responses to Teams incrementally as they're generated, rather than waiting for the full reply to complete. Each chunk of text is appended to the stream as it arrives.

```ts
const runner = client.chat.completions.runTools({ model, messages: history, tools, stream: true });
runner.on('content', (delta: string) => stream.emit(delta));
await runner.done();
```

See [Streaming](../../essentials/sending-messages/overview.md#streaming) for the full story on how Teams renders chunks and the constraints on stream lifecycle.

## AI-generated label

`add_ai_generated()` marks the message as system-generated, ensuring it is clearly labeled as AI output within Teams.

```ts
const reply = new MessageActivity().addAiGenerated();
stream.emit(reply);
```

:::image type="content" source="../../assets/screenshots/streaming.gif" alt-text="Screenshot shows streaming."lightbox="../../assets/screenshots/streaming.gif":::

## User feedback

`add_feedback(mode="custom")` enables built-in thumbs up/down controls on the reply and lets you surface a custom feedback form when users respond.

```ts
const reply = new MessageActivity().addAiGenerated().addFeedback('custom');
stream.emit(reply);
```

See [Feedback](../feedback.md) for the full form-handling story  capturing the submission, persisting it, and following up with the user.

## Clarification cards

When the agent calls the `request_clarification` tool (from [Build an agent](build-agent-maf.md#adding-a-local-tool)), the reply is a card, not text. The model still produces a short wrap-up after the tool returns, so discard the streamed text and send only the card. Clearing the stream's accumulated text before emitting the card-only activity keeps the turn to a single clean reply.
```ts
function shipResult(result: AgentRunResult, stream: IStreamer, recipientId: string): void {
  if (result.pendingCard) {
    // Clarification card — discard any streamed text, then emit card-only.
    stream.clearText();
    stream.emit(new MessageActivity().addCard('adaptive', result.pendingCard).addAiGenerated());
    return;
  }
  // normal reply: attach follow-ups, citations, feedback (below).
}
```

The user's choice is captured by a card-action handler and fed straight back into the agent as the next turn:

```ts
app.on('card.action.clarification', async ({ activity, stream }) => {
  const data = (activity.value.action.data ?? {}) as Record<string, unknown>;
  const choice = typeof data[CLARIFICATION_INPUT_ID] === 'string' ? (data[CLARIFICATION_INPUT_ID] as string) : '';
  if (choice) {
    const result = await agent.run(activity.conversation.id, choice, stream);
    shipResult(result, stream, activity.from.id);
  }
  return { statusCode: 200, type: 'application/vnd.microsoft.activity.message', value: 'OK' };
});
```

The user's selection arrives as a fresh turn through the card-action route — the same code path as a normal message — so the agent picks up with full context.

:::image type="content" source="../../assets/screenshots/clarification.gif" alt-text="Screenshot shows user selecting an option." lightbox="../../assets/screenshots/clarification.gif":::

## Suggested prompts

Suggested prompts give the user one-click follow-up questions after a reply. In Teams they render as chips under the message; tapping one sends the value back as a normal user message, so the same message handler picks it up — no extra routing required.

Rather than hard-coding them, generate two contextual follow-ups with a separate lightweight model call constrained to a strict JSON schema, then attach them as suggested actions.

```ts
const FOLLOW_UPS_PROMPT =
  'Produce 2 specific prompts the user might want to ask next, based on the conversation so far. ' +
  'Each must be phrased in the first person and stay under 8 words.';

const FOLLOW_UPS_SCHEMA = {
  type: 'object',
  properties: { prompt1: { type: 'string' }, prompt2: { type: 'string' } },
  required: ['prompt1', 'prompt2'],
  additionalProperties: false,
} as const;

async function generateFollowUps(history: ChatCompletionMessageParam[]): Promise<string[]> {
  try {
    const completion = await client.chat.completions.create({
      model: deployment,
      messages: [...history, { role: 'system', content: FOLLOW_UPS_PROMPT }],
      response_format: {
        type: 'json_schema',
        json_schema: { name: 'follow_ups', strict: true, schema: FOLLOW_UPS_SCHEMA },
      },
    });
    const parsed = JSON.parse(completion.choices[0]?.message?.content ?? '{}');
    return [parsed.prompt1, parsed.prompt2].filter((s): s is string => typeof s === 'string' && s.length > 0);
  } catch {
    return []; // degrade silently — the main reply still ships
  }
}
```

Attach the generated prompts to the reply with withSuggestedActions:
```ts
finalMarker.withSuggestedActions({
  to: [recipientId],
  actions: followUps.map((prompt) => ({ type: 'imBack', title: prompt, value: prompt })),
});
```

:::image type="content" source="~/assets/screenshots/suggested-prompts.png" alt-text="Screenshot of outgoing agent message to user marked with 'AI generated' badge, with thumbs up/down feedback controls below the message." lightbox="~/assets/screenshots/suggested-prompts.png" :::
## Citations

Citations render as footnote-style references inline with the reply  `[1]`, `[2]`, etc.  surfacing the source title, abstract, and URL on hover. They typically originate from tool outputs, where middleware assigns each result a stable `position` (see the [`CitationMiddleware` example](./build-agent-maf.md#middleware) earlier).

When building the final reply, attach only the citations whose `position` actually appears in the streamed text.
```ts
attachCitations(activity: MessageActivity, fullText: string): number {
  const used = new Set<number>();
  for (const match of fullText.matchAll(/\[(\d+)\]/g)) used.add(Number(match[1]));

  let attached = 0;
  for (const entry of this.entries.values()) {
    if (!used.has(entry.position)) continue;
    activity.addCitation(entry.position, {
      name: entry.title || `Source ${entry.position}`,
      abstract: entry.snippet || 'No description available.',
      url: entry.url,
    });
    attached++;
  }
  return attached;
}
```
Assemble the final marker activity with everything at once — the AI label, custom feedback, citations, and follow-up chips — then emit it so the streamer folds them into the final message:

```ts
const finalMarker = new MessageActivity().addAiGenerated().addFeedback('custom');
result.citations.attachCitations(finalMarker, result.fullText);
if (result.followUps.length > 0) {
  finalMarker.withSuggestedActions({
    to: [recipientId],
    actions: result.followUps.map((p) => ({ type: 'imBack', title: p, value: p })),
  });
}
stream.emit(finalMarker);
```

:::image type="content" source="~/assets/screenshots/citations.gif" alt-text="Animated screenshot showing user hovering over a footnote citation in agent response, and a pop-up showing explanatory text." lightbox="~/assets/screenshots/citations.gif" :::
::: zone-end