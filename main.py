
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from tools import get_weather, get_population
from middleware import log_tool_calls

load_dotenv(override=True)

# Create memory
memory = MemorySaver()

# Create agent
agent = create_agent(
    model="groq:qwen/qwen3.8-27b",
    tools=[get_weather, get_population],
    checkpointer=memory,
    middleware=[log_tool_calls],
    system_prompt="""
    You are a helpful travel assistant.

    Use the available tools to answer questions
    about weather and population.

    Remember previous conversation details.
    """
)

# Conversation ID
config = {
    "configurable": {
        "thread_id": "travel-session-1"
    }
}

print("Travel Assistant Started!")
print("Type 'exit' to stop.\n")

while True:

    user_query = input("You: ")

    if user_query.lower() == "exit":
        break

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        },
        config=config
    )

    print("\nAgent:", result["messages"][-1].content)
