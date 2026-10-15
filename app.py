import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
import requests




load_dotenv()



page_1 = st.Page("page_1.py")
page_2 = st.Page("page_2.py")
page_3 = st.Page("page_3.py")


pages = st.navigation([page_1, page_2, page_3])

pages.run()