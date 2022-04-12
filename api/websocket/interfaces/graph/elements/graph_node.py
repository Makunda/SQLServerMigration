from dataclasses import dataclass


@dataclass
class GraphNode:
    id: int
    size: int
    label: str
    color: str

    def __init__(self, id: int, size: int, label: str, color: str):
        self.id = id
        self.size = size
        self.label = label
        self.color = color

    def repr_json(self) -> dict:
        """
        Serialize the Api response into in a dictionary
        :return:
        """
        return dict(
            id=self.id,
            size=self.size,
            label=self.label,
            color=self.color
        )