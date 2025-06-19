import streamlit as st
from google import genai
from google.genai import types
from typing import Optional
import random
import json
import os
from datetime import datetime
from utils.load_env import load_api_key_from_env

_ENV_FILE_ = os.path.join(os.path.dirname(__file__),"variables.env")
#### ----- SET-UP AND PRE-AMBLE ----- ####

# Initialize session state for API key and messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

# Initialize saved chats in session state if not exists
if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = {}

# Initialize agents in session state if not exists
if "agents" not in st.session_state:
    st.session_state.agents = []

if "last_config_modified" not in st.session_state:
    st.session_state.last_config_modified = 0

# Try to load API key from env file
env_api_key = load_api_key_from_env(_ENV_FILE_)
if env_api_key:
    # Only run this block for Gemini Developer API
    st.session_state.gemini_api_key = env_api_key
    client = genai.Client(api_key=env_api_key)
   

models = ["models/gemini-1.5-pro-latest",
          "models/gemini-1.5-flash",
          "models/gemini-2.0-flash",
          "models/gemini-2.0-pro-exp",
          "models/gemini-2.5-flash",
          "models/gemini-2.0-pro-exp"
          ]


#### ----- START OF STREAMLIT APPLICATION ----- ####
# Page configuration
st.set_page_config(
    page_title="Data Chat App",
    page_icon="📊",
    layout="wide"
)

# Sidebar for API key configuration
with st.sidebar:
    st.header("Configuration 🔧")
    #Add this for a dynamic key, otherwise comment out
    #api_key = st.text_input(
    #    "Enter your Gemini API Key",
    #    type="password",
    #    help="Get your API key from https://aistudio.google.com/apikey"
    #)
    
    #if api_key:
    #    st.session_state.gemini_api_key = api_key
    #    st.success("API key configured!")

    # Model selection
    if st.session_state.gemini_api_key:
        try:
            #To see all models, uncomment the line below
            #models = [m.name for m in genai.list_models()]
            selected_model = st.selectbox(
                "Select Gemini Model",
                models,
                help="Choose which Gemini model to use"
            )
            st.success(f"Using model: {selected_model}")
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
    else:
        st.warning("Please enter your API key to use the full features.")
    
    
    ## ------ SIDEBAR CHAT OPTIONS ----- ##
    st.header("Chat Options ")
    
    # Agent configuration status and refresh
    st.subheader("🤖 Agent Configuration")
    if st.button("🔄 Refresh Agents"):
        try:
            if os.path.exists("agent_config.json"):
                with open("agent_config.json", "r") as f:
                    st.session_state.agents = json.load(f)
                st.session_state.last_config_modified = os.path.getmtime("agent_config.json")
                st.success("Agents refreshed!")
                st.rerun()
            else:
                st.warning("No agent configuration file found")
        except Exception as e:
            st.error(f"Error refreshing agents: {str(e)}")
    
    #st.caption(f"Active agents: {len(st.session_state.agents)}")
    
    if st.button("💾 Save Chat"):
        if st.session_state.messages:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            chat_name = f"Chat_{timestamp}"
            
            st.session_state.saved_chats[chat_name] = {
                "messages": st.session_state.messages.copy(),
                "timestamp": timestamp,
                "title": chat_name
            }
            
            # Save to file
            try:
                with open("saved_chats.json", "w") as f:
                    json.dump(st.session_state.saved_chats, f, indent=2)
                st.success(f"Chat saved as '{chat_name}'!")
            except Exception as e:
                st.error(f"Error saving chat: {str(e)}")
        else:
            st.warning("No messages to save!")


    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.rerun()


    if st.button("📋 View Saved Chats"):
        st.switch_page("pages/1_Saved_Chats.py")

# Main chat interface
st.header("Data Chat Assistant 💬")

# Check if agent config file has been modified
config_file_path = "agent_config.json"
current_modified_time = 0
if os.path.exists(config_file_path):
    current_modified_time = os.path.getmtime(config_file_path)

# Reload agents if config file has been modified
if current_modified_time > st.session_state.last_config_modified:
    try:
        with open(config_file_path, "r") as f:
            st.session_state.agents = json.load(f)
        st.session_state.last_config_modified = current_modified_time
        st.rerun()  # Refresh the page to show updated agents
    except Exception as e:
        st.error(f"Error loading agent configuration: {str(e)}")

# Initialize default agent if no agents exist
if not st.session_state.agents:
    st.session_state.agents = [{
        "name": "Default Agent",
        "persona": """You are a helpful AI assistant focused on data analysis and insights. You communicate clearly and professionally while maintaining a friendly tone. You ask clarifying questions when needed and provide detailed explanations for your analysis.""",
        "active": True
    }]

# Let user select agent
agent_names = [agent["name"] for agent in st.session_state.agents]
selected_agent = st.selectbox(
    "Select AI Agent",
    agent_names,
    help="Choose which AI persona to chat with"
)

# Get selected agent's persona
selected_persona = next(
    agent["persona"] 
    for agent in st.session_state.agents 
    if agent["name"] == selected_agent
)

# Add system prompt if messages empty or if agent changed
if not st.session_state.messages or (st.session_state.messages and st.session_state.messages[0].get("content") != selected_persona):
    st.session_state.messages = [
        {"role": "system", "content": selected_persona}
    ]



# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your data..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    if not st.session_state.gemini_api_key:
        #If no API key, random gibberish response for testing purposes
        messages = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(50, 200)))
        
        with st.chat_message("assistant"):
            st.markdown(messages)
            st.session_state.messages.append({"role": "assistant", "content": messages})
    else:
        try:
            #initiate the chat
  
            chat = client.chats.create(
                model=selected_model,
                config=types.GenerateContentConfig(
                    system_instruction=selected_persona
                )
            )
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat.send_message(prompt)
                    st.markdown(response.text)
                    
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
