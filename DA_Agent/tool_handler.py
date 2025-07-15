from llama_index.core.tools import FunctionTool
from .function_handler import query_dataframe

class ToolHandler:
    def __init__(self):
        self.tools = {}
        self._init_tools()

    def _init_tools(self):
        # Tool to send a WhatsApp message when the user asks for a human agent
        self.tools["query_dataframe"] = FunctionTool.from_defaults(
            fn=query_dataframe,
            name="query_dataframe",
            description="Use this tool to query the pandas dataframe and return the filtered dataframe we got after the query"
        )

    def get_tools(self):
        return list(self.tools.values())

# Agent