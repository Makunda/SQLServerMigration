from dataclasses import dataclass
from typing import List

from neo4j.graph import Node

@dataclass
class ImagingTransaction:
    """
    Imaging transaction for API Communiction
    """
    name: str
    full_name: str
    object_number: int
    start_point: str
    end_points: List[str]
    cyclomatic_complexity: float
    integration_complexity: float
    essential_complexity: float

    node: Node = None

    def repr_json(self) -> dict:
        """
        Convert the node to a serializable document
        :return: The related dictionary
        """

        return dict(
            name=self.name,
            fullName=self.full_name,
            object_number=self.object_number,
            start_point=self.start_point,
            end_points=self.end_points,
            cyclomatic_complexity=self.cyclomatic_complexity,
            integration_complexity=self.integration_complexity,
            essential_complexity=self.essential_complexity
        )

    def get_node(self) -> Node:
        return self.node

    @staticmethod
    def get_headers() -> List:
        """
        Get the list of headers values
        :return: The headers
        """
        return [
            "Name",
            "Full Name",
            "Object Number",
            "Starting Type",
            "End Types",
            "Cyclomatic Complexity",
            "Integration Complexity",
            "Essential Complexity"
        ]

    def get_values(self) -> List:
        """
        Get the list of values
        :return:
        """
        return list(self.repr_json().values())