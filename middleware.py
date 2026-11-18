
from langchain.agents.middleware import wrap_tool_call


@wrap_tool_call
def log_tool_calls(request, handler):

    call = request.tool_call

    print("\n[MIDDLEWARE] Tool call detected")
    print("Tool name:", call["name"])
    print("Arguments:", call["args"])

    return handler(request)
