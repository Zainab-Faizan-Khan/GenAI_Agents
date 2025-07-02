# 🤖 AI-Powered CRM Automation with LangGraph + HubSpot

This project showcases how an AI-powered multi-agent system can automate real-world CRM workflows using natural language. It's designed to demonstrate how LLMs, tools, and automation can work together to perform complex tasks like managing HubSpot contacts and deals — with minimal human input.

It’s built using **LangGraph**, **LangChain**, and **FastAPI**, and integrates with **HubSpot** and email services to provide seamless, autonomous workflow execution.

---

## 🚀 What It Can Do

- 🧠 **Understands natural language** using OpenAI’s GPT-3.5-turbo to interpret user queries
- 🛠️ **Performs CRM actions automatically**, including:
  - Creating a HubSpot contact
  - Updating an existing contact
  - Creating a HubSpot deal
  - Updating a deal’s properties
- ✉️ **Sends email notifications** after every operation to confirm the action
- 🧩 **Built with LangGraph**, enabling modular, state-aware, multi-step execution
- ⚡ **FastAPI-based API** so you can plug it into any frontend or automation system




---

## ▶️ How to Run This Project

Follow these steps to get the project running on your machine:

### 1. Clone the Repository


git clone https://github.com/your-username/genai-crm-automation.git
cd genai-crm-automation


### 2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Add API Configuration
{
  "openai_api_key": "your-openai-key",
  "hubspot_api_key": "your-hubspot-token",
  "email_sender": "your-email@example.com",
  "email_password": "your-email-app-password"
}

### 5. Start the FastAPI Server
uvicorn api.main:app --reload
The server will run at:
📍 http://localhost:8000
