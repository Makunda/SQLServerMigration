from dataclasses import dataclass


@dataclass
class GraphCharacteristics:
    """

    """
    name: str
    session: str
    batch_size: int
    graph_size: int

    def repr_json(self) -> dict:
        """
        Serialize the Api response into in a dictionary
        :return:
        """
        return dict(
            name=self.name,
            session=self.session,
            batch_size=self.batch_size,
            graph_size=self.graph_size
        )
