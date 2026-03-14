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
    # response=chat_workflow.invoke(init_state, config=config)
    response=chat_workflow.stream(init_state, config=config, stream_mode="messages", version="v2")
    # Iterate through the stream and yield content chunks
    for chunk in response:
        ai_message_chunk, metadata = chunk
        if ai_message_chunk.content:  # Only yield non-empty content
            yield ai_message_chunk.content

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)
    
    # assistant_response= get_response(user_input)

    
    with st.chat_message("assistant"):        
        stream_response=get_response(user_input=user_input)
        assistant_response=st.write_stream(stream_response)
    st.session_state["message_history"].append({"role": "assistant", "content": assistant_response})