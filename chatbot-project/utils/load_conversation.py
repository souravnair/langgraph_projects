from langchain.messages import HumanMessage,AIMessage
def load_conversation(config,session_state, chat_workflow):
    get_state_history=chat_workflow.get_state(config)
    print("message_history", get_state_history)
    get_messsage_history=[]
    try:
        get_messsage_history=get_state_history.values["messages"]
    except:
        get_state_history.values["messages"]=[]

    role=""
    messages=[]
    print("message_history", get_messsage_history)
    if get_messsage_history:        
        for msg in get_messsage_history:            
            if isinstance(msg,HumanMessage):
                role="user"
            else:
                role="assistant"
            messages.append({"role":role, "content": msg.content})
    return messages        
