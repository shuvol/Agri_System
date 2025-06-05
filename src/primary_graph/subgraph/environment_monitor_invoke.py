"""定义调用环境监测子图助手所需的类和方法"""

from langchain_core.messages import ToolMessage
from pydantic import BaseModel, Field

from src.environment_monitor_graph.graph import EnvironmentMonitorGraph
from src.primary_graph.state import CenterState


class InvokeEnvironmentMonitorAssistant(BaseModel):
    """
    咨询环境数据采集与分析的环境监测助理。
    """

    request: str = Field(
        description="用户想要了解的环境的地点"
    )

    assistant: str = Field(default="monitor_environment_assistant", description="对应的assistant节点的名字")




graph = EnvironmentMonitorGraph().graph
async def consult_monitor_environment_assistant(state: CenterState):
    # 多重工具调用下获取工具调用ID和调用参数
    tool_call_id = None
    tool_request = None
    for tool_call in state["messages"][-1].tool_calls:
        if tool_call["name"] == InvokeEnvironmentMonitorAssistant.__name__:
            tool_call_id = tool_call["id"]
            tool_request = tool_call["args"]["request"]

    # 自定义输入参数
    assistant_input_format = {"messages": [{"role": "system", "content": tool_request}]}

    # 异步调用子图
    result = await graph.ainvoke(assistant_input_format)

    return {
        "messages": [
            ToolMessage(
                content=f"环境监测助手'monitor_environment_assistant'返回消息:{result['messages'][-1].content}",
                tool_call_id=tool_call_id,
            )
        ]
    }
