import os

import streamlit
from click import prompt
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
import streamlit as st
from pandas.core.groupby.ops import extract_result
load_dotenv()
mykey=os.getenv("groq_api_key")

chat = ChatGroq(groq_api_key=mykey,model_name="llama-3.3-70b-versatile")

url_text=st.text_input("Enter a url")

prompt_text=st.text_input("Enter your massage")
submit_button=st.button("Submit")
if submit_button:
    doc = WebBaseLoader(url_text)
    extracted_Text=doc.load()
    textFromFromFirstWebsite=extracted_Text[0].page_content

    response= chat.invoke("solve the 0/1 knapsack problem using python")
    docs = WebBaseLoader(["https://docs.python.org/3/tutorial/datastructures.html","https://www.geeksforgeeks.org/python-data-structures/"])
    extractedText=docs.load()
    textFromFirstWebsite=extractedText[0].page_content
    extract_prompt=PromptTemplate.from_template("""
    ------------------
    The scrapped text is:
    {textFromFirstWebsite}
    -----------------
    Instruction:
    give a summary with two examples for the map data structure
    """)
    chain=extract_prompt | chat
    res=chain.invoke(input={'textFromFirstWebsite':textFromFirstWebsite,"prompt_text":prompt_text})

    st.title("chat with any website")
    #streamlit.text(res.content)
    st.markdown(res.content,unsafe_allow_html=True)