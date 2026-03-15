from utils.generate_new_thread_id import generate_new_thread_id
from utils.new_chat import add_session_thread
def create_session(session_state):
    if "message_history" not in session_state:
        session_state["message_history"]=[] #list of dictionaries

    if "thread_id" not in session_state:
        session_state["thread_id"]=generate_new_thread_id()

    if "chat_threads" not in session_state:
        session_state["chat_threads"]=[]
    
    add_session_thread(session_state["thread_id"], session_state)


