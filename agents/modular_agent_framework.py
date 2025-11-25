"""
Modular LangGraph Migration Framework
Core framework that accepts pluggable subgraph modules for different migration tasks
"""

from langgraph.graph import StateGraph, END
from typing import Dict, List

# Core state that all subgraphs share
from agents.bian_core import CoreBianState
from agents.modules.agent_module import AgentModule


class ModularAgentFramework:
    """Core framework that orchestrates migration modules"""

    def __init__(self):
        self.modules: Dict[str, AgentModule] = {}
        self.execution_order: List[str] = []

    def register_module(self, module: AgentModule):
        """Register a migration module"""
        # Log module loading
        module.log_loading()

        self.modules[module.module_name] = module
        self._update_execution_order()

    def _update_execution_order(self):
        """Update execution order based on dependencies"""
        # Simple topological sort
        ordered = []
        remaining = set(self.modules.keys())

        while remaining:
            ready = []
            for module_name in remaining:
                module = self.modules[module_name]
                if all(dep in ordered for dep in module.dependencies):
                    ready.append(module_name)

            if not ready:
                raise ValueError("Circular dependency detected in modules")

            # Add ready modules to order
            for module_name in ready:
                ordered.append(module_name)
                remaining.remove(module_name)

        self.execution_order = ordered

    def create_main_graph(self) -> StateGraph:
        """Create a single, flat migration graph with all module nodes."""
        main_graph = StateGraph(CoreBianState)

        module_endpoints = {}

        # 1. Add all nodes from all modules to the main graph
        for module_name in self.execution_order:
            module = self.modules[module_name]
            entry_node, exit_node = module.add_nodes_to_graph(main_graph)
            module_endpoints[module_name] = {"entry": entry_node, "exit": exit_node}

        # 2. Chain the modules together using their entry/exit nodes
        if self.execution_order:
            # Set the main graph's entry point to the first module's entry node
            first_module_name = self.execution_order[0]
            main_graph.set_entry_point(module_endpoints[first_module_name]["entry"])

            # Add edges between modules
            for i in range(len(self.execution_order) - 1):
                current_module_name = self.execution_order[i]
                next_module_name = self.execution_order[i + 1]

                # Connect the exit node of the current module to the entry node of the next one
                exit_of_current = module_endpoints[current_module_name]["exit"]
                entry_of_next = module_endpoints[next_module_name]["entry"]
                main_graph.add_edge(exit_of_current, entry_of_next)

            # Connect the last module's exit node to the graph's END
            last_module_name = self.execution_order[-1]
            main_graph.add_edge(module_endpoints[last_module_name]["exit"], END)

        return main_graph.compile()

    def start_analysis(self, state: CoreBianState) -> Dict:
        """Run the complete migration with all registered modules"""
        print(f"Starting migration with modules: {self.execution_order}")

        main_graph = self.create_main_graph()

        final_state = main_graph.invoke(state, {"recursion_limit": 400})

        final_state["migration_complete"] = True
        return final_state

    def visualize_graph(self, xray: int = 1):
        """
        Visualize the migration graph using mermaid diagram

        Args:
            xray (int): Level of detail for the graph visualization (0-3)
                       0: Basic structure
                       1: Standard detail (default)
                       2: More detail
                       3: Maximum detail

        Returns:
            IPython.display.Image: The rendered graph image
        """
        try:
            from IPython.display import Image, display

            # Create the main graph
            main_graph = self.create_main_graph()

            # Generate and display the mermaid diagram
            graph_image = main_graph.get_graph(xray=xray).draw_mermaid_png()

            # Display the graph
            display(Image(graph_image))
            # return Image(graph_image)

        except ImportError as e:
            print("IPython not available. Install with: pip install ipython")
            return None
        except Exception as e:
            print(f"Error generating graph visualization: {e}")
            return None
