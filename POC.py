import os
import json
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.tools import FunctionTool
from llama_index.core.llms import ChatMessage
import streamlit as st

# Import Libraries for Analysis
import pandas as pd
import numpy as np
import openpyxl as pyx

# Import Libararies for Visualization
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Use Windows Installed fonts for rendering devnaagri text
plt.rcParams['font.family'] = ['Nirmala UI']
plt.rcParams['axes.unicode_minus'] = False

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with open(os.path.join(os.getcwd(), "config.json"), 'r') as f:
    config = json.loads(f.read())

llm = GoogleGenAI(
    model=config["llm"]["model"],
    temperature=config["llm"]["temperature"],
    api_key=os.getenv("GOOGLE_API_KEY"),
)

# Functions

def query_dataframe(code: str):
    """Executes Python code on the dataframe `df` and returns result + code."""
    try:
        # Eval the result
        print("Generated Code: ", code)
        result = eval(code)
        return result
    except Exception as e:
        return f"Error: {e}"

def visualize_data(code: str):
    """
    Executes code for seaborn/matplotlib plot using global df,
    saves the figure to disk, and returns image path.
    """
    global df
    image_filename = "seaborn_plot.png"
    image_path = os.path.join("plots", image_filename)

    try:
        print("Generated Code:\n", code)
        exec(code)
        fig = plt.gcf()
        os.makedirs("plots", exist_ok=True)
        fig.savefig(image_path, bbox_inches='tight', dpi=300)
        fig.show()
        plt.close(fig)
        print(f"Visualization saved to: {image_path}")
        return image_path

    except Exception as e:
        print("Error during visualization:")
        return None


# Tools

tools = {}
tools["query_dataframe"] = FunctionTool.from_defaults(
        fn=query_dataframe,
        name="query_dataframe",
        description="Use this tool to query the pandas dataframe and return the filtered dataframe we got after the query"
        )

tools["visualize_data"] = FunctionTool.from_defaults(
        fn=visualize_data,
        name="visualize_data",
        description="takes the seaborn code for visualization and return the image path"
)

tool_map = {tool: tools[tool] for tool in tools.keys()}
print(f"Tool map keys: {tool_map.keys()}")

# Agent




# Streamlit App
st.set_page_config(page_title="CSV Chat Assistant", layout="wide")
st.title("📊 Chat with CSV/Excel")
print("Starting Program")

# File Upload
uploaded_file = st.file_uploader("📁 Upload your CSV/Excel File", type=["csv", "xls"])

# Global chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'results' not in st.session_state:
    st.session_state.results = [] 

# if uploaded_file:
#     try:
#         if(uploaded_file.name.endswith(".csv")):
#             df = pd.read_csv(uploaded_file)
#             logging.info(f"Successfully Uploaded File. {uploaded_file.name}")
#         elif(uploaded_file.name.endswith(".xls")):
#             df = pd.read_excel(uploaded_file)
#             logging.info(f"Successfully Uploaded File. {uploaded_file.name}")
#         # normalizing columns
#         columns = [col.strip(" ").lower() for col in df.columns]
#         print(columns)
#         df.columns = columns
#     except Exception as e:
#         st.error(f"Failed to read file: {e}")

filtered_df = pd.DataFrame()

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            logging.info(f"Successfully Uploaded File. {uploaded_file.name}")
        elif uploaded_file.name.endswith(".xls"):
            df = pd.read_excel(uploaded_file)
            logging.info(f"Successfully Uploaded File. {uploaded_file.name}")

        # Normalize column names
        columns = [col.strip(" ").lower() for col in df.columns]
        df.columns = columns

        # Fix duplicate column names
        if df.columns.duplicated().any():
            df.columns = [f"{col}_{i}" if df.columns.duplicated()[i] else col 
                            for i, col in enumerate(df.columns)]
            logging.warning("Duplicate column names found and renamed.")

        print(df.columns)

    except Exception as e:
        st.error(f"Failed to read file: {e}")

    system_prompt = f"""
            You are a Data Analysis Agent which Analyzes the Pandas Dataframe. You provide with the right tool and its arguments.

            You have tool like:
            query_dataframe -> which allows you to query the pandas dataframe using code
            visualize_data -> which provide you with the seaborn visualization

            Columns of the dataframe are : {df.columns}

            HARD RULES:
            - Use only the column name provided. DO NOT INVENT column name.
    """
# Show DataFrame preview
    with st.expander("🔍 Preview DataFrame"):
        st.dataframe(df.head(10))

    # --- Chat Interface ---
    st.markdown("### 💬 Ask your questions below:")

    if prompt:=st.chat_input("Let me help you with insights from the data?"):
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=prompt),
        ]
        with st.chat_message("user"):
            st.markdown(prompt)
        response = llm.chat_with_tools(
                        messages=messages,
                        tools=list(tools.values()),
                        allow_parallel_tool_calls=False,
                        verbose=True,
            )
        logging.info(f"LLM response Generated : {response}")

        tool_calls = response.message.additional_kwargs.get("tool_calls", [])
        logging.info(f"Tool calls: {tool_calls}")
        if not tool_calls:
            logging.info("No tool calls in LLM response")

        for tool_call in tool_calls:
            tool_name = tool_call.name
            logging.info(f"Processing tool call: {tool_name}")
            tool_func = tool_map[tool_name]
            logging.info(tool_func)
            if not tool_func:
                logging.info(f"Tool {tool_name} not found in tool_map: {tool_map.keys()}")
                continue
            try:
                if tool_name == "query_dataframe":
                    args = tool_call.args
                    code = args["code"]
                    if not isinstance(code, str) or not code.strip():
                        logging.info(f"Skipping {tool_name} with invalid or empty code: {code}")
                        continue
                    result = tool_func(code)
                    try:
                        with st.chat_message("assistant"):
                            if isinstance(result.raw_output, pd.DataFrame):
                                filtered_df = result.raw_output
                                
                                reply = f"Successfully retrieved the data with a Query: {result.raw_input['args']}"
                                st.markdown(reply)
                                st.session_state.results.append({"role": "query_result", "content": result.raw_output})
                                with st.expander("View Results"):
                                    st.dataframe(result.raw_output)
                            else:
                                reply = str(result.raw_output)
                                st.markdown(reply)
                        logging.info(f"Executing tool {tool_name} with Code: {code}")
                        # logging.info(f"Tool {tool_name} result: {result}")
                    except Exception as e:
                        logging.info(f"An Error Occurred: {e}")
            except Exception as e:
                logging.info(f"Error executing tool {tool_name}: {type(e).__name__}: {e}")
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": reply})
        
        # for message in st.session_state.messages:
        #     with st.chat_message(message["role"]):
        #         st.markdown(message["content"])
        # if st.session_state.results:
        #     st.subheader("📊 Previous Query Results")
        #     for i, (desc, df) in enumerate(st.session_state.results):
        #         with st.expander(f"Result {i+1}: {desc}"):
        #             st.dataframe(df)

        # # Display chat history
        # for sender, message in st.session_state.messages:
        #     if sender == "You":
        #         st.markdown(f"**🧑 You:** {message}")
        #     else:
        #         st.markdown(f"**🤖 Bot:** {message}")
        #         st.dataframe(filtered_df)


# elif not openai_api_key:
#     st.warning("⚠️ Please enter your OpenAI API Key to continue.")

elif not uploaded_file:
    st.info("📤 Upload a CSV file to begin chatting!")


