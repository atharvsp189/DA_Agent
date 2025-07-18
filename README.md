# Data Analytics Agent 🤖📊

A powerful AI-powered data analytics agent that transforms your CSV and Excel files into interactive insights through natural language queries. Built with Streamlit, LlamaIndex, and popular visualization libraries.


Ask questions like:
> "What is the average sales by region?"  
> "Show me a bar plot of top 5 products by revenue."

...and get **instant answers** + **visualizations**!



## 🚀 Features

- 📁 Upload `.csv` or `.xlsx` files directly
- 🧠 Ask **natural language queries** and get intelligent responses
- 📊 Automatically generates **charts** using **Matplotlib** and **Seaborn**
- 🔍 Uses **LLM** + **LLamaIndex tools** to parse, query, and visualize data
- 💬 Built with **Streamlit** for an interactive chat interface


## 🧰 Tech Stack

- **Streamlit** – UI & chat interface  
- **Pandas** – Data handling  
- **Seaborn / Matplotlib** – Visualizations  
- **LlamaIndex** – Agent orchestration  
- **Gemini** – Language Model backend  


## 📦 Installation

### 🔧 Requirements

- Python 3.10+
- Recommended: Use virtualenv or conda

### ⚙️ Setup
---

1. Clone the Repository
```bash
git clone https://github.com/atharvsp189/DA_Agent.git
cd DA_Agent
```
2. Activate Virtual Enviourment
```
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```
3. Install Libraries
```
pip install -r requirements.txt
```
4. Add Enviourment Variable
```
<!-- Create .env File -->
.env -> GOOGLE_API_KEY = <API_KEY>
```
5. Run streamlit application
```
streamlit run streamlit_app.py
```

### 🎯 Usage
---
#### Basic Usage

- Launch the application
- Upload your data
- Click "Browse files" or drag and drop your CSV/Excel file
- Supported formats: .csv, .xlsx, .xls


#### Ask questions

Type your query in natural language

Examples:

- "What's the average sales by region?"
- "Show me a histogram of customer ages"
- "Which product category has the highest revenue?"

#### Get insights

- View automated analysis results
- Interactive visualizations
- Statistical summaries



## 👨‍💻 Author

**Atharv Patil**
- GitHub: [@atharvsp189](https://github.com/atharvsp189)
- LinkedIn: [@atharvsp189](https://linkedin.com/in/atharvsp189)

## 🙏 Acknowledgments

- [LlamaIndex](https://github.com/jerryjliu/llama_index) for the powerful indexing framework
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [OpenAI](https://openai.com/) for the language models
- All contributors and the open-source community


⭐ **Star this repository if you find it helpful!**