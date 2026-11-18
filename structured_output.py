
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.agents import create_agent

from tools import get_weather, get_population

load_dotenv(override=True)


# 1. Define the output schema
class CityReport(BaseModel):

    city: str = Field(
        description="Name of the city"
    )

    weather: str = Field(
        description="Weather information of the city"
    )

    population: str = Field(
        description="Population of the city"
    )


# 2. Create agent with structured output
agent = create_agent(
    model="groq:qwen/qwen3.8-27b",
    tools=[get_weather, get_population],
    response_format=CityReport,
    system_prompt="""
    You are a city information assistant.

    Use the available tools to get weather
    and population information.

    Return the result in the required structure.
    Do not invent missing information.
    """
)


# 3. Get user input
city = input("Enter city name: ")


# 4. Execute agent
result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": f"Generate a report for {city}."
        }
    ]
})


# 5. Extract structured response
report = result["structured_response"]


# 6. Display results
print("\nCity Report")
print("----------------------")

print("City:", report.city)
print("Weather:", report.weather)
print("Population:", report.population)


# Convert Pydantic object into dictionary
print("\nDictionary format:")
print(report.model_dump())
