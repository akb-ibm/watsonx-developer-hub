from typing import Callable

from ibm_watsonx_ai import APIClient
from langchain_ibm import ChatWatsonx
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

from langgraph_react_agent import TOOLS

from langgraph_react_agent.modules.synthesizer_agent import SythesizerAgent


from langgraph.graph import END, StateGraph, MessagesState
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

def get_graph_closure(client: APIClient, model_id: str) -> Callable:
    """Graph generator closure."""

    # Define system prompt
    default_system_prompt = "You are a helpful AI Research assistant named Onboarding Buddy, please respond to the user's query to the best of your ability! Execute a tool call whenever you see fit."

    def get_graph(system_prompt=default_system_prompt) -> CompiledGraph:
        # Define the function that calls the model
        tool_node = ToolNode(TOOLS)


        #Define individual react agents
        synthesizer_agent = SythesizerAgent(name="react_agent_synthesizer", client=client, model_id=model_id)
        synth_agent_react = synthesizer_agent.make_react_agent()

        # Define the function that calls the react agent
        def call_model(state: MessagesState):
            messages = state['messages']
            # response = synthesizer_agent.invoke_model_stateful(state)
            # response = synthesizer_agent.chat_watsonx.invoke(messages)
            response = synth_agent_react.invoke(state)
            # We return a list, because this will get added to the existing list
            # return {"messages": [response]}
            return state


        # Define a new graph
        workflow = StateGraph(MessagesState)
        # Define the two nodes we will cycle between
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        workflow.set_entry_point("agent")
        # We now add a conditional edge

        # We now add a normal edge from `tools` to `agent`.
        # This means that after `tools` is called, `agent` node is called next.
        workflow.add_edge("tools", 'agent')
        return workflow.compile()
    
    return get_graph