import streamlit as st
import requests

st.title("🌱 Empathetic AI Companion")
st.markdown("A safe space powered by RAG and Cognitive Behavioral Therapy frameworks.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How are you feeling today?"):
    # 1. Display user message immediately
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Call FastAPI backend
    try:
        # Grab all messages EXCEPT the one the user just typed
        history_to_send = st.session_state.messages[:-1]

        # Show a loading spinner while waiting for the API
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://127.0.0.1:8000/chat", 
                json={
                    "message": prompt,
                    "history": history_to_send 
                }
            )
            response.raise_for_status()
            
            bot_reply = response.json()["response"]
        
        # 3. Display bot response
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        
    except Exception as e:
        st.error(f"Error connecting to backend: Please make sure FastAPI is running. Details: {e}")