---
sidebar_label: Keeping State
title: Keeping State
zone_pivot_groups: dev-lang
description: Guide to managing conversation state in LLM interactions, explaining how to maintain chat history using ChatPrompt's state management capabilities and implementing custom persistence strategies for multi-conversation scenarios.
---
# Keeping State

By default, LLMs are not stateful. This means that they do not remember previous messages or context when generating a response.
It's common practice to keep state of the conversation history in your application and pass it to the LLM each time you make a request.

By default, the `ChatPrompt` instance will create a temporary in-memory store to keep track of the conversation history. This is beneficial
when you want to use it to generate an LLM response, but not persist the conversation history. But in other cases, you may want to keep the conversation history

> [!WARNING]
> By reusing the same `ChatPrompt` class instance across multiple conversations will lead to the conversation history being shared across all conversations. Which is usually not the desired behavior.

To avoid this, you need to get messages from your persistent (or in-memory) store and pass it in to the `ChatPrompt`.

> [!NOTE]
> The `ChatPrompt` class will modify the messages object that's passed into it. So if you want to manually manage it, you need to make a copy of the messages object before passing it in.

## State Initialization

Here's how to initialize and manage conversation state for multiple conversations:


::: zone pivot="csharp"
```csharp
using Microsoft.Teams.AI;
using Microsoft.Teams.AI.Messages;
using Microsoft.Teams.AI.Models.OpenAI;
using Microsoft.Teams.AI.Prompts;
using Microsoft.Teams.AI.Templates;
using Microsoft.Teams.Api.Activities;
using Microsoft.Teams.Apps;

// Simple in-memory store for conversation histories
// In your application, it may be a good idea to use a more
// persistent store backed by a database or other storage solution
private static readonly Dictionary<string, List<IMessage>> ConversationStore = new();

/// <summary>
/// Get or create conversation memory for a specific conversation
/// </summary>
public static List<IMessage> GetOrCreateConversationMemory(string conversationId)
{
    if (!ConversationStore.ContainsKey(conversationId))
    {
        ConversationStore[conversationId] = new List<IMessage>();
    }

    return ConversationStore[conversationId];
}

/// <summary>
/// Clear memory for a specific conversation
/// </summary>
public static Task ClearConversationMemory(string conversationId)
{
    if (ConversationStore.TryGetValue(conversationId, out var messages))
    {
        var messageCount = messages.Count;
        messages.Clear();
    }

    return Task.CompletedTask;
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.ai import ChatPrompt, ListMemory, AIModel
from microsoft.teams.openai import OpenAICompletionsAIModel

# Simple in-memory store for conversation histories
# In your application, it may be a good idea to use a more
# persistent store backed by a database or other storage solution
conversation_store: dict[str, ListMemory] = {}

# Initialize AI model
ai_model = OpenAICompletionsAIModel(model="gpt-4")

def get_or_create_conversation_memory(conversation_id: str) -> ListMemory:
    """Get or create conversation memory for a specific conversation"""
    if conversation_id not in conversation_store:
        conversation_store[conversation_id] = ListMemory()
    return conversation_store[conversation_id]

async def clear_conversation_memory(conversation_id: str) -> None:
    """Clear memory for a specific conversation"""
    if conversation_id in conversation_store:
        memory = conversation_store[conversation_id]
        await memory.set_all([])
        print(f"Cleared memory for conversation {conversation_id}")
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { ChatPrompt, IChatModel, Message } from '@microsoft/teams.ai';
import { ActivityLike, IMessageActivity, MessageActivity } from '@microsoft/teams.api';
// ...

// Simple in-memory store for conversation histories
// In your application, it may be a good idea to use a more
// persistent store backed by a database or other storage solution
const conversationStore = new Map<string, Message[]>();

const getOrCreateConversationHistory = (conversationId: string) => {
  // Check if conversation history exists
  const existingMessages = conversationStore.get(conversationId);
  if (existingMessages) {
    return existingMessages;
  }
  // If not, create a new conversation history
  const newMessages: Message[] = [];
  conversationStore.set(conversationId, newMessages);
  return newMessages;
};
```
::: zone-end


## Usage Example


::: zone pivot="csharp"
```csharp
/// <summary>
/// Example of stateful conversation handler that maintains conversation history
/// </summary>
public static async Task HandleStatefulConversation(OpenAIChatModel model, IContext<MessageActivity> context)
{
    // Retrieve existing conversation memory or initialize new one
    var messages = GetOrCreateConversationMemory(context.Activity.Conversation.Id);

    // Create prompt with conversation-specific memory
    var prompt = new OpenAIChatPrompt(model, new ChatPromptOptions
    {
        Instructions = new StringTemplate("You are a helpful assistant that remembers our previous conversation.")
    });

    // Send with existing messages as context
    var options = new IChatPrompt<OpenAI.Chat.ChatCompletionOptions>.RequestOptions
    {
        Messages = messages
    };
    var result = await prompt.Send(context.Activity.Text, options);

    if (result.Content != null)
    {
        var message = new MessageActivity
        {
            Text = result.Content,
        }.AddAIGenerated();
        await context.Send(message);

        // Update conversation history
        messages.Add(UserMessage.Text(context.Activity.Text));
        messages.Add(new ModelMessage<string>(result.Content));
    }
    else
    {
        await context.Reply("I did not generate a response.");
    }
}
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.ai import ChatPrompt, ListMemory, AIModel
from microsoft.teams.api import MessageActivity, MessageActivityInput
from microsoft.teams.apps import ActivityContext
# ...

async def handle_stateful_conversation(model: AIModel, ctx: ActivityContext[MessageActivity]) -> None:
    """Example of stateful conversation handler that maintains conversation history"""
    print(f"Received message: {ctx.activity.text}")

    # Retrieve existing conversation memory or initialize new one
    memory = get_or_create_conversation_memory(ctx.activity.conversation.id)

    # Get existing messages for logging
    existing_messages = await memory.get_all()
    print(f"Existing messages before sending to prompt: {len(existing_messages)} messages")

    # Create ChatPrompt with conversation-specific memory
    chat_prompt = ChatPrompt(model, memory=memory)

    chat_result = await chat_prompt.send(
        input=ctx.activity.text,
        instructions="You are a helpful assistant that remembers our previous conversation."
    )

    if chat_result.response.content:
        message = MessageActivityInput(text=chat_result.response.content).add_ai_generated()
        await ctx.send(message)
    else:
        await ctx.reply("I did not generate a response.")

    # Log final message count
    final_messages = await memory.get_all()
    print(f"Messages after sending to prompt: {len(final_messages)} messages")

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    """Handle messages using stateful conversation"""
    await handle_stateful_conversation(ai_model, ctx)
```
::: zone-end

::: zone pivot="typescript"
```typescript
/**
 * Example of a stateful conversation handler that maintains conversation history
 * using an in-memory store keyed by conversation ID.
 * @param model The chat model to use
 * @param activity The incoming activity
 * @param send Function to send an activity
 */
export const handleStatefulConversation = async (
  model: IChatModel,
  activity: IMessageActivity,
  send: (activity: ActivityLike) => Promise<any>,
  log: ILogger
) => {
  log.info('Received message', activity.text);

  // Retrieve existing conversation history or initialize new one
  const existingMessages = getOrCreateConversationHistory(activity.conversation.id);

  log.info('Existing messages before sending to prompt', existingMessages);

  // Create prompt with existing messages
  const prompt = new ChatPrompt({
    instructions: 'You are a helpful assistant.',
    model,
    messages: existingMessages, // Pass in existing conversation history
  });

  const result = await prompt.send(activity.text);

  if (result) {
    await send(
      result.content != null
        ? new MessageActivity(result.content).addAiGenerated()
        : 'I did not generate a response.'
    );
  }

  log.info('Messages after sending to prompt:', existingMessages);
};
```
::: zone-end



::: zone pivot="csharp"
### Usage in your application

```csharp
teamsApp.OnMessage(async (context) =>
{
    await HandleStatefulConversation(aiModel, context);
});
```

#### How It Works

1. **Conversation Store**: A dictionary maps conversation IDs to their message histories
2. **Per-Conversation Memory**: Each conversation gets its own isolated message list
3. **Request Options**: Pass the message history via `RequestOptions.Messages` when calling `Send()`
4. **Automatic Updates**: After receiving a response, manually add both the user message and AI response to the store
5. **Persistence**: The conversation history persists across multiple user interactions within the same conversation

> [!TIP]
> The `ChatPrompt.Send()` method does **not** automatically update the messages you pass in via `RequestOptions`. You must manually add the user message and AI response to your conversation store after each interaction.

> [!NOTE]
> In a production application, consider using a more robust storage solution like Azure Cosmos DB, SQL Server, or Redis instead of an in-memory dictionary. This ensures conversation history persists across application restarts and scales across multiple instances.

![Stateful Chat Example](~/assets/screenshots/stateful-chat-example.png)
::: zone-end

::: zone pivot="python"
![Screenshot of chat between user and agent, user first states 'My dinosaur's name is Barnie' and later asks What's my pet's name and the agent responds correctly with 'Barnie'.](~/assets/screenshots/stateful-chat-example.png)
::: zone-end

::: zone pivot="typescript"
![Stateful Chat Example](~/assets/screenshots/stateful-chat-example.png)
::: zone-end
