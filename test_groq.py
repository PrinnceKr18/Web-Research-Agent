from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool

load_dotenv(override=True)

@tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny."

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

model_with_tools = model.bind_tools([get_weather])

response = model_with_tools.invoke(
    "What is the weather in Jaipur? Use the get_weather tool."
)

print("Response:", response)
print("Tool calls:", response.tool_calls)