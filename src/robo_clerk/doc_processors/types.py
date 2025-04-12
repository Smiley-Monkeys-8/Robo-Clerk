from dataclasses import dataclass

@dataclass
class Feature:
    key: str
    value: str
    coordinates: dict
