from dataclasses import dataclass


@dataclass
class LinkWeightInput:
    """
    Link weight structure for community propagation
    """
    rel_name: str
    value: float
    regex: str = None

    def has_regex(self):
        """

        :return:
        """
        return self.regex is not None

    def get_regex(self):
        return self.regex

    def get_weight(self):
        return self.value
