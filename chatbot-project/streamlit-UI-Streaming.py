import streamlit as st
from chatbot import chat_workflow 
from langchain_core.messages import HumanMessage
from utils.generate_new_thread_id import generate_new_thread_id
from utils.create_session import create_session
from utils.new_chat import *
from utils.load_conversation import *

#session state to store previous message history : st.session_state() : dict
# if "message_history" not in st.session_state:
#     st.session_state["message_history"]=[] #list of dictionaries

# if "thread_id" not in st.session_state:
#     st.session_state["thread_id"]=generate_new_thread_id()

# if "chat_threads" not in st.session_state:
#     st.session_state["chat_threads"]=[]
def get_config():
    return {"configurable":{"thread_id":st.session_state["thread_id"]}}

create_session(st.session_state)



#****************SIDEBAR-UI***************
st.sidebar.title("LANGRAPH CHATBOT")

if st.sidebar.button("New Chat"): #if "new chat" button is clicked
    new_chat(st.session_state)

st.sidebar.header("My Conversations")
for thread_id in st.session_state["chat_threads"][::-1]: #display the sessions in reverse, the new conversaton should stay in top
    if st.sidebar.button(str(thread_id)):#if sidebar button is clicked then load the conversation which is specific to that thread_id
        st.session_state["thread_id"]=thread_id
        config=get_config()        
        get_message_history=load_conversation(config,st.session_state, chat_workflow)
        st.session_state["message_history"]=get_message_history
        # for msg in get_message_history:
        #     with st.chat_message(msg["role"]):
        #         st.text(msg["content"])
#*****************************************

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input=st.chat_input("Enter your message here")



def get_response(user_input):
    config=get_config()
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