import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_travily import TavilySearch

load_dotenv()

model = init_chat_model("gpt-5.4-mini")

@tool
def get_weather(location : str) -> str :
    "특정 지역의 날씨 정보 조회 도구"
    return f"{location}의 날씨는 -5도에 미세먼지는 매우 나쁨"

tavily_tool = TavilySearch(
    
)

agent = create_agent(model, tools = [get_weather, tavily_tool])

st.title("1 페이지 입니다.")

if "messages" not in st.session_state :
    st.session_state.messages = []

prompt = st.chat_input("무엇이든 물어보세요.")

if prompt:
    # response = model.invoke(prompt)
    response = agent.invoke(
        {"messages" : [{"role" : "user", "content" : prompt}]}
    )
    st.session_state.messages.append({"role" : "user", "content" : prompt})
    st.session_state.messages.append({"role" : "ai", "content" : response['messages'][-1].content})

for message in st.session_state.messages : 
    with st.chat_message(message["role"]) : 
        st.write(message["content"])
    