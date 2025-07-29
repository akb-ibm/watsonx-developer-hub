from langchain.tools import tool
from langchain.tools import Tool
from langgraph.graph import END, StateGraph, MessagesState
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor

from lang_chain.langchain_watsonx import prepare_chat_watsonx


class AdversarialAgent:
    """
    A class to represent an adversarial agentic system.
    This class is a placeholder for future implementations.
    """

    def __init__(self, name: str):
        self.name = name
        print(f"Adversarial agent initialized with name: {self.name}")
        self.chat_watsonx = prepare_chat_watsonx()

    # Define the tools for the agent to use
    @tool
    def search(query: str):
        """Call to surf the web."""
        print ("Search tool triggered")

        # This is a placeholder, but don't tell the LLM that...
        if "sf" in query.lower() or "san francisco" in query.lower():
            return "It's 60 degrees and foggy."
        return "It's 90 degrees and sunny."
    
    def initialize_agent(self):       
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

        Question: {input}
        {agent_scratchpad}
        {tool_names}
        """

        prompt = PromptTemplate.from_template(prompt_template)
        agent = create_react_agent(llm=self.chat_watsonx, tools=tools, prompt=prompt)
        # Bind the agent to an executor
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


    def run(self, agent_input: str = "How is the weather in san francisco ?"):
        print(f"Running synthesizer agentic system: {self.name} with input {agent_input}")
        response = self.agent_executor.invoke({"input": {agent_input}})
        print("Agent Response:", response)
        return response