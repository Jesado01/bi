import os
from typing import List, Tuple
from pathlib import Path
from langgraph.graph import StateGraph
from agents.bian_core import CoreBianState
from agents.modules.agent_module import AgentModule

class FrameworkDetectorModule(AgentModule):
    """
    Module to detect the framework and programming language of API endpoint files.
    """

    def __init__(self, file_reader, llm_client):
        self.file_reader = file_reader
        self.llm_client = llm_client
        self._module_name = "framework_detector"
        self._dependencies = []
        self._llm_config = {
            "max_tokens": 5000,
        }

    @property
    def module_name(self) -> str:
        return self._module_name

    @property
    def dependencies(self) -> List[str]:
        return self._dependencies

    def add_nodes_to_graph(self, graph: StateGraph) -> Tuple[str, str]:
        """Adds this module's node to the main graph."""
        node_name = f"{self.module_name}_node"
        graph.add_node(node_name, self.detect_framework_and_language)
        return (node_name, node_name)

    def detect_framework_and_language(self, state: CoreBianState) -> CoreBianState:
        """
        Detects the framework and programming language of the first file in the endpoints directory.
        Updates the state with the detected information.
        """
        print(f"[{self.module_name}] Detecting framework and language...")
        state["current_module"] = self.module_name

        try:
            # Get the first file in the endpoints directory
            endpoints_dir = Path(state["endpoints_dir"])
            if not endpoints_dir.exists() or not endpoints_dir.is_dir():
                raise FileNotFoundError(f"Endpoints directory not found at: {endpoints_dir}")

            # Get the first .py or .js file in the directory
            endpoint_files = list(endpoints_dir.glob("*.md"))
            if not endpoint_files:
                raise FileNotFoundError(f"No supported endpoint files found in {endpoints_dir}")

            first_file = endpoint_files[0]
            print(f"[{self.module_name}] Analyzing file: {first_file}")

            # Read the file content
            file_content = self.file_reader.read_file(str(first_file))

            # Prepare the prompt for the LLM
            system_prompt = """
            You are an expert software engineer analyzing code to identify the programming language 
            and web framework used. Respond with ONLY the language and framework in this exact format:
            "Language: <language>\nFramework: <framework>"
            
            If the framework is not a known web framework, just put 'None'.
            Be concise and specific in your identification.
            """

            user_prompt = f"""Analyze this code and identify the programming language and web framework:
            
            {file_content}
            
            Format your response as:
            Language: <language>
            Framework: <framework or None>
            """

            # Call the LLM
            response, _ = self.llm_client.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                **self._llm_config
            )

            print(response)

            # Parse the response
            language = None
            framework = None
            
            for line in response.split('\n'):
                if line.lower().startswith('language:'):
                    language = line.split(':', 1)[1].strip()
                elif line.lower().startswith('framework:'):
                    framework = line.split(':', 1)[1].strip()
                    if framework.lower() == 'none':
                        framework = None

            # Update the state with the detected information
            if language:
                state["target_language"] = language.lower()
                print(f"[{self.module_name}] Detected language: {language}")
            if framework:
                state["target_framework"] = framework.lower()
                print(f"[{self.module_name}] Detected framework: {framework}")

        except Exception as e:
            error_msg = f"{self.module_name}: Error detecting framework and language: {str(e)}"
            print(f"[ERROR] {error_msg}")
            state["errors"].append(error_msg)

        return state
