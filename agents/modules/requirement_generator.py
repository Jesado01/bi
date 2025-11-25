import json
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
from langgraph.graph import StateGraph
from agents.bian_core import CoreBianState
from agents.modules.agent_module import AgentModule

class RequirementGeneratorModule(AgentModule):
    """
    Module to generate requirements by analyzing endpoint implementations and OpenAPI specifications.
    """

    def __init__(self, file_reader, llm_client):
        self.file_reader = file_reader
        self.llm_client = llm_client
        self._module_name = "requirement_generator"
        self._dependencies = ["framework_detector"]
        self._llm_config = {
            "max_tokens": 64000,
            "temperature": 0.0
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
        graph.add_node(node_name, self.generate_requirements)
        return (node_name, node_name)

    def _load_json_file(self, file_path: str) -> Dict[str, Any]:
        """Load and parse a JSON file."""
        try:
            content = self.file_reader.read_file(file_path)
            return json.loads(content)
        except Exception as e:
            raise Exception(f"Failed to parse JSON file {file_path}: {str(e)}")

    def _read_endpoints_directory(self) -> str:
        """Read and merge all files from the endpoints directory."""
        endpoints_dir = Path("tmp/endpoints")
        if not endpoints_dir.exists() or not endpoints_dir.is_dir():
            raise FileNotFoundError(f"Endpoints directory not found at: {endpoints_dir}")

        merged_content = []
        for file_path in sorted(endpoints_dir.glob("*")):
            if file_path.is_file():
                try:
                    content = self.file_reader.read_file(str(file_path))
                    merged_content.append(f"\n{'='*80}\nFile: {file_path.name}\n{'='*80}\n{content}")
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {str(e)}")

        if not merged_content:
            raise FileNotFoundError(f"No files found in {endpoints_dir}")

        return "\n".join(merged_content)

    def _load_openapi_spec(self, state: CoreBianState) -> Dict[str, Any]:
        """Load the OpenAPI specification from the bian directory."""
        bian_dir = Path(state["bian_dir"])
        if not bian_dir.exists() or not bian_dir.is_dir():
            raise FileNotFoundError(f"BIAN directory not found at: {bian_dir}")

        json_files = list(bian_dir.glob("*.json"))
        if not json_files:
            raise FileNotFoundError(f"No JSON files found in {bian_dir}")

        # Assuming there's only one JSON file as per requirements
        return self._load_json_file(str(json_files[0]))

    def generate_requirements(self, state: CoreBianState) -> CoreBianState:
        """
        Generate requirements by analyzing endpoint implementations and OpenAPI spec.
        """
        print(f"[{self.module_name}] Generating requirements...")
        state["current_module"] = self.module_name

        try:
            # 1. Read and merge all endpoint files
            print(f"[{self.module_name}] Reading endpoint files...")
            endpoints_content = self._read_endpoints_directory()
            
            # 2. Load OpenAPI specification
            print(f"[{self.module_name}] Loading OpenAPI specification...")
            openapi_spec = self._load_openapi_spec(state)
            
            # 3. Get target language and framework from state
            target_language = state.get("target_language", "Java")
            target_framework = state.get("target_framework", "Spring Boot")

            # 4. Prepare the prompt for the LLM
            system_prompt = """
            You are an expert software architect. Your task is to analyze the provided endpoint implementations
            and OpenAPI specification to generate comprehensive requirements for the API endpoints.
            
            CRITICAL: You MUST preserve all endpoint names, request/response models, and error models exactly as defined in the OpenAPI specification.
            CRITICAL: request and response models must be included into domain layer.
            
            For each endpoint, include:
            1. Endpoint path and HTTP method
            2. Required headers and parameters
            3. Request/response models with all fields and their types
            4. Error responses and status codes
            5. Any business rules or validations
            
            Format the output in clear, well-structured markdown.
            """

            user_prompt = f"""
            I need to generate requirements for a {target_framework} application in {target_language}.
            
            Here are the endpoint implementations:
            {endpoints_content}
            
            And here is the OpenAPI specification that must be strictly followed:
            {json.dumps(openapi_spec, indent=2)}
            
            Please generate comprehensive requirements for this API, ensuring all endpoints, models, and error handling from the OpenAPI spec are preserved.
            """

            # 5. Call the LLM
            print(f"[{self.module_name}] Generating requirements with LLM...")
            requirements, _ = self.llm_client.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                **self._llm_config
            )

            # 6. Save the requirements to the state
            state["generated_requirements"] = requirements
            print(f"[{self.module_name}] Successfully generated requirements")

        except Exception as e:
            error_msg = f"{self.module_name}: Error generating requirements: {str(e)}"
            print(f"[ERROR] {error_msg}")
            state["errors"].append(error_msg)

        return state
