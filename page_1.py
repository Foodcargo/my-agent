import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
import requests
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

load_dotenv()

model = init_chat_model("gpt-5.4-mini")

@tool
def get_weather(location : str) -> str :
    "특정 지역의 날씨 정보 조회 도구"
    return f"{location}의 날씨는 -5도에 미세먼지는 매우 나쁨"

@tool
def get_exchange_rate(base: str = "USD", quote: str = "KRW", amount: float = 1.0) -> str:
    """
    특정 통화의 환율을 조회합니다.
    예: base='USD', quote='KRW'이면 1달러가 몇 원인지 조회합니다.
    amount를 넣으면 해당 금액을 환산합니다.
    """

    base = base.upper()
    quote = quote.upper()

    url = f"https://api.frankfurter.dev/v2/rate/{base}/{quote}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    rate = data["rate"]
    date = data.get("date", "알 수 없음")

    converted = amount * rate

    return (
        f"기준일: {date}\n"
        f"환율: 1 {base} = {rate:,.2f} {quote}\n"
        f"환산: {amount:,.2f} {base} = {converted:,.2f} {quote}"
    )


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
    