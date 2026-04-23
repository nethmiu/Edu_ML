from langgraph.graph import StateGraph, END
from state import AgentState
from agents import summarizer_agent
from tools import file_reader_tool

# 1. Initializing the system workflow (Graph)
workflow = StateGraph(AgentState)

# 2. Adding Nodes to the system
# Here "summarizer" represents the responsibility of one member
workflow.add_node("summarizer", summarizer_agent)

# 3. Setting up the system flow (Edges)
workflow.set_entry_point("summarizer")
workflow.add_edge("summarizer", END)

# 4. Compiling the system
app = workflow.compile()

# 5. Testing the system (Execution)
if __name__ == "__main__":
    # Reading data using the Custom Tool
    initial_content = file_reader_tool("notes.txt") 
    
    if initial_content and not initial_content.startswith("Error"):
        # Running the system and getting the final result
        inputs = {"lecture_notes": initial_content}
        result = app.invoke(inputs)

        # Displaying the final summary on the screen
        print("\n" + "="*30)
        print("FINAL SUMMARIZED OUTPUT:")
        print("="*30)
        print(result.get("summary", "Could not retrieve the summary."))
    else:
        print(f"Could not execute the system: {initial_content}")