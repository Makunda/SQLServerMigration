from dataclasses import dataclass


@dataclass
class GraphEdge:
    source: int
    target: int

    def repr_json(self) -> dict:
        """
        Serialize the Graph Edge
        :return:
        """
        return dict(
            source=self.source,
            target=self.target
        )