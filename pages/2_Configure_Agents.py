import streamlit as st
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Configure Agents",
    page_icon="🤖",
    layout="wide"
)

# Initialize agents in session state if not exists
if "agents" not in st.session_state:
    # Try to load agents from config file first
    if os.path.exists("agent_config.json"):
        with open("agent_config.json", "r") as f:
            st.session_state.agents = json.load(f)
    else:
        st.session_state.agents = [{
            "name": "Default Agent",
            "persona": "You are a helpful AI assistant focused on data analysis and insights. You communicate clearly and professionally while maintaining a friendly tone. You ask clarifying questions when needed and provide detailed explanations for your analysis. To answer questions use the following data: TEST. Whenever possible, show a data visualization with an explanation. Use the MATPLOTLIB library to create the visualizations. If you cannot answer the question with the dataset, say so, and provide only a short explanation, with no code.",
            "response-schema":{
                        'required': [
                            'code',
                            'explanation'
                        ],
                        'properties': {
                            'code': {'type': 'STRING'},
                            'explanation': {'type': 'STRING'}
                        },
                        'type': 'OBJECT',
                    },
            "active": True
        }]

st.title("Configure AI Agents 🤖")

# Add new agent button
if st.button("➕ Add New Agent"):
    st.session_state.agents.append({
        "name": f"Agent {len(st.session_state.agents) + 1}",
        "persona": "I am a helpful AI assistant.",
        "response-schema":{},
        "active": True
    })


# Display and configure each agent
for i, agent in enumerate(st.session_state.agents):
    with st.expander(f"🤖 {agent['name']}", expanded=(i == 0)):
        # Agent name
        new_name = st.text_input(
            "Agent Name",
            value=agent["name"],
            key=f"name_{i}"
        )
        st.session_state.agents[i]["name"] = new_name
        
        # Agent persona/prompt
        new_persona = st.text_area(
            "Agent Persona/Prompt",
            value=agent["persona"],
            height=150,
            key=f"persona_{i}",
            help="Define the personality and behavior of your agent"
        )
        st.session_state.agents[i]["persona"] = new_persona

        # Response schema
        try:
            # Get existing schema or use empty dict
            current_schema = agent.get("response-schema",{})
            print(current_schema)
            
            # Convert dict to formatted JSON string for editing
            schema_str = json.dumps(current_schema, indent=2) if current_schema else "{}"
            
            new_schema = st.text_area(
                "Response Schema (JSON)",
                value=schema_str,
                height=150,
                key=f"schema_{i}",
                help="Define the expected response format in JSON"
            )
            
            # Try to parse the JSON and update the agent
            try:
                parsed_schema = json.loads(new_schema)
                st.session_state.agents[i]["response-schema"] = parsed_schema
            except json.JSONDecodeError:
                st.error("Invalid JSON format in schema")
                
        except Exception as e:
            st.error(f"Error handling response schema: {str(e)}")
        
       # Use only in the multi-agent mode
       #active = st.toggle(
        #    "Active",
        #    value=agent["active"],
        #    key=f"active_{i}"
        #)
        #st.session_state.agents[i]["active"] = active
        
        # Delete agent button (prevent deleting last agent)
        if len(st.session_state.agents) > 1:
            if st.button("🗑️ Delete Agent", key=f"delete_{i}"):
                st.session_state.agents.pop(i)
                st.rerun()

# Save agents configuration
if st.button("💾 Save Configuration"):

    try:
        with open("agent_config.json", "w") as f:
            json.dump(st.session_state.agents, f, indent=2)
        st.success("Agent configuration saved successfully!")
    
    except Exception as e:
        st.error(f"Error saving configuration: {str(e)}")

# Load saved configuration
if os.path.exists("agent_config.json"):
    if st.button("📂 Load Saved Configuration"):
        try:
            config_file = st.text_input("Configuration file name", value="agent_config.json")
        
            with open(config_file, "r") as f:
                st.session_state.agents = json.load(f)
            st.success("Configuration loaded successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error loading configuration: {str(e)}")
