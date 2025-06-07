from langchain_core.runnables import Runnable
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from configuration import Configuration
from src.crop_growth_monitor_graph.prompt import crop_growth_monitor_prompt
from src.crop_growth_monitor_graph.state import CropGrowthMonitorState
from src.graph_common.assistant import AgriAssistant


class CropGrowthMonitorGraph:
    def __init__(self, tools=None):
        self.tools = tools or []
        self.graph = self.build_graph()

    def build_runnable(self) -> Runnable:
        llm = Configuration.new_llm()
        if self.tools:
            return crop_growth_monitor_prompt | llm.bind_tools(self.tools)
        return crop_growth_monitor_prompt | llm

    def build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(CropGrowthMonitorState)

        # Adding nodes
        graph.add_node("crop_growth_monitor_assistant", AgriAssistant(self.build_runnable()))

        # Adding edges
        graph.add_edge(START, "crop_growth_monitor_assistant")
        graph.add_edge("crop_growth_monitor_assistant", END)

        return graph.compile()


