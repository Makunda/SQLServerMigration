from dataclasses import dataclass
from typing import List

from api.websocket.interfaces.graph.elements.graph_edge import GraphEdge
from api.websocket.interfaces.graph.elements.graph_node import GraphNode


@dataclass
class GraphDataBatch:
    nodes: List[GraphNode]
    edges: List[GraphEdge]

    def repr_json(self) -> dict:
        """
        Serialize the Api response into in a dictionary
        :return:
        """
        return dict(
            nodes=[x.repr_json() for x in self.nodes],
            edges=[x.repr_json() for x in self.edges]
        )