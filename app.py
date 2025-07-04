#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 14:29:59 2025

@author: user
"""

# app.py
import streamlit as st
import requests
from crewai import Agent, Task, Crew, LLM
from chromadb import PersistentClient
from chromadb.utils import embedding_functions

# === LLM Setup ===
langchain_llm = LLM(
    base_url="http://localhost:11434",
    model="ollama/llama3.2:1b",
    temperature=0.3,
    max_tokens=2000
)

# === Chroma Connection ===
client = PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="shariah_texts", embedding_function=embedding_fn)

def retrieve_passages(query, k=3):
    results = collection.query(query_texts=[query], n_results=k)
    return results['documents'][0]

def fetch_fmp_data(ticker, api_key):
    try:
        profile_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={api_key}"
        income_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=1&apikey={api_key}"
        ratios_url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={api_key}"

        profile = requests.get(profile_url).json()
        income = requests.get(income_url).json()
        ratios = requests.get(ratios_url).json()

        if not profile or not income or not ratios:
            return {"error": "Missing data."}

        sector = profile[0].get("sector", "N/A")
        interest_income = float(income[0].get("interestIncome", 0))
        total_revenue = float(income[0].get("revenue", 1))
        interest_pct = round((interest_income / total_revenue) * 100, 2)
        debt_ratio = ratios[0].get("debtEquityRatioTTM", "N/A")

        return {
            "sector": sector,
            "interest_pct": interest_pct,
            "debt_ratio": debt_ratio
        }
    except Exception as e:
        return {"error": str(e)}

def build_stock_summary_crew(financial_data):
    summary = (
        f"Sector: {financial_data.get('sector', 'N/A')}. "
        f"Interest income represents {financial_data.get('interest_pct', 0)}% of revenue. "
        f"Debt-to-equity ratio is {financial_data.get('debt_ratio', 'N/A')}."
    )
    
    # Get Islamic context
    Islamic_context = str(retrieve_passages(summary))
    print("📖 Islamic Context Retrieved:")
    print(Islamic_context)
    print("-" * 50)
   
    # Agent 1: Stock Info Gatherer
    stock_info_agent = Agent(
        role="Financial Data Interpreter",
        goal="Convert raw financial metrics into clear, factual descriptions",
        backstory="""You are a financial data analyst who interprets financial 
        metrics factually. You explain what numbers mean without giving investment 
        advice. You always provide analysis when given financial data.""",
        verbose=False,
        llm=langchain_llm
    )
    
    # Agent 2: Islamic Finance Researcher  
    islamic_finance_researcher = Agent(
        role="Islamic Finance Researcher",
        goal="Find relevant Islamic finance information related to stock summaries",
        backstory="""You are an Islamic Financial expert. When given a stock summary, 
        you search Islamic finance texts for relevant information about the company's 
        compliance with Islamic principles. You focus on interest rates, debt levels, 
        business sectors, and Sharia compliance. You present factual findings without 
        giving advice.""",
        verbose=False,
        llm=langchain_llm
    )
    
    # Task 1: Financial Summary
    financial_summary_task = Task(
        description=f"""
        TASK: Interpret the following financial metrics and write a summary paragraph.
        
        FINANCIAL METRICS:
        {financial_data}
        
        REQUIREMENTS:
        1. Explain what a debt-to-equity ratio of this level typically indicates
        2. Explain what the interest income percentage reveals about revenue sources  
        3. Describe the overall financial structure these metrics suggest
        4. Use factual, descriptive language
        5. Do not refuse - this is standard financial data interpretation
        
        Write as: "This company's financial metrics show..."
        """,
        expected_output="A factual paragraph interpreting the financial metrics",
        agent=stock_info_agent
    )

    # Task 2: Islamic Finance Analysis - FIXED VERSION
    islamic_analysis_task = Task(
        description=f"""
        You will receive a financial summary from the previous task. Use this summary 
        along with the Islamic finance context provided below to create your analysis.
        
        ISLAMIC FINANCE CONTEXT FROM SHARIAH TEXTS:
        {Islamic_context}
        
        INSTRUCTIONS:
        1. Review the financial summary from the previous task
        2. Use the Islamic finance context above to analyze:
           - The company's business sector and its Islamic permissibility
           - Islamic perspectives on the debt levels mentioned
           - Islamic views on interest income (if any)
           - General Sharia compliance considerations
        
        3. Write a paragraph presenting your findings based on the Islamic texts provided
        4. Focus on factual Islamic finance principles, not investment advice
        
        Format your response as: "Based on Islamic finance principles, this company..."
        """,
        expected_output="A paragraph presenting Islamic finance findings related to the stock",
        agent=islamic_finance_researcher,
        context=[financial_summary_task]  # This task depends on the first task
    )
    
    # Create crew
    crew = Crew(
        agents=[stock_info_agent, islamic_finance_researcher],
        tasks=[financial_summary_task, islamic_analysis_task],
        verbose=False
    )
    return crew

# === Streamlit UI ===
st.title("📊 Shariah Stock Screener")
api_key = st.text_input("🔑 Enter your FinancialModelingPrep API Key", type="password")
ticker = st.text_input("🏢 Enter a stock ticker (e.g., TSLA, RDDT)")

if st.button("Analyze"):
    if not api_key or not ticker:
        st.warning("Please enter both your API key and a valid stock ticker.")
    else:
        with st.spinner("🔎 Fetching data and analyzing..."):
            data = fetch_fmp_data(ticker.upper(), api_key)
            if "error" in data:
                st.error(f"❌ Error: {data['error']}")
            else:
                st.write("## 🔍 Financial Summary")
                st.write(data)

                crew = build_stock_summary_crew(data)
                result = crew.kickoff()

                st.write("## 📜 Islamic Finance Assessment")
                st.success(result)
