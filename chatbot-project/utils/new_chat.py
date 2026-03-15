from utils.generate_new_thread_id import generate_new_thread_id
def new_chat(session_state):
    thread_id=generate_new_thread_id()
    session_state["thread_id"]=thread_id
    add_session_thread(session_state["thread_id"], session_state)
    session_state["message_history"]=[]

def add_session_thread(thread_id,session_state):
    if thread_id not in session_state["chat_threads"]:
        session_state["chat_threads"].append(thread_id)

