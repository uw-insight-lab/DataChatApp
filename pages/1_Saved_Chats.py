import streamlit as st
import json
import os
from datetime import datetime

st.title("Saved Chats 💾")

# Initialize saved chats in session state if not exists
if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = {}

# Function to save current chat
def save_current_chat():
    if st.session_state.messages:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        chat_name = f"Chat_{timestamp}"
        
        # Save to session state
        st.session_state.saved_chats[chat_name] = {
            "messages": st.session_state.messages.copy(),
            "timestamp": timestamp,
            "title": chat_name
        }
        
        # Save to file
        save_chats_to_file()
        return chat_name
    return None

# Function to save chats to file
def save_chats_to_file():
    try:
        with open("saved_chats.json", "w") as f:
            json.dump(st.session_state.saved_chats, f, indent=2)
    except Exception as e:
        st.error(f"Error saving chats: {str(e)}")

# Function to load chats from file
def load_chats_from_file():
    try:
        if os.path.exists("saved_chats.json"):
            with open("saved_chats.json", "r") as f:
                st.session_state.saved_chats = json.load(f)
    except Exception as e:
        st.error(f"Error loading chats: {str(e)}")


# Load existing chats
load_chats_from_file()

# Display saved chats
if st.session_state.saved_chats and len(st.session_state.saved_chats) > 0:
    st.markdown("### Your Saved Chats")
    st.write(len(st.session_state.saved_chats))
    
    for chat_name, chat_data in st.session_state.saved_chats.items():
        with st.expander(f"📄 {chat_name}"):
            st.write(f"**Saved on:** {chat_data.get('timestamp', 'Unknown')}")
            st.write(f"**Messages:** {len(chat_data['messages'])}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Load {chat_name}", key=f"load_{chat_name}"):
                    st.session_state.messages = chat_data['messages'].copy()
                    st.success(f"Loaded {chat_name}!")
                    st.rerun()
            
            with col2:
                if st.button(f"Delete {chat_name}", key=f"delete_{chat_name}"):
                    del st.session_state.saved_chats[chat_name]
                    save_chats_to_file()
                    st.success(f"Deleted {chat_name}!")
                    st.rerun()
            
            # Show preview of messages
            st.markdown("**Preview:**")
            for i, msg in enumerate(chat_data['messages'][:3]):  # Show first 3 messages
                st.write(f"{msg['role']}: {msg['content'][:100]}...")
else:
    st.info("No saved chats yet. Start a conversation and save it!") 