---
title: Enhance the Teams Experience
description: Round out a Teams agent reply with streaming, the AI-generated label, custom feedback, clarification cards, dynamic follow-up prompts, and inline citations.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 07/27/2026
---

# Enhance the Teams Experience

::: zone pivot="csharp"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="typescript"

> [!WARNING]
>
> Our AI libraries are deprecated
> The Teams SDK has deprecated its own AI libraries a the `@microsoft/teams.ai` packages (`ChatPrompt`, `Model`, and the older `@microsoft/teams.mcp` / `@microsoft/teams.a2a` plugins) a in favor of dedicated AI frameworks. Use the pattern shown in these guides instead: bring the OpenAI SDK (or any framework you like), and wire MCP and A2A directly into your Teams app.

::: zone-end

::: zone pivot="python,typescript"

## Enhance the Teams Experience

You can enrich the agent output into a more Teams-native experience a adding structure, interactivity, and metadata on top of the generated text. This guide builds on the agent from [Build an agent in Teams](./build-agent.md).

## Streaming

Streaming delivers responses to Teams incrementally as they're generated, rather than waiting for the full reply to complete. Each chunk of text is appended to the stream as it arrives.
::: zone-end

::: zone pivot="python"
```python

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    async for chunk in agent.run(ctx.activity.text or "", stream=True):
        if chunk.text:
            ctx.stream.emit(chunk.text)
```
::: zone-end

::: zone pivot="typescript"
```typescript

const runner = client.chat.completions.runTools({ model, messages: history, tools, stream: true });
runner.on('content', (delta: string) => stream.emit(delta));
await runner.done();
```
::: zone-end

::: zone pivot="python,typescript"
See [Streaming](../../essentials/sending-messages/overview.md#streaming) for the full story on how Teams renders chunks and the constraints on stream lifecycle.

## AI-generated label

Mark the message as system-generated so Teams clearly labels it as AI output.
::: zone-end

::: zone pivot="python"
`add_ai_generated()` marks the message as system-generated.

```python

reply = MessageActivityInput().add_ai_generated()
ctx.stream.emit(reply)
```
::: zone-end

::: zone pivot="typescript"
`addAiGenerated()` marks the message as system-generated.

```typescript

const reply = new MessageActivity().addAiGenerated();
stream.emit(reply);
```
::: zone-end

::: zone pivot="python,typescript"
<img
  src={StreamingImgUrl}
  alt="Animated screenshot of an agent reply streaming into a Teams chat token by token, with the 'AI generated' label on the message."
  style={{ width: '100%', maxWidth: 900 }}
/>

## User feedback

Enable built-in thumbs up/down controls on the reply and surface a custom feedback form when users respond.
::: zone-end

::: zone pivot="python"
`add_feedback(mode="custom")` enables the thumbs up/down controls and lets you surface a custom feedback form when users respond.

```python

reply = MessageActivityInput().add_ai_generated().add_feedback(mode="custom")
ctx.stream.emit(reply)
```
::: zone-end

::: zone pivot="typescript"
`addFeedback('custom')` enables the thumbs up/down controls and lets you surface a custom feedback form when users respond.

```typescript

const reply = new MessageActivity().addAiGenerated().addFeedback('custom');
stream.emit(reply);
```
::: zone-end

::: zone pivot="python,typescript"
See [Feedback](../feedback.md) for the full form-handling story a capturing the submission, persisting it, and following up with the user.

## Clarification cards

When the agent calls the `request_clarification` tool (from [Build an agent](./build-agent.md#adding-a-local-tool)), the reply is a card, not text. The model still produces a short wrap-up after the tool returns, so discard the streamed text and send only the card. Clearing the stream's accumulated text before emitting the card-only activity keeps the turn to a single clean reply.
::: zone-end

::: zone pivot="python"
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
::: zone-end

::: zone pivot="typescript"
```typescript

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

```typescript

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
::: zone-end

::: zone pivot="python,typescript"
The user's selection arrives as a fresh turn through the card-action route; the same code path as a normal message, so the agent picks up with full context.

<img
  src={ClarificationImgUrl}
  alt="Animated screenshot of the clarification flow: the user asks an ambiguous question, the bot replies with a choice card, the user picks an option, and the bot streams a grounded answer with an inline citation."
  style={{ width: '100%', maxWidth: 900 }}
/>

## Suggested prompts

Suggested prompts give the user one-click follow-up questions after a reply. In Teams they render as chips under the message; tapping one sends the value back as a normal user message, so the same message handler picks it up a no extra routing required.

Rather than hard-coding them, generate two contextual follow-ups with a separate lightweight model call constrained to a strict JSON schema, then attach them as suggested actions.
::: zone-end

::: zone pivot="python"
```python

import json

from microsoft_teams.api import CardAction, CardActionType, SuggestedActions

_FOLLOW_UPS_PROMPT = (
    "Based on the conversation so far, suggest exactly 2 short follow-up questions the user might want to ask next. "
    'Respond with JSON: {"followUps": ["question 1", "question 2"]}. Keep each question under 60 characters.'
)

async def _generate_follow_ups(last_user_text: str, last_ai_text: str) -> list[CardAction]:
    completion = await openai_client.chat.completions.create(
        model=getenv("AZURE_OPENAI_MODEL", ""),
        messages=[
            {"role": "user", "content": last_user_text},
            {"role": "assistant", "content": last_ai_text},
            {"role": "system", "content": _FOLLOW_UPS_PROMPT},
        ],
        response_format=_FOLLOW_UPS_SCHEMA,  # strict json_schema
    )
    data = json.loads(completion.choices[0].message.content or "{}")
    return [CardAction(type=CardActionType.IM_BACK, title=q, value=q) for q in data.get("followUps", [])[:2]]
```

Attach the generated prompts to the reply with `with_suggested_actions`:

```python

reply.with_suggested_actions(
    SuggestedActions(to=[ctx.activity.from_.id], actions=follow_ups)
)
```

The follow-up call runs separately from the main agent, so any parse or network failure silently degrades to no chips while the main reply still ships.
::: zone-end

::: zone pivot="typescript"
```typescript

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

Attach the generated prompts to the reply with `withSuggestedActions`:

```typescript

finalMarker.withSuggestedActions({
  to: [recipientId],
  actions: followUps.map((prompt) => ({ type: 'imBack', title: prompt, value: prompt })),
});
```
::: zone-end

::: zone pivot="python,typescript"
<img
  src={SuggestedPromptsImgUrl}
  alt="Animated screenshot of suggested follow-up prompt chips appearing under an agent reply; tapping one sends it back as the next user message."
  style={{ width: '100%', maxWidth: 900 }}
/>

## Citations

Citations render as footnote-style references inline with the reply a `[1]`, `[2]`, etc. a surfacing the source title, abstract, and URL on hover. They originate from tool outputs, where the collector from [Grounding responses with citations](./build-agent.md#grounding-responses-with-citations) assigned each result a stable position.

When building the final reply, attach only the citations whose position actually appears in the streamed text.
::: zone-end

::: zone pivot="python"
```python

import re

from microsoft_teams.api import CitationAppearance

def _attach_citations(reply: MessageActivityInput, full_text: str) -> None:
    used_positions = {int(n) for n in re.findall(r"\[(\d+)\]", full_text)}
    for annotation in tool_logger.citations.values():
        pos = annotation["position"]
        if pos in used_positions:
            reply.add_citation(
                position=pos,
                appearance=CitationAppearance(
                    name=annotation.get("title") or f"Source {pos}",
                    abstract=annotation.get("snippet") or "No description available.",
                    url=annotation.get("url"),
                ),
            )
```

`tool_logger` is the `CitationMiddleware` instance from [Build an agent](./build-agent.md#grounding-responses-with-citations); its `citations` dict is reset at the start of each turn.
::: zone-end

::: zone pivot="typescript"
Use the `CitationCollector` from [Build an agent](./build-agent.md#grounding-responses-with-citations). `attachCitations` reads the `[N]` markers out of the streamed text and writes a citation entity onto the final activity for each one it has data for.

```typescript

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

Assemble the final marker activity with everything at once a the AI label, custom feedback, citations, and follow-up chips a then emit it so the streamer folds them into the final message:

```typescript

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
::: zone-end

::: zone pivot="python,typescript"
<img
  src={CitationsImgUrl}
  alt="Animated screenshot showing a user hovering over a footnote citation in an agent response, with a pop-up showing explanatory text."
  style={{ width: '100%', maxWidth: 900 }}
/>
::: zone-end

