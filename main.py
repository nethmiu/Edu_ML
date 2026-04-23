from langgraph.graph import StateGraph, END
from state import AgentState
from agents import summarizer_agent
from tools import file_reader_tool

# 1. පද්ධතියේ වැඩ ප්‍රවාහය (Graph) ආරම්භ කිරීම [cite: 13, 31]
workflow = StateGraph(AgentState)

# 2. පද්ධතියට Nodes එකතු කිරීම [cite: 17, 42]
# මෙහිදී "summarizer" යනු එක් සාමාජිකයෙකුගේ වගකීමකි [cite: 24, 48]
workflow.add_node("summarizer", summarizer_agent)

# 3. පද්ධතියේ ගමන් මග (Edges) සැකසීම [cite: 17, 42]
workflow.set_entry_point("summarizer")
workflow.add_edge("summarizer", END)

# 4. පද්ධතිය Compile කිරීම [cite: 13]
app = workflow.compile()

# 5. පද්ධතිය පරීක්ෂා කිරීම (Execution) [cite: 36, 52]
if __name__ == "__main__":
    # Custom Tool එක භාවිතා කර දත්ත කියවීම [cite: 19, 26, 33]
    initial_content = file_reader_tool("notes.txt") 
    
    if initial_content and not initial_content.startswith("Error"):
        # පද්ධතිය රන් කර ලැබෙන අවසාන ප්‍රතිඵලය ලබා ගැනීම [cite: 21]
        inputs = {"lecture_notes": initial_content}
        result = app.invoke(inputs)

        # අවසාන සාරාංශය තිරයේ පෙන්වීම [cite: 37]
        print("\n" + "="*30)
        print("FINAL SUMMARIZED OUTPUT:")
        print("="*30)
        print(result.get("summary", "සාරාංශයක් ලබා ගත නොහැකි විය."))
    else:
        print(f"පද්ධතිය ක්‍රියාත්මක කළ නොහැක: {initial_content}")