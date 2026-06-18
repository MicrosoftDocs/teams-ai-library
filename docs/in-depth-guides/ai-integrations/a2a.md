---
title: 'Bot-to-Bot Communication with A2A'
description: 'Connect two Teams bots so their agents can ask each other questions over the Agent2Agent protocol  with human operators in the loop on both sides.'
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 06/11/2026
---

# Bot-to-Bot Communication with A2A

::: zone pivot="csharp,typescript"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="python"

## Bot-to-Bot Communication with A2A

Agents are typically designed to interact either with people (chatbots) or with systems (tools, APIs, MCP servers).[Agent2Agent (A2A)](https://a2a-protocol.org/latest/) introduces a third interaction model: agents communicating directly with other agents as peers — each with its own model, capabilities, and human audience.

This guide walks through a **handoff** between two Teams bots, **Alice** and **Bob**, each backed by its own LLM agent. A user DMs one bot; its agent reads the peer's capability description and decides whether to answer directly or hand the user off. On handoff, the receiving bot **proactively opens a 1:1 chat** with the user and greets them with the context that came across — so the conversation continues seamlessly in the new chat.

Both bots run the **same code**, differentiated entirely by environment variables (name, description, self/peer URLs). They use [@a2a-js/sdk](https://www.npmjs.com/package/@a2a-js/sdk) for the protocol and the OpenAI SDK for the LLM agent.

Full source: [examples/a2a-test](https://github.com/microsoft/teams.py/tree/main/examples/a2a-test).

## Advertising capabilities with an Agent Card

Every A2A server publishes an `AgentCard`  a small machine-readable document describing who the agent is and what it can do. Peers fetch this card to learn about each other; their LLMs then read the `description` field to decide *when* to forward a question.

The card is built once per bot and served by the A2A runtime alongside the request handler.

```python
from a2a.server.apps.jsonrpc.starlette_app import A2AStarletteApplication
from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

agent_card = AgentCard(
    name="Alice",
    description="Alice — a Teams bot whose human operator answers design and UX questions.",
    url="http://localhost:3978/a2a/",
    version="1.0.0",
    protocol_version="0.3.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[AgentSkill(id="ask_reply", name="ask_reply", description="...", tags=["ask_reply"])],
)
```

The `description` is the most important knob in this sample  it's the natural-language summary another bot's LLM uses to decide whether *this* bot is the right peer for a given question. Tweak it to match the persona and expertise you want each bot to advertise.

## Defining the A2A message contract

A2A messages carry arbitrary structured data inside `DataPart` envelopes. Defining a small Pydantic union with a `kind` discriminator keeps both sides honest about what they accept  and lets the executor branch cleanly on the message type without sniffing dictionaries.

```python
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field, TypeAdapter

class AskMessage(BaseModel):
    kind: Literal["ask"] = "ask"
    qid: str
    question: str
    sender: str
    reply_url: str

class ReplyMessage(BaseModel):
    kind: Literal["reply"] = "reply"
    qid: str
    answer: str
    responder: str

A2AMessage = Annotated[Union[AskMessage, ReplyMessage], Field(discriminator="kind")]
A2AMessageAdapter: TypeAdapter[A2AMessage] = TypeAdapter(A2AMessage)
```

Each `ask` carries a `qid` (question id) used to correlate the asynchronous reply that arrives later, plus a `reply_url` so the answering bot knows where to send the response.

## LLM-driven peer routing

Routing is not a hard-coded rule  the LLM decides. Each bot exposes a single `send_to_peer` tool to its agent, and the agent's instructions include the live `AgentCard.description` of every reachable peer. When a question fits a peer's expertise better than its own, the model picks the tool.

Peer cards are fetched lazily via `A2ACardResolver` and cached, so the agent's prompt always reflects the latest descriptions.

# [The send_to_peer tool](#tab/tool)

```python
from agent_framework import tool
from a2a_client import send_a2a
from messages import AskMessage

@tool
async def send_to_peer(
    peer: Annotated[str, Field(description=f"Peer to ask. Must be one of: {peer_names}.")],
    question: Annotated[str, Field(description="The natural-language question to send to the peer.")],
) -> str:
    """Forward a question to a peer agent over A2A.

    Use this when the user's question fits a peer's expertise (per their description) better than
    your own. The reply arrives asynchronously (a human operator answers on the peer's side), so
    this call only *queues* the question and returns immediately.
    """
    peer_url = self._peers[peer]
    qid = str(uuid.uuid4())
    user_conv_id = current_user_conv_id.get()
    self._state.awaiting_reply[qid] = {"conv_id": user_conv_id, "question": question}
    msg = AskMessage(qid=qid, question=question, sender=self._self_name, reply_url=self._self_a2a_url)
    await send_a2a(peer_url, msg.model_dump())
    return f"Queued question to {peer}. Their reply will arrive separately."
```

# [Instructions with peer descriptions](#tab/instructions)

```python
async def _refresh_peer_cards(self) -> None:
    async with httpx.AsyncClient(timeout=10.0) as http:
        for name in self._peers:
            if name in self._peer_cards:
                continue
            card = await A2ACardResolver(http, self._peers[name]).get_agent_card()
            self._peer_cards[name] = card

instructions = f"""You are {self._self_name}, a Teams bot assistant.

You should forward questions to peer agents when their expertise fits better than your own.
Peers:
{self._format_peers()}   # renders "- bob: <bob's AgentCard.description>"

Guidelines:
- If a peer is a good fit for the user's question, call `send_to_peer` with that peer's name.
- Otherwise, answer the user directly.
- When a peer reply arrives later, you'll see a "[peer update]" note in the conversation; reference it naturally.
"""
```

---

The tool only *queues* the ask  it returns as soon as the A2A call has been sent. The actual answer arrives later, asynchronously, as a separate inbound A2A message. The `qid` is stashed in `awaiting_reply` so the bot can correlate that reply with the original user conversation when it lands.

## Sending an A2A message

The outbound side is a small wrapper around the official `a2a-sdk` client: resolve the peer's card, build a client, and fire a single `DataPart`-carrying message. We drain the response stream without reading it  the peer only sends an `ack`; any real answer comes back later as a separate inbound A2A call.

```python
import httpx, uuid
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import DataPart, Message, Part, Role

async def send_a2a(peer_url: str, data: dict[str, Any]) -> None:
    async with httpx.AsyncClient(timeout=60.0) as http_client:
        peer_card = await A2ACardResolver(httpx_client=http_client, base_url=peer_url).get_agent_card()
        client = ClientFactory(ClientConfig(httpx_client=http_client, streaming=True)).create(peer_card)

        request = Message(
            message_id=str(uuid.uuid4()),
            role=Role.user,
            parts=[Part(root=DataPart(data=data))],
        )
        async for _ in client.send_message(request):
            pass
```

## Handling inbound A2A messages

The A2A server side dispatches incoming messages by inspecting the `DataPart` payload and branching on the `kind` discriminator. An `ask` is routed to the operator as an Adaptive Card; a `reply` is folded back into the original user's chat.

A2A tasks need a terminal status event to close out, so the executor always emits one  even when the "real" response will flow later as a separate inbound call.

```python
from a2a.server.agent_execution.agent_executor import AgentExecutor

class AskReplyExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        message = parse_a2a_message(context.message)

        if isinstance(message, AskMessage):
            await self._on_ask(message)
        elif isinstance(message, ReplyMessage):
            await self._on_reply(message)

        # Ack and finish — the real response (if any) flows later as a separate
        # inbound A2A message from the peer.
        ack = Message(message_id=str(uuid.uuid4()), role=Role.agent,
                      parts=[Part(root=DataPart(data={"kind": "ack"}))])
        await event_queue.enqueue_event(TaskStatusUpdateEvent(
            task_id=context.task_id, context_id=context.context_id,
            status=TaskStatus(state=TaskState.completed, message=ack),
            final=True,
        ))
```

### Validating the peer

Before stashing routing state or pushing a card to a human, the executor verifies that the inbound `reply_url` matches a configured allowlist.

```python
async def _on_ask(self, msg: AskMessage) -> None:
    conv_id = self._state.operator_conv_id
    if not conv_id:
        return  # nobody to ask yet
    if not is_allowed_peer(msg.reply_url, self._allowed_peer_urls):
        return  # untrusted reply_url
    self._state.inbound_asks[msg.qid] = {
        "reply_url": msg.reply_url, "sender": msg.sender, "question": msg.question,
    }
    await self._teams_app.send(conv_id, ask_card(sender=msg.sender, question=msg.question, qid=msg.qid))
```

In production, replace this URL-based check with a real authorization mechanism  a bearer token signed by an IdP, or mTLS  rather than trusting a self-declared URL.

## Human-in-the-loop via Adaptive Cards

When a peer asks a question, the answering bot pushes an Adaptive Card to its operator's 1:1 conversation. The operator types a reply and submits; the card-action handler looks up the original peer by `qid` and forwards the answer back over A2A.

The submit payload only carries the `qid`  the `reply_url` is resolved from server-side state, since card data is client-tamperable.

# [The ask card](#tab/card)

```python
from microsoft_teams.cards import (
    ActionSet, AdaptiveCard, ExecuteAction, SubmitData, TextBlock,
)
from microsoft_teams.cards.core import TextInput

ASK_REPLY_ACTION = "ask_reply"

def ask_card(sender: str, question: str, qid: str) -> AdaptiveCard:
    return AdaptiveCard(
        version="1.4",
        body=[
            TextBlock(text=f"From {sender}", weight="Bolder", size="Medium"),
            TextBlock(text=question, wrap=True),
            TextInput(id="answer").with_label("Your answer").with_placeholder("Type here…"),
            ActionSet(actions=[
                ExecuteAction(title="Send reply")
                    .with_data(SubmitData(action=ASK_REPLY_ACTION, data={"qid": qid}))
                    .with_associated_inputs("auto")
            ]),
        ],
    )
```

# [Operator submit handler](#tab/handler)

```python
@app.on_card_action_execute(ASK_REPLY_ACTION)
async def handle_reply_submit(ctx: ActivityContext[AdaptiveCardInvokeActivity]) -> AdaptiveCardInvokeResponse:
    d = ctx.activity.value.action.data
    qid = d.get("qid", "")
    answer_text = d.get("answer", "")

    pending = state.inbound_asks.pop(qid, None)
    if pending is None:
        return AdaptiveCardActionMessageResponse(value="Reply not sent: no matching ask.")

    reply = ReplyMessage(qid=qid, answer=answer_text, responder=NAME)
    await send_a2a(pending["reply_url"], reply.model_dump())
    return AdaptiveCardActionMessageResponse(value=f"Reply sent back to {pending['sender']}.")
```

---

The "operator" is just whoever DM'd the bot most recently in a 1:1 conversation  captured in `state.operator_conv_id` from the message handler. In production, you'd wire this to a real on-call rotation or assignment system.

## Folding peer replies back into the conversation

When the peer's reply lands, two things need to happen: the user who originally asked needs to *see* the answer, and the LLM agent needs to *know* about it so future turns can reference it naturally. The reply card handles the first; an injected `[peer update]` note in the agent's session handles the second.

```python
async def _on_reply(self, msg: ReplyMessage) -> None:
    pending = self._state.awaiting_reply.pop(msg.qid, None)
    if not pending:
        return
    card = reply_card(responder=msg.responder, question=pending["question"],
                      answer=msg.answer, qid=msg.qid)
    await self._teams_app.send(pending["conv_id"], card)
    if self._on_peer_reply is not None:
        self._on_peer_reply(pending["conv_id"], msg.responder, pending["question"], msg.answer)
```

The `on_peer_reply` callback lets the agent layer append the answer to the user's session history, so the next time the model runs it sees the peer's response as conversational context:

```python
def record_peer_reply(self, user_conv_id: str, responder: str, question: str, answer: str) -> None:
    session = self._sessions.get(user_conv_id)
    if session is None:
        return
    note = f"[peer update] {responder} replied: {answer!r} (to your earlier question: {question!r})."
    store = session.state.setdefault(InMemoryHistoryProvider.DEFAULT_SOURCE_ID, {})
    messages: list[Message] = store.setdefault("messages", [])
    messages.append(Message("user", [note]))
```

This is what closes the loop on the LLM-driven part: the next time the user references the earlier question ("how do I scale my postgres database again, I forgot?"), the model has the peer's answer in context and can summarize it in its own words.

## Wiring A2A into your Teams app

The Teams bot and A2A server run in the same process and share one HTTP surface. The Teams app handles `/api/messages`; the A2A Starlette sub-app is mounted at `/a2a` on the same FastAPI instance, so a single uvicorn serves both.

```python
import asyncio, uvicorn
from fastapi import FastAPI
from microsoft_teams.apps import App, FastAPIAdapter

fastapi_app = FastAPI()
app = App(http_server_adapter=FastAPIAdapter(app=fastapi_app), ...)

async def main() -> None:
    a2a_app = make_a2a_app(
        teams_app=app,
        state=state,
        description=DESCRIPTION,
        skill="ask_reply",
        url=SELF_A2A_URL,
        allowed_peer_urls=ALLOWED_PEER_URLS,
        on_peer_reply=bot_agent.record_peer_reply,
    )
    fastapi_app.mount("/a2a", a2a_app.build())
    await app.initialize()
    server = uvicorn.Server(uvicorn.Config(fastapi_app, host=HOST, port=PORT))
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
```

Each bot needs its own Teams app registration (so DMs route to the right bot) and its own port. The sample runs Alice on `3978` and Bob on `3979`; their A2A URLs point at each other through the `BOB_A2A_URL` and `ALICE_A2A_URL` environment variables.

## Putting it all together

With both bots running and DM'd at least once (so each has captured an operator conversation), DM Alice with a backend question and watch the round-trip: Alice's LLM picks `send_to_peer`, Bob's operator gets the ask card, types an answer, and the reply card lands back in Alice's chat with the user.

:::image type="content" source="~/assets/screenshots/a2a.gif" alt-text="Animated screenshot of the end-to-end A2A flow: user DMs Alice, Alice forwards to Bob, Bob's operator answers via Adaptive Card, and the reply flows back into the original chat." lightbox="~/assets/screenshots/a2a.gif" :::
The bots are symmetric  DM Bob with a UX question and the same flow runs the other way, with Bob's LLM forwarding to Alice.
::: zone-end
