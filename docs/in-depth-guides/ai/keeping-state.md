---
title: Keeping State
description: Guide to managing conversation state in LLM interactions, explaining how to maintain chat history using ChatPrompt's state management capabilities and implementing custom persistence strategies for multi-conversation scenarios.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 05/15/2026
---
# Keeping State

::: zone pivot="python"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="javascript,csharp"
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
::: zone-end

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

::: zone pivot="javascript,csharp"
## Usage Example
::: zone-end

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
teamsApp.OnMessage(async (context, cancellationToken) =>
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
:::image type="content" source="~/assets/screenshots/stateful-chat-example.png" alt-text="Stateful Chat Example" lightbox="~/assets/screenshots/stateful-chat-example.png":::
::: zone-end

::: zone pivot="typescript"
:::image type="content" source="~/assets/screenshots/stateful-chat-example.png" alt-text="Stateful Chat Example" lightbox="~/assets/screenshots/stateful-chat-example.png":::
::: zone-end
