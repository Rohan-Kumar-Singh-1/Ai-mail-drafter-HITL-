import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from state import EmailState
from nodes import drafter_node, send_node

conn = sqlite3.connect("emails.db", check_same_thread=False)

memory = SqliteSaver(conn)

builder = StateGraph(EmailState)

builder.add_node("drafter", drafter_node)
builder.add_node("send", send_node)

builder.set_entry_point("drafter")


def router(state):

    if state.get("approved") is True:
        return "send"

    if state.get("approved") is False:
        return "drafter"

    return END


builder.add_conditional_edges(
    "drafter",
    router,
    {
        "send": "send",
        "drafter": "drafter",
        END: END,
    },
)

builder.add_edge("send", END)

graph = builder.compile(checkpointer=memory)