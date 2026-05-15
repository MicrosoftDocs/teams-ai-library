---
title: Function / Tool calling
description: How to implement function calling in AI models, allowing the LLM to execute functions as part of its response generation.
ms.topic: how-to
zone_pivot_groups: dev-lang
ms.date: 05/15/2026
---
# Function / Tool calling

::: zone pivot="python"
This article is not available for the selected development language.
::: zone-end

::: zone pivot="csharp"
It's possible to hook up functions that the LLM can decide to call if it thinks it can help with the task at hand. This is done by registering functions with a `ChatPrompt` using the `.Function()` method.
::: zone-end

::: zone pivot="typescript"
It's possible to hook up functions that the LLM can decide to call if it thinks it can help with the task at hand. This is done by adding a `function` to the `ChatPrompt`.
::: zone-end



::: zone pivot="csharp"
:::image type="content" source="~/assets/diagrams/function-calling.png" alt-text="Sequence diagram showing function calling flow for a Pokemon search through an external API in C#" lightbox="~/assets/diagrams/function-calling.png":::

::: zone-end

::: zone pivot="typescript"
:::image type="content" source="~/assets/diagrams/function-calling-2.png" alt-text="Sequence diagram showing function calling flow for a Pokemon search through an external API in TypeScript" lightbox="~/assets/diagrams/function-calling-2.png":::

::: zone-end




::: zone pivot="csharp"
## Single Function Example

Here's a complete example showing how to create a Pokemon search function that the LLM can call.


# [Imperative](#tab/imperative)


```csharp
using System.Text.Json;
using Microsoft.Teams.AI.Annotations;
using Microsoft.Teams.AI.Models.OpenAI;
using Microsoft.Teams.AI.Prompts;
using Microsoft.Teams.AI.Templates;
using Microsoft.Teams.Api.Activities;
using Microsoft.Teams.Apps;

/// <summary>
/// Handle Pokemon search using PokeAPI
/// </summary>
public static async Task<string> PokemonSearchFunction([Param("pokemon_name")] string pokemonName)
{
    try
    {
        using var client = new HttpClient();
        var response = await client.GetAsync($"https://pokeapi.co/api/v2/pokemon/{pokemonName.ToLower()}");

        if (!response.IsSuccessStatusCode)
        {
            return $"Pokemon '{pokemonName}' not found";
        }

        var json = await response.Content.ReadAsStringAsync();
        var data = JsonDocument.Parse(json);
        var root = data.RootElement;

        var name = root.GetProperty("name").GetString();
        var height = root.GetProperty("height").GetInt32();
        var weight = root.GetProperty("weight").GetInt32();
        var types = root.GetProperty("types")
            .EnumerateArray()
            .Select(t => t.GetProperty("type").GetProperty("name").GetString())
            .ToList();

        return $"Pokemon {name}: height={height}, weight={weight}, types={string.Join(", ", types)}";
    }
    catch (Exception ex)
    {
        return $"Error searching for Pokemon: {ex.Message}";
    }
}

/// <summary>
/// Handle single function calling - Pokemon search
/// </summary>
public static async Task HandlePokemonSearch(OpenAIChatModel model, IContext<MessageActivity> context)
{
    var prompt = new OpenAIChatPrompt(model, new ChatPromptOptions
    {
        Instructions = new StringTemplate("You are a helpful assistant that can look up Pokemon for the user.")
    });

    // Register the pokemon search function
    prompt.Function(
        "pokemon_search",
        "Search for pokemon information including height, weight, and types",
        PokemonSearchFunction
    );

    var result = await prompt.Send(context.Activity.Text);

    if (result.Content != null)
    {
        var message = new MessageActivity
        {
            Text = result.Content,
        }.AddAIGenerated();
        await context.Send(message);
    }
    else
    {
        await context.Reply("Sorry I could not find that pokemon");
    }
}
```

# [Declarative](#tab/declarative)


    This approach uses attributes to declare prompts and functions, providing clean separation of concerns.

    **Create a Prompt Class:**

```csharp
using System.Text.Json;
using Microsoft.Teams.AI.Annotations;

namespace Samples.AI.Prompts;

[Prompt]
[Prompt.Description("Pokemon search assistant")]
[Prompt.Instructions("You are a helpful assistant that can look up Pokemon for the user.")]
public class PokemonPrompt
{
    [Function]
    [Function.Description("Search for pokemon information including height, weight, and types")]
    public async Task<string> PokemonSearch([Param("pokemon_name")] string pokemonName)
    {
        try
        {
            using var httpClient = new HttpClient();
            var response = await httpClient.GetAsync($"https://pokeapi.co/api/v2/pokemon/{pokemonName.ToLower()}");

            if (!response.IsSuccessStatusCode)
            {
                return $"Pokemon '{pokemonName}' not found";
            }

            var json = await response.Content.ReadAsStringAsync();
            var data = JsonDocument.Parse(json);
            var root = data.RootElement;

            var name = root.GetProperty("name").GetString();
            var height = root.GetProperty("height").GetInt32();
            var weight = root.GetProperty("weight").GetInt32();
            var types = root.GetProperty("types")
                .EnumerateArray()
                .Select(t => t.GetProperty("type").GetProperty("name").GetString())
                .ToList();

            return $"Pokemon {name}: height={height}, weight={weight}, types={string.Join(", ", types)}";
        }
        catch (Exception ex)
        {
            return $"Error searching for Pokemon: {ex.Message}";
        }
    }
}
```

    **Usage in Program.cs:**

```csharp
using Microsoft.Teams.AI.Models.OpenAI;
using Microsoft.Teams.Api.Activities;

// Create the AI model
var aiModel = new OpenAIChatModel(azureOpenAIModel, azureOpenAI);

// Use the prompt with OpenAIChatPrompt.From()
teamsApp.OnMessage(async (context, cancellationToken) =>
{
    var prompt = OpenAIChatPrompt.From(aiModel, new Samples.AI.Prompts.PokemonPrompt());

    var result = await prompt.Send(context.Activity.Text);

    if (!string.IsNullOrEmpty(result.Content))
    {
        await context.Send(new MessageActivity { Text = result.Content }.AddAIGenerated(), cancellationToken);
    }
    else
    {
        await context.Reply("Sorry I could not find that pokemon", cancellationToken);
    }
});
```

---


### How It Works

1. **Function Definition**: The function is defined as a regular C# method with parameters decorated with the `[Param]` attribute
2. **Automatic Schema Generation**: The SDK automatically generates the JSON schema for the function parameters using reflection
3. **Function Registration**:
   - **Imperative Approach**: The `.Function()` method registers the function with the prompt, providing the name, description, and handler
   - **Declarative Approach**: The `[Function]` attribute automatically registers methods when using `OpenAIChatPrompt.From()`
4. **Automatic Invocation**: When the LLM decides to call the function, it automatically:
   - Parses the function call arguments
   - Validates them against the schema
   - Invokes the handler
   - Returns the result back to the LLM
::: zone-end

::: zone pivot="typescript"
```typescript
import { ChatPrompt, IChatModel } from '@microsoft/teams.ai';
import { ActivityLike, IMessageActivity } from '@microsoft/teams.api';
// ...

const prompt = new ChatPrompt({
  instructions: 'You are a helpful assistant that can look up Pokemon for the user.',
  model,
})
  // Include `function` as part of the prompt
  .function(
    'pokemonSearch',
    'search for pokemon',
    // Include the schema of the parameters
    // the LLM needs to return to call the function
    {
      type: 'object',
      properties: {
        pokemonName: {
          type: 'string',
          description: 'the name of the pokemon',
        },
      },
      required: ['text'],
    },
    // The cooresponding function will be called
    // automatically if the LLM decides to call this function
    async ({ pokemonName }: IPokemonSearch) => {
      log.info('Searching for pokemon', pokemonName);
      const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${pokemonName}`);
      if (!response.ok) {
        throw new Error('Pokemon not found');
      }
      const data = await response.json();
      // The result of the function call is sent back to the LLM
      return {
        name: data.name,
        height: data.height,
        weight: data.weight,
        types: data.types.map((type: { type: { name: string } }) => type.type.name),
      };
    }
  );

// The LLM will then produce a final response to be sent back to the user
// activity.text could have text like 'pikachu'
const result = await prompt.send(activity.text);
await send(result.content ?? 'Sorry I could not find that pokemon');
```
::: zone-end




::: zone pivot="csharp"
## Multiple Functions

Additionally, for complex scenarios, you can add multiple functions to the `ChatPrompt`. The LLM will then decide which function(s) to call based on the context of the conversation.

# [Imperative](#tab/imperative)


```csharp
/// <summary>
/// Get user location (mock)
/// </summary>
public static string GetLocationFunction()
{
    var locations = new[] { "Seattle", "San Francisco", "New York" };
    var random = new Random();
    var location = locations[random.Next(locations.Length)];
    return location;
}

/// <summary>
/// Get weather for location (mock)
/// </summary>
public static string GetWeatherFunction([Param] string location)
{
    var weatherByLocation = new Dictionary<string, (int Temperature, string Condition)>
    {
        ["Seattle"] = (65, "sunny"),
        ["San Francisco"] = (60, "foggy"),
        ["New York"] = (75, "rainy")
    };

    if (!weatherByLocation.TryGetValue(location, out var weather))
    {
        return "Sorry, I could not find the weather for that location";
    }

    return $"The weather in {location} is {weather.Condition} with a temperature of {weather.Temperature}°F";
}

/// <summary>
/// Handle multiple function calling - location then weather
/// </summary>
public static async Task HandleMultipleFunctions(OpenAIChatModel model, IContext<MessageActivity> context)
{
    var prompt = new OpenAIChatPrompt(model, new ChatPromptOptions
    {
        Instructions = new StringTemplate("You are a helpful assistant that can help the user get the weather. First get their location, then get the weather for that location.")
    });

    // Register both functions
    prompt.Function(
        "get_user_location",
        "Gets the location of the user",
        GetLocationFunction
    );

    prompt.Function(
        "weather_search",
        "Search for weather at a specific location",
        GetWeatherFunction
    );

    var result = await prompt.Send(context.Activity.Text);

    if (result.Content != null)
    {
        var message = new MessageActivity
        {
            Text = result.Content,
        }.AddAIGenerated();
        await context.Send(message);
    }
    else
    {
        await context.Reply("Sorry I could not figure it out");
    }
}
```

# [Declarative](#tab/declarative)


    **Create a Prompt Class:**

```csharp
using Microsoft.Teams.AI.Annotations;

namespace Samples.AI.Prompts;

[Prompt]
[Prompt.Description("Weather assistant")]
[Prompt.Instructions("You are a helpful assistant that can help the user get the weather. First get their location, then get the weather for that location.")]
public class WeatherPrompt
{
    [Function]
    [Function.Description("Gets the location of the user")]
    public string GetUserLocation()
    {
        var locations = new[] { "Seattle", "San Francisco", "New York" };
        var random = new Random();
        return locations[random.Next(locations.Length)];
    }

    [Function]
    [Function.Description("Search for weather at a specific location")]
    public string WeatherSearch([Param] string location)
    {
        var weatherByLocation = new Dictionary<string, (int Temperature, string Condition)>
        {
            ["Seattle"] = (65, "sunny"),
            ["San Francisco"] = (60, "foggy"),
            ["New York"] = (75, "rainy")
        };

        if (!weatherByLocation.TryGetValue(location, out var weather))
        {
            return "Sorry, I could not find the weather for that location";
        }

        return $"The weather in {location} is {weather.Condition} with a temperature of {weather.Temperature}°F";
    }
}
```

    **Usage in Program.cs:**

```csharp
using Microsoft.Teams.AI.Models.OpenAI;
using Microsoft.Teams.Api.Activities;

// Create the AI model
var aiModel = new OpenAIChatModel(azureOpenAIModel, azureOpenAI);

// Use the prompt with OpenAIChatPrompt.From()
teamsApp.OnMessage(async (context, cancellationToken) =>
{
    var prompt = OpenAIChatPrompt.From(aiModel, new Samples.AI.Prompts.WeatherPrompt());

    var result = await prompt.Send(context.Activity.Text);

    if (!string.IsNullOrEmpty(result.Content))
    {
        await context.Send(new MessageActivity { Text = result.Content }.AddAIGenerated(), cancellationToken);
    }
    else
    {
        await context.Reply("Sorry I could not figure it out", cancellationToken);
    }
});
```

---


### Multiple Function Execution Flow

When you register multiple functions:

1. The LLM receives information about all available functions
2. Based on the user's query, it decides which function(s) to call and in what order
3. For example, asking "What's the weather?" might trigger:
   - First: `get_user_location()` to determine where the user is
   - Then: `weather_search(location)` to get the weather for that location
4. The LLM combines all function results to generate the final response

> [!TIP]
> The LLM can call functions sequentially - using the output of one function as input to another - without any additional configuration. This makes it powerful for complex, multi-step workflows.
::: zone-end

::: zone pivot="typescript"
## Multiple functions

Additionally, for complex scenarios, you can add multiple functions to the `ChatPrompt`. The LLM will then decide which function to call based on the context of the conversation. The LLM can pick one or more functions to call before returning the final response.

```typescript
import { ChatPrompt, IChatModel } from '@microsoft/teams.ai';
import { ActivityLike, IMessageActivity } from '@microsoft/teams.api';
// ...

// activity.text could be something like "what's my weather?"
// The LLM will need to first figure out the user's location
// Then pass that in to the weatherSearch
const prompt = new ChatPrompt({
  instructions: 'You are a helpful assistant that can help the user get the weather',
  model,
})
  // Include multiple `function`s as part of the prompt
  .function(
    'getUserLocation',
    'gets the location of the user',
    // This function doesn't need any parameters,
    // so we do not need to provide a schema
    async () => {
      const locations = ['Seattle', 'San Francisco', 'New York'];
      const randomIndex = Math.floor(Math.random() * locations.length);
      const location = locations[randomIndex];
      log.info('Found user location', location);
      return location;
    }
  )
  .function(
    'weatherSearch',
    'search for weather',
    {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: 'the name of the location',
        },
      },
      required: ['location'],
    },
    async ({ location }: { location: string }) => {
      const weatherByLocation: Record<string, {}> = {
        Seattle: { temperature: 65, condition: 'sunny' },
        'San Francisco': { temperature: 60, condition: 'foggy' },
        'New York': { temperature: 75, condition: 'rainy' },
      };

      const weather = weatherByLocation[location];
      if (!weather) {
        return 'Sorry, I could not find the weather for that location';
      }

      log.info('Found weather', weather);
      return weather;
    }
  );

// The LLM will then produce a final response to be sent back to the user
const result = await prompt.send(activity.text);
await send(result.content ?? 'Sorry I could not figure it out');
```
::: zone-end




::: zone pivot="csharp"
<!-- Not applicable -->
::: zone-end

::: zone pivot="typescript"
## Stopping Functions early

You'll notice that after the function responds, `ChatPrompt` re-sends the response from the function invocation back to the LLM which responds back with the user-facing message. It's possible to prevent this "automatic" function calling by passing in a flag

```typescript
import { ChatPrompt, IChatModel, Message } from '@microsoft/teams.ai';
import { ActivityLike, IMessageActivity } from '@microsoft/teams.api';
// ...

const result = await prompt.send(activity.text, {
  autoFunctionCalling: false, // Disable automatic function calling
});
// Extract the function call arguments from the result
const functionCallArgs = result.function_calls?.[0].arguments;

const firstCall = result.function_calls?.[0];
const fnResult = actualFunction(firstCall.arguments);
messages.push({
  role: 'function',
  function_id: firstCall.id,
  content: fnResult,
});

// Optionally, you can call the chat prompt again after updating the messages with the results
const result = await prompt.send('What should we do next?', {
  messages,
  autoFunctionCalling: true, // You can enable it here if you want
});
const functionCallArgs = result.function_calls?.[0].arguments; // Extract the function call arguments
await send(
  `The LLM responed with the following structured output: ${JSON.stringify(functionCallArgs, undefined, 2)}.`
);
```
::: zone-end
