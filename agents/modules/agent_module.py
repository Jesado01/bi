from typing import List, Protocol, Tuple
from langgraph.graph import StateGraph

class AgentModule(Protocol):
    """Protocol that all migration modules must implement"""

    @property
    def module_name(self) -> str:
        """Unique name for this module"""
        ...

    @property
    def dependencies(self) -> List[str]:
        """List of module names this module depends on"""
        ...

    def add_nodes_to_graph(self, graph: StateGraph) -> Tuple[str, str]:
        """
        Adds this module's nodes and internal edges to the provided graph.

        Args:
            graph (StateGraph): The main graph to add nodes to.

        Returns:
            Tuple[str, str]: A tuple containing the (entry_node_name, exit_node_name) for this module.
        """
        ...

    def get_entry_point(self) -> str:
        """Get the entry point node name for this subgraph"""
        ...

    def get_exit_point(self) -> str:
        """Get the exit point node name for this subgraph"""
        ...

    def log_loading(self) -> None:
        """
        Log when this module is being loaded.
        This method provides a default implementation that should not be overridden.
        """
        print(f"[INFO] Loading module: {self.module_name}") # Print for immediate visibility

