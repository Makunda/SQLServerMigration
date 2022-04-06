from dataclasses import dataclass


@dataclass
class CallerCalleeWeightInput:
    """
    Configuration input of the weight to take in account for a specific caller and callee
    """

    src_type: str
    end_type: str
    value: float
    rel_name: str = None
    regex: str = None