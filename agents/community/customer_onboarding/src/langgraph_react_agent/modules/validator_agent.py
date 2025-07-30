from typing import Literal

from langchain.tools import tool
from langchain.tools import Tool
from langgraph.graph import END, StateGraph, MessagesState
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor

from ibm_watsonx_ai import APIClient
from langchain_ibm import ChatWatsonx



class ValidatorAgent:
    """
    A class to represent a validator agentic system.
    This class is a placeholder for future implementations.
    """

    def __init__(self, name: str, client: APIClient, model_id: str):
        self.name = name
        print(f"Validator agent initialized with name: {self.name}")

        self.chat_watsonx = ChatWatsonx(
        model_id=model_id,
        watsonx_client=client,
        )


    # Define the tools for the agent to use
    @tool
    def trigger_security_breach_sop(query: str):
        """Trigger security protocols."""
        print ("Trigger security protocols")

        # This is a placeholder, but don't tell the LLM that...
        if "David" in query.lower():
            message = {
                "content": "Initiating SOP for security breach.",
                "role": "verify_identify",
                "response_metadata": {"finish_reason": "stop"}
            }
        else:
            message = {
                "content": "This was a false alarm, no security breach detected.",
                "role": "verify_identify",
                "response_metadata": {"finish_reason": "stop"}
            }
        return message

    def make_react_agent(self):       
        tools = [
            Tool.from_function(
                func=self.trigger_security_breach_sop,
                name="verify_identify",
                description="Verify whether the security breach SOP has to be triggered."
            )
        ]

        prompt_template = """You are a helpful assistant named validator_agent.

        You have access to the following tools:
        {tools}

        When you need to use a tool, use this format:

        Thought: Do I need to use a tool? Yes
        Action: <tool name>
        Action Input: <input>

        When you want to respond to the user, use this format:

        Thought: Do I need to use a tool? No
        Final Answer: <answer>

        Begin!

        Question: {messages}
        {agent_scratchpad}
        {tool_names}
        """

        prompt = PromptTemplate.from_template(prompt_template)
        try:
            agent = create_react_agent(llm=self.chat_watsonx, tools=tools, prompt=prompt)
        except Exception as e:
            print(f"Error creating agent: {e}")
            raise
        # Bind the agent to an executor
        try:
            self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        except Exception as e:
            print(f"Error creating agent executor: {e}")
            raise    
        return self.agent_executor

