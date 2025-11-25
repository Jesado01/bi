import os
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Union
from langgraph.graph import StateGraph
from agents.bian_core import CoreBianState
from agents.modules.agent_module import AgentModule

class ProjectStructureModule(AgentModule):
    """
    Module to update the project structure based on the detected language and framework.
    Uses architecture templates from tmp/architectures/{LANGUAGE}.txt
    """

    def __init__(self, file_reader, llm_client):
        self.file_reader = file_reader
        self.llm_client = llm_client
        self._module_name = "project_structure"
        self._dependencies = ["framework_detector", "requirement_generator"]
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
        graph.add_node(node_name, self.update_project_structure)
        return (node_name, node_name)

    def _load_architecture_template(self, language: str, architecture: str) -> Optional[str]:
        """Load the architecture template for the given language and architecture."""
        template_path = Path(f"tmp/architectures/{language.lower()}/{architecture.lower()}.txt")
        
        try:
            if template_path.exists():
                return self.file_reader.read_file(str(template_path))
        except Exception as e:
            print(f"[WARNING] Could not load template {template_path}: {e}")
                
        return None
        
    def _generate_structure_with_llm(self, language: str, architecture: str, requirements: str, template: str) -> str:
        """Use LLM to update the requirements with an appropriate project structure."""
        system_prompt = """
        You are an expert software architect. Your task is to update the project requirements document
        by replacing the "Proposed Project Structure" section with a new one based on the provided template.
        
        INSTRUCTIONS:
        1. Find the "## Proposed Project Structure" or "## Project Structure" section in the requirements
        2. Replace ONLY this section with the new structure
        3. Keep all other content exactly as is
        4. The new structure should be based on the provided template but adapted to the project
        5. Maintain consistent markdown formatting
        
        The template is just an example - adapt it intelligently to fit the project's requirements.
        """

        user_prompt = f"""
        Please update the project requirements document below by replacing the "Proposed Project Structure"
        section with a new one based on the template. The new structure should be tailored to this project.
        
        ========== EXISTING REQUIREMENTS ==========
        {requirements}
        
        ========== TEMPLATE STRUCTURE ==========
        {template}
        
        ========== INSTRUCTIONS ==========
        1. Find the "## Proposed Project Structure" section
        2. Replace ONLY this section with the new structure
        3. Keep all other content exactly as is
        4. The structure should follow the template but be adapted to this project
        5. Use proper markdown formatting with code blocks
        
        Return the complete updated requirements document with the replaced structure section.
        """

        try:
            # First, get the structure from the LLM
            structure_prompt = f"""
            Based on the following project requirements and template, generate a new "Proposed Project Structure" 
            section in markdown format. The structure should be based on the template but adapted to this project.
            
            Focus on creating a clean, well-organized structure that follows the template's organization 
            but is tailored to this project's needs.
            
            Requirements (first 4000 chars):
            {requirements[:4000]}
            
            Template Structure:
            {template}
            
            Return ONLY the updated "Proposed Project Structure" section, including the header and code block.
            """
            
            structure_response, _ = self.llm_client.generate(
                system_prompt=system_prompt,
                user_prompt=structure_prompt,
                **self._llm_config
            )
            
            # Extract just the structure part
            structure_md = structure_response.strip()
            
            # Now update the requirements document
            if "## Proposed Project Structure" in requirements:
                # Split the document at the section we want to replace
                parts = requirements.split("## Proposed Project Structure", 1)
                before_section = parts[0]
                after_section = parts[1].split("\n## ", 1)  # Split at next heading
                
                # If there's content after the section, keep it with proper heading
                after_content = after_section[1] if len(after_section) > 1 else ""
                if after_content:
                    after_content = "## " + after_content
                
                # Rebuild the document with the new structure
                updated_requirements = (
                    f"{before_section}## Proposed Project Structure\n\n"
                    f"{structure_md}\n\n"
                    f"{after_content}"
                )
            else:
                # If the section doesn't exist, add it before the first heading
                parts = requirements.split("##", 1)
                updated_requirements = (
                    f"{parts[0]}\n\n## Proposed Project Structure\n\n"
                    f"{structure_md}\n\n##{parts[1] if len(parts) > 1 else ''}"
                )
            
            return updated_requirements.strip()
            
        except Exception as e:
            print(f"[ERROR] Failed to generate project structure with LLM: {str(e)}")
            return template  # Fall back to the template if LLM fails

    def update_project_structure(self, state: CoreBianState) -> CoreBianState:
        """
        Update the generated requirements with a project structure adapted by LLM.
        """
        print(f"[{self.module_name}] Generating project structure...")
        state["current_module"] = self.module_name

        try:
            # Get the target language and architecture from state
            language = state.get("target_language", "").lower()
            architecture = state.get("target_architecture", "multimodule").lower()
            
            if not language:
                raise ValueError("Target language not detected")

            # Load the architecture template as a guideline
            template = self._load_architecture_template(language, architecture)
            if not template:
                print(f"[{self.module_name}] No architecture template found for {language}/{architecture}, no updating project structure")
                return state

            requirements = state.get('generated_requirements', '')
            updated_requirements = self._generate_structure_with_llm(
                language=language,
                architecture=architecture,
                requirements=requirements,
                template=template
            )
                
            state['updated_requirements'] = updated_requirements
            print(f"[{self.module_name}] Updated requirements with LLM-generated project structure")
                
        except Exception as e:
            error_msg = f"{self.module_name}: Error updating project structure: {str(e)}"
            print(f"[ERROR] {error_msg}")
            state["errors"].append(error_msg)
            
        return state
