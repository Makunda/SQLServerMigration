from dataclasses import dataclass
from typing import List

from neo4j.graph import Node


@dataclass
class ImagingObject:
    """
    Imaging Object structure for API Communication
    """
    name: str
    full_name: str
    object_type: str
    internal_type: str
    level: str
    file_path: str
    line_of_code: int
    cyclomatic_complexity: float
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
            object_type=self.object_type,
            internal_type=self.internal_type,
            level=self.level,
            file_path=self.file_path,
            line_of_code=self.line_of_code,
            cyclomatic_complexity=self.cyclomatic_complexity,
            essential_complexity=self.essential_complexity,
        )

    def get_node(self) -> Node:
        return self.node

    @staticmethod
    def get_headers():
        """
        Get the headers
        :return:
        """
        return [
            "Name",
            "Full Name",
            "Object Type",
            "Internal Type",
            "Level",
            "File Path",
            "Line of code",
            "Cyclomatic Complexity",
            "Essential Complexity",
        ]

    def get_values(self) -> List:
        """
        Get the values
        :return:
        """
        return list(self.repr_json().values())
