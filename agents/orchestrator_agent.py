from dotenv import load_dotenv
import os
import sys
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from config_loader import config


# Get the API key securely
OPENAI_API_KEY = config["openai_api_key"]
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

# Create LLM instance 
try:
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=OPENAI_API_KEY
    )
except Exception as e:
    print(f"❌ Error initializing LLM: {e}")
    sys.exit(1)

# Function to get orchestrator 
def get_orchestrator(tools):
    try:
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        return agent
    except Exception as e:
        print(f"❌ Error initializing LangChain agent: {e}")
        return None  # Or raise e if you want to crash the program
