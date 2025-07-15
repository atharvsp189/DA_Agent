import streamlit as st
import pandas as pd
import os

# --- Streamlit UI ---

st.set_page_config(page_title="CSV Chat Assistant", layout="wide")
st.title("📊 CSV Chat Assistant")

# File Upload
uploaded_file = st.file_uploader("📁 Upload your CSV/Excel File", type=["csv", "xlsx"])

# Global chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Show DataFrame preview
        with st.expander("🔍 Preview DataFrame"):
            st.dataframe(df.head())

        # Create LangChain Agent

        # --- Chat Interface ---
        st.markdown("### 💬 Ask your questions below:")

        user_input = st.text_input("You:", key="input")

        if user_input:
            with st.spinner("Processing..."):
                print("Waiting..")
                # try:
                #     # response = agent.run(user_input)
                # except Exception as e:
                #     response = f"❌ Error: {str(e)}"

                # Update chat history
                # st.session_state.chat_history.append(("You", user_input))
                # st.session_state.chat_history.append(("Bot", response))

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

