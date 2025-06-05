"""病虫害防治智能体 State"""

from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages



class DiseasePestState(TypedDict):
    """
    病虫害防治智能体 State结构
    """

    messages: Annotated[list[AnyMessage], add_messages]