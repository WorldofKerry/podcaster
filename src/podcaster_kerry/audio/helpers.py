from dataclasses import dataclass


@dataclass
class Entry:
    speaker_id: int
    text: str
