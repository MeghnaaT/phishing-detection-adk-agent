import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

# --- Setup Logging and Environment ---

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL") or "gemini-1.5-flash"

# --- Save user prompt ---

def add_prompt_to_state(
    tool_context: ToolContext, prompt: str
) -> dict[str, str]:
    """Saves the user's initial prompt to the state."""
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[State updated] Added to PROMPT: {prompt}")
    return {"status": "success"}


# --- External Knowledge Tool (kept same) ---

wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# --- 1. Cybersecurity Analyzer Agent ---

comprehensive_researcher = Agent(
    name="cybersecurity_analyzer",
    model=model_name,
    description="Analyzes user input for potential cybersecurity threats.",
    instruction="""
You are a cybersecurity analysis assistant.

Your task is to analyze the user's PROMPT and classify it into ONE of the following:

- Phishing → malicious links, password requests, urgency, scams
- Suspicious → unusual or unclear intent but not clearly malicious
- Safe → normal harmless communication

You may use available tools if needed.

Return output strictly in this format:

Classification: <Safe / Suspicious / Phishing>
Reason: <short explanation>

PROMPT:
{ PROMPT }
""",
    tools=[wikipedia_tool],
    output_key="research_data"
)

# --- 2. Response Formatter Agent ---

response_formatter = Agent(
    name="security_response_formatter",
    model=model_name,
    description="Formats cybersecurity analysis into a user-friendly response.",
    instruction="""
You are a cybersecurity assistant explaining results to the user.

Using the RESEARCH_DATA:

- Clearly state whether the message is Safe, Suspicious, or Phishing
- Explain WHY in simple terms
- Give a short safety recommendation

Format your response exactly like this:

🔍 Classification: <result>  
📌 Reason: <reason>  
🛡️ Advice: <what user should do>

RESEARCH_DATA:
{ research_data }
"""
)

# --- Workflow (same structure, renamed purpose) ---

tour_guide_workflow = SequentialAgent(
    name="cybersecurity_analysis_workflow",
    description="Analyzes user input for cybersecurity threats.",
    sub_agents=[
        comprehensive_researcher,
        response_formatter,
    ]
)

# --- Root Agent (entry point) ---

root_agent = Agent(
    name="cybersecurity_entry_agent",
    model=model_name,
    description="Main entry point for cybersecurity message analysis.",
    instruction="""
- Greet the user and tell them you will help detect scams, phishing, or suspicious messages.
- Ask the user to provide any message, email, or text they want to analyze.
- When the user responds, store it using the 'add_prompt_to_state' tool.
- After storing, transfer control to the cybersecurity analysis workflow.
""",
    tools=[add_prompt_to_state],
    sub_agents=[tour_guide_workflow]
)