
from langgraph.graph import StateGraph, START, END

from app.agents.state import EmailState
from app.agents.nodes import (
    analyze_email,
    generate_reply
)


def build_email_graph():

    workflow = StateGraph(EmailState)

    workflow.add_node(
        "analyze_email",
        analyze_email
    )

    workflow.add_node(
        "generate_reply",
        generate_reply
    )

    workflow.add_edge(
        START,
        "analyze_email"
    )

    workflow.add_edge(
        "analyze_email",
        "generate_reply"
    )

    workflow.add_edge(
        "generate_reply",
        END
    )

    return workflow.compile()


email_graph = build_email_graph()


def run_email_graph(
    email: str,
    tone: str,
    length: str
):

    result = email_graph.invoke({
        "email": email,
        "tone": tone,
        "length": length
    })

    return result

