from langgraph.graph import StateGraph, END
from state import AgentState
from agents import summarizer_agent
from tools import file_reader_tool

# ග්‍රාෆ් එක ආරම්භ කිරීම
workflow = StateGraph(AgentState)

# Nodes එකතු කිරීම [cite: 42]
workflow.add_node("summarizer", summarizer_agent)

# ග්‍රාෆ් එකේ ගමන් මග (Edges) [cite: 17]
workflow.set_entry_point("summarizer")
workflow.add_edge("summarizer", END)

# ග්‍රාෆ් එක compile කිරීම
app = workflow.compile()

# පද්ධතිය ක්‍රියාත්මක කිරීම (Testing)
initial_content = file_reader_tool("notes.txt") # notes.txt ලෙස file එකක් සාදා ගන්න
app.invoke({"lecture_notes": initial_content})