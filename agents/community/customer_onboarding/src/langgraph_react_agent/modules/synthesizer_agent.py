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



class SythesizerAgent:
    """
    A class to represent a synthesizer agentic system.
    This class is a placeholder for future implementations.
    """

    def __init__(self, name: str, client: APIClient, model_id: str):
        self.name = name
        print(f"Synthesizer agent initialized with name: {self.name}")

        self.chat_watsonx = ChatWatsonx(
        model_id=model_id,
        watsonx_client=client,
        )


    # Define the tools for the agent to use
    @tool
    def search(query: str):
        """Call to surf the web."""
        print ("Search tool triggered")

        # This is a placeholder, but don't tell the LLM that...
        if "sf" in query.lower() or "san francisco" in query.lower():
            message = {
                "content": "It's 60 degrees and sunny.",
                "role": "tool",
                "response_metadata": {"finish_reason": "stop"}
            }
        else:
            message = {
                "content": "It's 90 degrees and sunny.",
                "role": "tool",
                "response_metadata": {"finish_reason": "stop"}
            }
        return message

    def make_react_agent(self):       
        tools = [
            Tool.from_function(
                func=self.search,
                name="search",
                description="Search the web for information, like weather or locations."
            )
        ]

        prompt_template = """You are a helpful assistant.

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

    def run(self, agent_input: str = "How are you"):
        print(f"Running synthesizer agentic system: {self.name} with input {agent_input}")
        response = self.agent_executor.invoke({"input": {agent_input}})
        print("Agent Response:", response)
        return response

    def invoke_model_stateful(self, state: MessagesState):
        messages = state['messages']
        # if (messages is None or len(messages) == 0):
        response = self.agent_executor.invoke(messages)
        return {"messages": [response]}
        # else:
        #     return {"messages": "Please provide a valid input message."}
        
    # def should_continue(self, state: MessagesState) -> Literal["tools", "agent_v2", END]:
    #     messages = state['messages']
    #     last_message = messages[-1]

    #     # Use a specific trigger to decide
    #     if "use secondary agent" in last_message.content.lower():
    #         return "agent_v2"

    #     if last_message.tool_calls:
    #         return "tools"

    #     return END
