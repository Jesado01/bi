from agents.bian_core import CoreBianState
from agents.modular_agent_framework import ModularAgentFramework

# Assume these new modules are created in agents/modules/
from agents.modules.framework_detector import FrameworkDetectorModule
from agents.modules.requirement_generator import RequirementGeneratorModule
from agents.modules.project_structure import ProjectStructureModule

# You would also need your client and reader setups
from llm.anthropic_llm_client import AnthropicLLMClient
from internal.file_system_reader import FileSystemReader

def setup_agent_framework(state: CoreBianState, api_key: str) -> ModularAgentFramework:
    # Setup LLM client and file reader
    llm_client = AnthropicLLMClient(api_key=api_key)
    file_reader = FileSystemReader()
    # Create the framework instance
    framework = ModularAgentFramework()

    # --- Module Instantiation ---
    # Note: Pass clients/tools to modules that need them
    # Initialize modules
    framework_detector = FrameworkDetectorModule(file_reader=file_reader, llm_client=llm_client)
    requirement_generator = RequirementGeneratorModule(file_reader=file_reader, llm_client=llm_client)
    project_structure = ProjectStructureModule(file_reader=file_reader, llm_client=llm_client)

    # --- Module Registration ---
    # The framework's topological sort will handle the execution order
    # based on dependencies
    framework.register_module(framework_detector)
    framework.register_module(requirement_generator)
    framework.register_module(project_structure)

    return framework