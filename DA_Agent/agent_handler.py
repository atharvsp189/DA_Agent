import os
import json
import logging
from llama_index.llms.gemini import Gemini
from .tool_handler import ToolHandler

from dotenv import load_dotenv
load_dotenv()

with open(os.path.join(os.getcwd(), "config.json"), 'r') as f:
    config = json.loads(f.read())

llm = Gemini(
    model=config["llm"]["model"],
    temperature=config["llm"]["temperature"],
    api_key=os.getenv("GOOGLE_API_KEY"),
)

class AgentHandler:
    def __init__(self):
        self.llm = llm
        self.tool_handler = ToolHandler()
        self.tools = self.tool_handler.get_tools()
        logging.info(f"Initialized Data Analytics AI Agent with {len(self.tools)} tools")

    def process_user_input(self, messages: list, df):

        try:
            response = self.llm.chat_with_tools(
                messages=messages,
                tools=self.tools,
                allow_parallel_tool_calls=False,
                verbose=True,
            )
            print("Response : ", response)
        except Exception as e:
            logging.error(f"Error during LLM processing: {type(e).__name__}: {e}")
            return None

        tool_map = {tool.metadata.name: tool.fn for tool in self.tools}
        logging.info(f"Tool map keys: {tool_map.keys()}")
        tool_calls = response.message.additional_kwargs.get("tool_calls", [])
        logging.info(f"Tool calls: {tool_calls}")
        if not tool_calls:
            logging.info("No tool calls in LLM response")
            return f"No tools called by LLM"

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            logging.info(f"Processing tool call: {tool_name}")
            tool_func = tool_map.get(tool_name)
            if not tool_func:
                logging.error(f"Tool {tool_name} not found in tool_map: {tool_map.keys()}")
                continue
            try:
                if tool_name == "query_dataframe":
                    args = json.loads(tool_call.function.arguments or "{}")
                    code = args.get("code", " ")
                    result = tool_func(code)
                    logging.info(f"Executing tool {tool_name} with code {code}")
                    return result
            except Exception as e:
                logging.error(f"Error executing tool {tool_name}: {type(e).__name__}: {e}")