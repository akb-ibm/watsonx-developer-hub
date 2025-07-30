from typing import Callable
from typing import Annotated, Literal, TypedDict

from ibm_watsonx_ai import APIClient
from langchain_ibm import ChatWatsonx
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode


from langgraph_react_agent import TOOLS
from langgraph_react_agent.modules.extractor_agent import ExtractorAgent
from langgraph_react_agent.modules.validator_agent import ValidatorAgent


def get_graph_closure(client: APIClient, model_id: str) -> Callable:
    """Graph generator closure."""

    # Define system prompt
    default_system_prompt = "You are a helpful AI Research assistant named Onboarding Buddy, please respond to the user's query to the best of your ability! Execute a tool call whenever you see fit."

    def get_graph(system_prompt=default_system_prompt) -> CompiledGraph:
        # Define the function that calls the model
        tool_node = ToolNode(TOOLS)
        

        #Define individual react agents
        collaborative_agents_list = ["validator_agent"]
        extractor_agent_obj = ExtractorAgent(name="react_agent_extractor", client=client, model_id=model_id)
        extractor_agent_obj_runner = extractor_agent_obj.make_react_agent()

        # #Define individual react agents
        collaborative_agents_list = ["extractor_agent"]
        validator_agent_obj = ValidatorAgent(name="react_agent_validator", client=client, model_id=model_id)
        validator_agent_obj_runner = validator_agent_obj.make_react_agent()

        # Define the function that determines whether to continue or not
        def should_continue(state: MessagesState) -> Literal[ "extractor_agent", "validator_agent", "tools", END]:
            messages = state['messages']
            last_message = messages[-1]
            # If the LLM makes a tool call, then we route to the "tools" node
            if last_message.tool_calls:
                return "tools"
            
            if "validator_agent" in last_message.content.lower():
                return "validator_agent"
                        
            # Otherwise, we stop (reply to the user)
            return END

        # Define agent inference functions
        def infer_extractor_agent_obj_runner(state: MessagesState):
            messages = state['messages']

            response = extractor_agent_obj_runner.invoke(state)           

            try:
                ai_message = AIMessage(
                content=response if isinstance(response, str) else response.get("output", ""),
                response_metadata={"source": "extractor_agent"},  # Optional: Add your own metadata
                )
            except Exception as e:
                print(f"Error creating AIMessage: {e}")
                ai_message = AIMessage(
                    content="An error occurred while processing your request. Please try again.",
                    response_metadata={"source": "extractor_agent"},
                )   

            messages.append(ai_message)
            state['messages'] = messages
            # print ("\n\nState after adding response:", state)
            return state

        def infer_validator_agent_obj_runner(state: MessagesState):
            messages = state['messages']

            response = validator_agent_obj_runner.invoke(state)           

            try:
                ai_message = AIMessage(
                content=response if isinstance(response, str) else response.get("output", ""),
                response_metadata={"source": "extractor_agent"},  # Optional: Add your own metadata
                )
            except Exception as e:
                print(f"Error creating AIMessage: {e}")
                ai_message = AIMessage(
                    content="An error occurred while processing your request. Please try again.",
                    response_metadata={"source": "extractor_agent"},
                )   

            messages.append(ai_message)
            state['messages'] = messages
            # print ("\n\nState after adding response:", state)
            return state


        # Define a new graph
        workflow = StateGraph(MessagesState)
        workflow.add_node("extractor_agent", infer_extractor_agent_obj_runner)
        workflow.add_node("validator_agent", infer_validator_agent_obj_runner)
        workflow.add_node("tools", tool_node)
        workflow.set_entry_point("extractor_agent")
        workflow.add_conditional_edges(
            "extractor_agent",
            should_continue,
        )
        workflow.add_edge("validator_agent", "extractor_agent")
        return workflow.compile()
    
    return get_graph