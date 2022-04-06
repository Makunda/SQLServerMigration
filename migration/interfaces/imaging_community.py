from dataclasses import dataclass
from typing import List

from neo4j.graph import Node


@dataclass
class ImagingCommunity:
    """
        Interface for a community built on CAST Imaging
    """

    community_id: int
    community_type: str
    object_number: int

    # Technical Complexity
    cyclomatic_complexity: float
    essential_complexity: float
    integration_complexity: float

    # Functional Complexity
    transactions_number: int

    incoming_communities: List[str]
    outgoing_communities: List[str]

    def repr_json(self) -> dict:
        """
        Convert the node to a serializable document
        :return: The related dictionary
        """
        return dict(
            community_id=self.community_id,
            community_type=self.community_type,
            object_number=self.object_number,
            cyclomatic_complexity=self.cyclomatic_complexity,
            essential_complexity=self.essential_complexity,
            integration_complexity=self.integration_complexity,
            transactions_number=self.transactions_number,
            incoming_communities_number=len(self.incoming_communities),
            outgoing_communities_number=len(self.outgoing_communities),
            incoming_communities=self.incoming_communities,
            outgoing_communities=self.outgoing_communities
        )

    @staticmethod
    def get_headers():
        return [
            "Community Id",
            "Type",
            "Object Number",
            "Cyclomatic Complexity",
            "Essential Complexity",
            "Integration Complexity",
            "Transaction Number",
            "Incoming Communities Number",
            "Outgoing Communities Number",
            "Incoming Communities",
            "Outgoing Communities"
        ]

    def get_values(self) -> List:
        """
        Get the list of values
        :return:
        """
        return list(self.repr_json().values())