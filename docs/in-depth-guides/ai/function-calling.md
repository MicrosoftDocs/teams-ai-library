---
sidebar_label: Function Calling
title: Function Calling
zone_pivot_groups: dev-lang
description: How to implement function calling in AI models, allowing the LLM to execute functions as part of its response generation.
---
# Function / Tool calling

::: zone pivot="csharp"
It's possible to hook up functions that the LLM can decide to call if it thinks it can help with the task at hand. This is done by registering functions with a `ChatPrompt` using the `.Function()` method.
::: zone-end

::: zone pivot="python,typescript"
It's possible to hook up functions that the LLM can decide to call if it thinks it can help with the task at hand. This is done by adding a `function` to the `ChatPrompt`.
::: zone-end


::: zone pivot="csharp"
![alt-text for function-calling-1.png](~/assets/diagrams/function-calling-1.png)
::: zone-end

::: zone pivot="python"
![alt-text for function-calling-2.png](~/assets/diagrams/function-calling-2.png)
::: zone-end

::: zone pivot="typescript"
![alt-text for function-calling-3.png](~/assets/diagrams/function-calling-3.png)
::: zone-end



::: zone pivot="csharp"
## Single Function Example

Here's a complete example showing how to create a Pokemon search function that the LLM can call.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

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
teamsApp.OnMessage(async (context) =>
{
    var prompt = OpenAIChatPrompt.From(aiModel, new Samples.AI.Prompts.PokemonPrompt());

    var result = await prompt.Send(context.Activity.Text);

    if (!string.IsNullOrEmpty(result.Content))
    {
        await context.Send(new MessageActivity { Text = result.Content }.AddAIGenerated());
    }
    else
    {
        await context.Reply("Sorry I could not find that pokemon");
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

::: zone pivot="python"
```python
import aiohttp
import random
from microsoft.teams.ai import Agent, Function
from microsoft.teams.api import MessageActivity, MessageActivityInput
from microsoft.teams.apps import ActivityContext
from microsoft.teams.openai import OpenAICompletionsAIModel
from pydantic import BaseModel

class SearchPokemonParams(BaseModel):
    pokemon_name: str
    """The name of the pokemon."""

async def pokemon_search_handler(params: SearchPokemonParams) -> str:
    """Search for Pokemon using PokeAPI - matches documentation example"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pokeapi.co/api/v2/pokemon/{params.pokemon_name.lower()}") as response:
                if response.status != 200:
                    raise ValueError(f"Pokemon '{params.pokemon_name}' not found")

                data = await response.json()

                result_data = {
                    "name": data["name"],
                    "height": data["height"],
                    "weight": data["weight"],
                    "types": [type_info["type"]["name"] for type_info in data["types"]],
                }

                return f"Pokemon {result_data['name']}: height={result_data['height']}, weight={result_data['weight']}, types={', '.join(result_data['types'])}"
    except Exception as e:
        raise ValueError(f"Error searching for Pokemon: {str(e)}")

@app.on_message
async def handle_message(ctx: ActivityContext[MessageActivity]):
    openai_model = OpenAICompletionsAIModel(model=AZURE_OPENAI_MODEL)
    agent = Agent(model=openai_model)
    agent.with_function(
        Function(
            name="pokemon_search",
            description="Search for pokemon information including height, weight, and types",
            # Include the schema of the parameters
            # the LLM needs to return to call the function
            parameter_schema=SearchPokemonParams,
            handler=pokemon_search_handler,
        )
    )

    chat_result = await agent.send(
            input=ctx.activity.text,
            instructions="You are a helpful assistant that can look up Pokemon for the user.",
        )

    if chat_result.response.content:
        message = MessageActivityInput(text=chat_result.response.content).add_ai_generated()
        await ctx.send(message)
    else:
        await ctx.reply("Sorry I could not find that pokemon")
```
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
teamsApp.OnMessage(async (context) =>
{
    var prompt = OpenAIChatPrompt.From(aiModel, new Samples.AI.Prompts.WeatherPrompt());

    var result = await prompt.Send(context.Activity.Text);

    if (!string.IsNullOrEmpty(result.Content))
    {
        await context.Send(new MessageActivity { Text = result.Content }.AddAIGenerated());
    }
    else
    {
        await context.Reply("Sorry I could not figure it out");
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

::: zone pivot="python"
## Multiple functions

Additionally, for complex scenarios, you can add multiple functions to the `ChatPrompt`. The LLM will then decide which function to call based on the context of the conversation. The LLM can pick one or more functions to call before returning the final response.

```python
import random
from microsoft.teams.ai import Agent, Function
from microsoft.teams.api import MessageActivity, MessageActivityInput
from microsoft.teams.apps import ActivityContext
from pydantic import BaseModel
# ...

class GetLocationParams(BaseModel):
    """No parameters needed for location"""
    pass

class GetWeatherParams(BaseModel):
    location: str
    """The location to get weather for"""

def get_location_handler(params: GetLocationParams) -> str:
    """Get user location (mock)"""
    locations = ["Seattle", "San Francisco", "New York"]
    location = random.choice(locations)
    return location

def get_weather_handler(params: GetWeatherParams) -> str:
    """Get weather for location (mock)"""
    weather_by_location = {
        "Seattle": {"temperature": 65, "condition": "sunny"},
        "San Francisco": {"temperature": 60, "condition": "foggy"},
        "New York": {"temperature": 75, "condition": "rainy"},
    }

    weather = weather_by_location.get(params.location)
    if not weather:
        return "Sorry, I could not find the weather for that location"

    return f"The weather in {params.location} is {weather['condition']} with a temperature of {weather['temperature']}°F"

@app.on_message
async def handle_multiple_functions(ctx: ActivityContext[MessageActivity]):
    agent = Agent(model)

    agent.with_function(
        Function(
            name="get_user_location",
            description="Gets the location of the user",
            parameter_schema=GetLocationParams,
            handler=get_location_handler,
        )
    ).with_function(
        Function(
            name="weather_search",
            description="Search for weather at a specific location",
            parameter_schema=GetWeatherParams,
            handler=get_weather_handler,
        )
    )

    chat_result = await agent.send(
        input=ctx.activity.text,
        instructions="You are a helpful assistant that can help the user get the weather. First get their location, then get the weather for that location.",
    )

    if chat_result.response.content:
        message = MessageActivityInput(text=chat_result.response.content).add_ai_generated()
        await ctx.send(message)
    else:
        await ctx.reply("Sorry I could not figure it out")
```
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
