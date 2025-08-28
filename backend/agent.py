from typing import TypedDict
import pandas as pd
from backend.data_cleaning import DataClean
from langgraph.graph import StateGraph

class AgentState(TypedDict, total=False):
    input : pd.DataFrame
    process : pd.DataFrame
    output : pd.DataFrame
    
class Agent():
    def __init__(self, df, batch_size = 20) -> None:
        self.batch_size = batch_size
        self.clean = DataClean() 
        
    def missing_node_start(self, state : AgentState) -> AgentState:
        answer = self.clean.fill_na(state.get("input"))
        if answer is not None:
            state["process"] = answer
            
        return state
               
    def llm_handling_node(self, state : AgentState) -> AgentState:
        answer = self.clean.llm_handling(state.get("process"), self.batch_size)
        if answer is not None:
            state["process"] = answer
            
        return state
    
    def encoding_node(self, state : AgentState) -> AgentState:
        answer = self.clean.encoding(state.get("process"))
        if answer is not None:
            state["process"] = answer
            
        return state
    
    def missing_node_last(self, state : AgentState) -> AgentState:
        answer = self.clean.fill_na(state.get("process"))
        if answer is not None:
            state["output"] = answer
            
        return state
    
    def get_app(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("start_missing", self.missing_node_start)
        workflow.add_node("llm_handling", self.llm_handling_node)
        workflow.add_node("encoding", self.encoding_node)
        workflow.add_node("end_missing", self.missing_node_last)
        
        workflow.add_edge("start_missing", "llm_handling")
        workflow.add_edge("llm_handling", "encoding")
        workflow.add_edge("encoding", "end_missing")
        
        workflow.set_entry_point("start_missing")
        workflow.set_finish_point("end_missing")
        
        app = workflow.compile()
        
        with open("graph.png", "wb") as file:
            file.write(app.get_graph().draw_mermaid_png())
            
        return app