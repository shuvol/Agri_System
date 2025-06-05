from langchain_core.runnables import Runnable
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from configuration import Configuration
from src.environment_monitor_graph.prompt import environment_monitor_prompt
from src.environment_monitor_graph.state import EnvironmentMonitorState
from src.graph_common.assistant import AgriAssistant


class EnvironmentMonitorGraph:
    def __init__(self, tools=None):
        self.tools = tools or []
        self.graph = self.build_graph()

    def build_runnable(self) -> Runnable:
        llm = Configuration.new_llm()
        if self.tools:
            return environment_monitor_prompt | llm.bind_tools(self.tools)
        return environment_monitor_prompt | llm

    def build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(EnvironmentMonitorState)

        # Adding nodes
        graph.add_node("monitor_environment_assistant", AgriAssistant(self.build_runnable()))

        # Adding edges
        graph.add_edge(START, "monitor_environment_assistant")
        graph.add_edge("monitor_environment_assistant", END)

        return graph.compile()



