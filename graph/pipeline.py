from langgraph.graph import StateGraph, END
from graph.state import QASentinelState
from agents.ticket_reader import ticket_reader_node
from agents.test_case_writer import test_case_writer_node
from agents.quality_checker import quality_checker_node, should_revise
from agents.script_generator import script_generator_node

def build_pipeline():
    workflow = StateGraph(QASentinelState)

    workflow.add_node("ticket_reader", ticket_reader_node)
    workflow.add_node("test_case_writer", test_case_writer_node)
    workflow.add_node("quality_checker", quality_checker_node)
    workflow.add_node("script_generator", script_generator_node)

    workflow.set_entry_point("ticket_reader")
    workflow.add_edge("ticket_reader", "test_case_writer")
    workflow.add_edge("test_case_writer", "quality_checker")
    workflow.add_conditional_edges(
        "quality_checker",
        should_revise,
        {
            "approved": "script_generator",
            "needs_revision": "test_case_writer"
        }
    )
    workflow.add_edge("script_generator", END)
    return workflow.compile()

app = build_pipeline()