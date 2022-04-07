from dataclasses import dataclass

@dataclass
class Status:

    status: bool

    def repr_json(self) -> dict:
        """
        Serialize the status response into in a dictionary
        :return:
        """
        return dict(
            status=self.status
        )