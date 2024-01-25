from typing import Any, Dict, List
from enum import Enum

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.tool import Tool
from core.model_manager import ModelInstance

class ModelTool(Tool):
    class ModelToolType(Enum):
        """
            the type of the model tool
        """
        VISION = 'vision'

    model_instance: ModelInstance
    tool_type: ModelToolType
    """
    Api tool
    """
    def fork_tool_runtime(self, meta: Dict[str, Any]) -> 'Tool':
        """
            fork a new tool with meta data

            :param meta: the meta data of a tool call processing, tenant_id is required
            :return: the new tool
        """
        return self.__class__(
            identity=self.identity.copy() if self.identity else None,
            parameters=self.parameters.copy() if self.parameters else None,
            description=self.description.copy() if self.description else None,
            runtime=Tool.Runtime(**meta)
        )

    def validate_credentials(self, credentials: Dict[str, Any], parameters: Dict[str, Any], format_only: bool = False) -> None:
        """
            validate the credentials for Model tool
        """
        pass

    def _invoke(self, user_id: str, tool_paramters: Dict[str, Any]) -> ToolInvokeMessage | List[ToolInvokeMessage]:
        """
        invoke http request
        """
        pass