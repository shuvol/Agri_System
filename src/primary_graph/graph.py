from langchain_core.runnables import Runnable
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from configuration import Configuration
from src.graph_common.assistant import AgriAssistant
from src.primary_graph.prompt import center_assistant_prompt
from src.primary_graph.state import CenterState
from src.primary_graph.subgraph.crop_growth_monitor_invoke import consult_crop_growth_monitor_assistant, \
    InvokeCropGrowthMonitorAssistant
from src.primary_graph.subgraph.disease_pest_invoke import (
    InvokeDiseaseAndPestAssistant, consult_disease_pest_assistant)
from src.primary_graph.subgraph.environment_monitor_invoke import (
    InvokeEnvironmentMonitorAssistant, consult_monitor_environment_assistant)


class PrimaryGraph:
    def __init__(self, assistants=None, tools=None):
        self.assistants = assistants or [
            InvokeEnvironmentMonitorAssistant,
            InvokeDiseaseAndPestAssistant,
            InvokeCropGrowthMonitorAssistant
        ]
        self.tools = tools or []
        self.graph = self.build_graph()

    def build_runnable(self) -> Runnable:
        llm = Configuration.new_llm()
        if self.tools or self.assistants:
            return center_assistant_prompt | llm.bind_tools(self.assistants + self.tools)
        return center_assistant_prompt | llm

    def route(self, state: CenterState):
        messages = state.get("messages", [])
        if not messages:
            raise ValueError("No message found in input")

        tools_by_name = {tool.__name__: tool for tool in self.assistants}
        message = messages[-1]

        return [
            tools_by_name[call["name"]].model_fields["assistant"].default
            for call in message.tool_calls
        ]

    def build_graph(self):
        graph = StateGraph(CenterState)

        # Adding nodes
        graph.add_node("center_assistant", AgriAssistant(self.build_runnable()))
        graph.add_node("disease_pest_assistant", consult_disease_pest_assistant)
        graph.add_node("monitor_environment_assistant", consult_monitor_environment_assistant)
        graph.add_node("crop_growth_monitor_assistant", consult_crop_growth_monitor_assistant)

        # Adding edges
        graph.add_edge(START, "center_assistant")
        graph.add_conditional_edges(
            "center_assistant",
            self.route,
            ["disease_pest_assistant", "monitor_environment_assistant", "crop_growth_monitor_assistant", END]
        )
        graph.add_edge("disease_pest_assistant", "center_assistant")
        graph.add_edge("monitor_environment_assistant", "center_assistant")
        graph.add_edge("crop_growth_monitor_assistant", "center_assistant")

        return graph.compile()

