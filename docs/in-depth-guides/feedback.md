---
sidebar_position: 7
title: Feedback
sidebar_label: Feedback
summary: Guide to implementing user feedback functionality in Teams applications, covering feedback UI components, event handling, and storage mechanisms for gathering and managing user responses to improve application performance.
zone_pivot_groups: dev-lang
---

# Feedback

User feedback is essential for the improvement of any application. Teams provides specialized UI components to help facilitate the gathering of feedback from users.

![Animated image showing user selecting the thumbs-up button on an agent response and a dialog opening asking 'What did you like?'. The user types 'Nice' and hits Submit.](/screenshots/feedback.gif)

## Storage

Once you receive a feedback event, you can choose to store it in some persistent storage. In the example below, we are storing it in an in-memory store.


::: zone pivot="csharp"
```csharp
// This store would ideally be persisted in a database
public static class FeedbackStore
{
    public static readonly Dictionary<string, FeedbackData> StoredFeedbackByMessageId = new();

    public class FeedbackData
    {
        public string IncomingMessage { get; set; } = string.Empty;
        public string OutgoingMessage { get; set; } = string.Empty;
        public int Likes { get; set; }
        public int Dislikes { get; set; }
        public List<string> Feedbacks { get; set; } = new();
    }
}
```
::: zone-end

::: zone pivot="python"
Once you receive a feedback event, you can choose to store it in some persistent storage. You'll need to implement storage for tracking:

- Like/dislike counts per message
- Text feedback comments
- Message ID associations

For production applications, consider using databases, file systems, or cloud storage. The examples below use in-memory storage for simplicity.
::: zone-end

::: zone pivot="typescript"
```typescript
import { ChatPrompt, IChatModel } from '@microsoft/teams.ai';
import { ActivityLike, IMessageActivity, MessageActivity } from '@microsoft/teams.api';
// ...

// This store would ideally be persisted in a database
export const storedFeedbackByMessageId = new Map<
  string,
  {
    incomingMessage: string;
    outgoingMessage: string;
    likes: number;
    dislikes: number;
    feedbacks: string[];
  }
>();
```
::: zone-end


## Including Feedback Buttons

When sending a message that you want feedback in, simply add feedback functionality to the message you are sending.


::: zone pivot="csharp"
```csharp
var sentMessageId = await context.Send(
    result.Content != null
        ? new MessageActivity(result.Content)
            .AddAiGenerated()
            /** Add feedback buttons via this method */
            .AddFeedback()
        : "I did not generate a response."
);

FeedbackStore.StoredFeedbackByMessageId[sentMessageId.Id] = new FeedbackStore.FeedbackData
{
    IncomingMessage = context.Activity.Text,
    OutgoingMessage = result.Content ?? string.Empty,
    Likes = 0,
    Dislikes = 0,
    Feedbacks = new List<string>()
};
```
::: zone-end

::: zone pivot="python"
```python
from microsoft.teams.ai import Agent
from microsoft.teams.api import MessageActivityInput
from microsoft.teams.apps import ActivityContext, MessageActivity

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    """Handle 'feedback demo' command to demonstrate feedback collection"""
    agent = Agent(current_model)
    chat_result = await agent.send(
        input="Tell me a short joke",
        instructions="You are a comedian. Keep responses brief and funny."
    )

    if chat_result.response.content:
        message = MessageActivityInput(text=chat_result.response.content)
                    .add_ai_generated()
                    # Create message with feedback enabled
                    .add_feedback()
        await ctx.send(message)
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { ChatPrompt, IChatModel } from '@microsoft/teams.ai';
import {
  ActivityLike,
  IMessageActivity,
  MessageActivity,
  SentActivity,
} from '@microsoft/teams.api';
// ...

const { id: sentMessageId } = await send(
  result.content != null
    ? new MessageActivity(result.content)
        .addAiGenerated()
        /** Add feedback buttons via this method */
        .addFeedback()
    : 'I did not generate a response.'
);

storedFeedbackByMessageId.set(sentMessageId, {
  incomingMessage: activity.text,
  outgoingMessage: result.content ?? '',
  likes: 0,
  dislikes: 0,
  feedbacks: [],
});
```
::: zone-end


## Handling the feedback

Once the user decides to like/dislike the message, you can handle the feedback in a received event. Once received, you can choose to include it in your persistent store.


::: zone pivot="csharp"
```csharp
[Microsoft.Teams.Apps.Activities.Invokes.Message.Feedback]
public Task OnFeedbackReceived([Context] Microsoft.Teams.Api.Activities.Invokes.Messages.SubmitActionActivity activity)
{
    var reaction = activity.Value?.ActionValue?.GetType().GetProperty("reaction")?.GetValue(activity.Value?.ActionValue)?.ToString();
    var feedbackJson = activity.Value?.ActionValue?.GetType().GetProperty("feedback")?.GetValue(activity.Value?.ActionValue)?.ToString();

    if (activity.ReplyToId == null)
    {
        _log.LogWarning("No replyToId found for messageId {ActivityId}", activity.Id);
        return Task.CompletedTask;
    }

    var existingFeedback = FeedbackStore.StoredFeedbackByMessageId.GetValueOrDefault(activity.ReplyToId);
    /**
        * feedbackJson looks like:
        * {"feedbackText":"Nice!"}
        */
    if (existingFeedback == null)
    {
        _log.LogWarning("No feedback found for messageId {ActivityId}", activity.Id);
    }
    else
    {
        var updatedFeedback = new FeedbackStore.FeedbackData
        {
            IncomingMessage = existingFeedback.IncomingMessage,
            OutgoingMessage = existingFeedback.OutgoingMessage,
            Likes = existingFeedback.Likes + (reaction == "like" ? 1 : 0),
            Dislikes = existingFeedback.Dislikes + (reaction == "dislike" ? 1 : 0),
            Feedbacks = existingFeedback.Feedbacks.Concat(new[] { feedbackJson ?? string.Empty }).ToList()
        };

        FeedbackStore.StoredFeedbackByMessageId[activity.Id] = updatedFeedback;
    }

    return Task.CompletedTask;
}
```
::: zone-end

::: zone pivot="python"
```python
import json
from typing import Dict, Any
from microsoft.teams.api import MessageSubmitActionInvokeActivity
from microsoft.teams.apps import ActivityContext
# ...

# Handle feedback submission events
@app.on_message_submit_feedback
async def handle_message_feedback(ctx: ActivityContext[MessageSubmitActionInvokeActivity]):
    """Handle feedback submission events"""
    activity = ctx.activity

    # Extract feedback data from activity value
    if not hasattr(activity, "value") or not activity.value:
        logger.warning(f"No value found in activity {activity.id}")
        return

    # Access feedback data directly from invoke value
    invoke_value = activity.value
    assert invoke_value.action_name == "feedback"
    feedback_str = invoke_value.action_value.feedback
    reaction = invoke_value.action_value.reaction
    feedback_json: Dict[str, Any] = json.loads(feedback_str)
    # { 'feedbackText': 'the ai response was great!' }

    if not activity.reply_to_id:
        logger.warning(f"No replyToId found for messageId {activity.id}")
        return

    # Store the feedback (implement your own storage logic)
    upsert_feedback_storage(activity.reply_to_id, reaction, feedback_json.get('feedbackText', ''))

    # Optionally Send confirmation response
    feedback_text: str = feedback_json.get("feedbackText", "")
    reaction_text: str = f" and {reaction}" if reaction else ""
    text_part: str = f" with comment: '{feedback_text}'" if feedback_text else ""

    await ctx.reply(f"✅ Thank you for your feedback{reaction_text}{text_part}!")
```
::: zone-end

::: zone pivot="typescript"
```typescript
import { App } from '@microsoft/teams.apps';
// ...

app.on('message.submit.feedback', async ({ activity, log }) => {
  const { reaction, feedback: feedbackJson } = activity.value.actionValue;
  if (activity.replyToId == null) {
    log.warn(`No replyToId found for messageId ${activity.id}`);
    return;
  }
  const existingFeedback = storedFeedbackByMessageId.get(activity.replyToId);
  /**
   * feedbackJson looks like:
   * {"feedbackText":"Nice!"}
   */
  if (!existingFeedback) {
    log.warn(`No feedback found for messageId ${activity.id}`);
  } else {
    storedFeedbackByMessageId.set(activity.id, {
      ...existingFeedback,
      likes: existingFeedback.likes + (reaction === 'like' ? 1 : 0),
      dislikes: existingFeedback.dislikes + (reaction === 'dislike' ? 1 : 0),
      feedbacks: [...existingFeedback.feedbacks, feedbackJson],
    });
  }
});
```
::: zone-end

