from dataclasses import dataclass


@dataclass
class GraphListeningMode:
    """
        Graph Listening mode
    """
    mode: str
    name: str
    session: int

    def repr_json(self) -> dict:
        """
        Serialize the Api response into in a dictionary
        :return:
        """
        return dict(
            mode=self.mode,
            name=self.name,
            session=self.session
        )

    @staticmethod
    def convert_dict(data: dict):
        if "mode" not in data.keys():
            raise ValueError("Missing 'mode' key in Graph Listening Mode.")
        mode = data["mode"]

        if "name" not in data.keys():
            raise ValueError("Missing 'name' key in Graph Listening Mode.")
        name = data["name"]

        if "session" not in data.keys():
            raise ValueError("Missing 'session' key in Graph Listening Mode.")
        session = data["session"]

        return GraphListeningMode(mode, name, session)
