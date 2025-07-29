import os
from lang_chain.langchain_watsonx import prepare_chat_watsonx
from synthesizer_agent import SythesizerAgent
from adversarial_agent import AdversarialAgent

    

class AdversarialAgenticSystem:
    """
    A class to represent an adversarial agentic system.
    This class is a placeholder for future implementations.
    """

    def __init__(self, name: str):
        self.name = name
        print(f"AdversarialAgenticSystem initialized with name: {self.name}")

    def initialize_system(self):
        self.synthesizer_agent = SythesizerAgent(name=self.name+"_synthesizer")
        self.synth_agent_subgraph = self.synthesizer_agent.compile_graph()
        self.adversarial_agent = AdversarialAgent(name=self.name+"_adversarial")
        self.adversarial_agent.initialize_agent()
        print("Adversarial agent and synthesizer agent initialized.")


    def run(self):
        print(f"Running adversarial agentic system: {self.name}")
        print ("Sythesizer response: ", self.synthesizer_agent.run(agent_input = "How is the weather in san francisco ?"))
        print ("Adversarial response: ", self.adversarial_agent.run(agent_input = "How is the weather in san francisco ?"))
        return "System ran successfully"  
    

if __name__ == "__main__":
    # Initialize the adversarial agentic system   
    adversarial_system = AdversarialAgenticSystem(name="adversarial_system")
    adversarial_system.initialize_system()
    adversarial_system.run()
    print("Adversarial agentic system finished.")