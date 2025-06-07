from langchain_core.messages import ToolMessage
from pydantic import BaseModel, Field

from src.crop_growth_monitor_graph.graph import CropGrowthMonitorGraph
from src.primary_graph.state import CenterState


class InvokeCropGrowthMonitorAssistant(BaseModel):
    """
    将工作转交给专门处理作物生长监控的助理。
    """
    img_path: str = Field(
        description="图像存储的地址"
    )

    request: str = Field(
        description="用户想要了解的作物生长信息和作物生长指标"
    )

    assistant: str = Field(default="crop_growth_monitor_assistant", description="对应的assistant节点的名字")

    class Config:
        json_schema_extra = {
            "示例": {
                "img_path": "agent/wwc/graph2.png",
                "request": "我想知道这个作物的叶龄是多大？我想知道当前某个地块的作物出苗率是怎样的？。",
            }
        }


graph = CropGrowthMonitorGraph().graph
async def consult_crop_growth_monitor_assistant(state: CenterState):
    # 多重工具调用下获取调用ID和调用参数
    tool_call_id = None
    tool_request = None
    for tool_call in state["messages"][-1].tool_calls:
        if tool_call["name"] == InvokeCropGrowthMonitorAssistant.__name__:
            tool_call_id = tool_call["id"]
            tool_request = tool_call["args"]["request"]

    # 自定义输入参数
    assistant_input_format = {"messages": [{"role": "system", "content": tool_request}]}

    # 异步调用子图
    result = await graph.ainvoke(assistant_input_format)

    return {
        "messages": [
            ToolMessage(
                content=f"作物生长监测助手'crop_growth_monitor_assistant'返回消息:{result['messages'][-1].content}",
                tool_call_id=tool_call_id,
            )
        ]
    }
