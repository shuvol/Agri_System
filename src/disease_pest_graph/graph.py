from langchain_core.runnables import Runnable
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from configuration import Configuration
from src.disease_pest_graph.prompt import disease_pest_prompt
from src.disease_pest_graph.state import DiseasePestState
from src.graph_common.assistant import AgriAssistant


class DiseasePestGraph:
    def __init__(self, tools=None):
        self.tools = tools or []
        self.graph = self.build_graph()

    def build_runnable(self) -> Runnable:
        llm = Configuration.new_llm()
        if self.tools:
            return disease_pest_prompt | llm.bind_tools(self.tools)
        return disease_pest_prompt | llm

    def build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(DiseasePestState)

        # Adding nodes
        graph.add_node("disease_pest_assistant", AgriAssistant(self.build_runnable()))

        # Adding edges
        graph.add_edge(START, "disease_pest_assistant")
        graph.add_edge("disease_pest_assistant", END)

        return graph.compile()


