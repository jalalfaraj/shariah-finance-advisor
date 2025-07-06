# 🕌 Shariah Compliance Financial Advisor

This project is an early-stage AI-powered tool to help Muslims determine whether a 
specific stock is halal (permissible) to invest in, based on Islamic finance 
principles. The system uses modern AI technologies, document retrieval, and 
financial data to generate well-structured responses in line with Islamic 
guidelines.

---

## 📌 Purpose

To provide Muslims with a clear and accessible way to analyze the permissibility of 
financial investments—particularly stocks—based on interest income, debt ratio, and 
business sector, according to Shariah law.

---

## 🧠 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **[CrewAI](https://docs.crewai.com/)** | Framework for creating multi-agent 
collaborative AI systems |
| **Groq LLaMA3** | Online Groq large language model used to perform reasoning and 
generate human-like answers |
| **ChromaDB** | Vector database used to store and retrieve Islamic finance 
documents |
| **CrewAI Tools - RagTool** | For RAG (Retrieval-Augmented Generation) to pull 
relevant Shariah content from local PDFs |
| **Financial Modeling Prep API** | To fetch real-time financial data such as debt 
ratios and interest income |
| **Streamlit (optional frontend)** | To turn the CLI app into a user-friendly web 
interface in the future |
| **Python** | Core programming language used throughout the backend system |

---

## 🚀 How It Works

1. The user asks whether a stock (e.g., `RDDT`) is halal to invest in.
2. The system extracts key metrics:
   - **Sector**
   - **Interest income percentage**
   - **Debt-to-equity ratio**
3. The data is analyzed by two agents:
   - **Financial Data Interpreter** summarizes the financials
   - **Islamic Finance Researcher** compares them to Islamic texts using RAG
4. A final judgment is returned with both financial and Shariah perspectives.

---

## ✅ Features

- Multi-agent system (via CrewAI)
- RAG-powered reasoning from Islamic PDFs
- Real-time data from Financial Modeling Prep API
- Modular, extensible backend
- Clear output explaining both financial context and Islamic rulings

---

## Step 2: Obtain a Free FMP 🔐 API Key

This application uses Financial Modeling Prep (FMP) to retrieve financial data and provide Shariah compliance insights. You must provide your own API key.

📌 **How to Get an API Key:**

1. Register for a free account at: [https://site.financialmodelingprep.com](https://site.financialmodelingprep.com)
2. After signing up, copy your personal API key.

---

## Step 3: Get a FREE API key from Groq (this is to run requests on the LLM model in the app).
Setup on account and request a FREE API key to use.
https://console.groq.com/keys

Finally run this from the directory where the github repository was downloaded:

```bash
streamlit run app.py
```

Your app will open in a new browser tab.

✨ You're all set! Enjoy exploring Shariah-compliant investments.

---
## 🛤️ Future Work
Zakat Calculators: Automatically compute annual zakat due based on user input.

Expense Audits: Help Muslims check if their spending is halal.

Investment Portfolios: Suggest Shariah-compliant portfolios using AI filters.

Debt Management: Advise on avoiding riba (interest-based) loans and suggest 
alternatives.

Streamlit Web Interface: Fully functional front-end app for wider access and 
usability.

---
## 📚 Islamic Sources
You can add your own Shariah-compliant PDFs to the rag_tool.add() section in the 
script. Recommended texts include:

Mufti Taqi Usmani’s Islamic Finance publications

---
## 📫 Contact
Have ideas or want to contribute? Email: farajj7@gmail.com

