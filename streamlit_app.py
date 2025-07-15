import json
import streamlit as st
import pandas as pd
import os
from DA_Agent import agent_handler


st.set_page_config(page_title="CSV Chat Assistant", layout="wide")
st.title("📊 CSV Chat Assistant")

# File Upload
uploaded_file = st.file_uploader("📁 Upload your CSV/Excel File", type=["csv", "xlsx"])

# Global chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file:
    try:
        if(uploaded_file.name.endswith(".csv")):
            df = pd.read_csv(uploaded_file)
        elif(uploaded_file.name.endswith(".xlsx")):
            df = pd.read_excel(uploaded_file)
        columns = df.columns
        system_prompt = f"""
            You are a Data Analysis Agent which Analyzes the Pandas Dataframe and provide with the insights and Visualization tools. and tells your findings honestly

            You have tool like:
            query_dataframe -> which allows you to query the pandas dataframe using code and provide with the insights
            visualize_data -> which provide you with the seaborn visualization

            Columns of the dataframe are : {columns}

            HARD RULES:
            - Use only the column provided not invent other column name.
        """

        # Show DataFrame preview
        with st.expander("🔍 Preview DataFrame"):
            st.dataframe(df.head(10))

        # Create LangChain Agent

        # --- Chat Interface ---
        st.markdown("### 💬 Ask your questions below:")

        if prompt:=st.chat_input("Let me help you with insights from the data?"):
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            result = agent_handler.process_user_input(messages)
            print(type(result))
            print(result)
            st.session_state.chat_history.append(("You", prompt))
            st.session_state.chat_history.append(("Bot", result))

        # Display chat history
        for sender, message in st.session_state.chat_history:
            if sender == "You":
                st.markdown(f"**🧑 You:** {message}")
            else:
                st.markdown(f"**🤖 Bot:** {message}")

    except Exception as e:
        st.error(f"Failed to read file: {e}")

# elif not openai_api_key:
#     st.warning("⚠️ Please enter your OpenAI API Key to continue.")

elif not uploaded_file:
    st.info("📤 Upload a CSV file to begin chatting!")

