import streamlit as st
from chatbot import chat_workflow 
from langchain_core.messages import HumanMessage

#session state to store previous message history : st.session_state() : dict
if "message_history" not in st.session_state:
    st.session_state["message_history"]=[] #list of dictionaries

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])


user_input=st.chat_input("Enter your message here")

def get_response(user_input):
    config={"configurable":{"thread_id":"1"}}
    init_state={"messages":[HumanMessage(content=user_input)]}
    response=chat_workflow.invoke(init_state, config=config)
    return response["messages"][-1].content

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)
    
    assistant_response= get_response(user_input)

    st.session_state["message_history"].append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.text(assistant_response)