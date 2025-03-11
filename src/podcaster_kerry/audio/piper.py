
from dataclasses import dataclass
from pathlib import Path
import subprocess
from podcaster_kerry.audio.helpers import Entry

# American english voices with > 1 speaker. https://github.com/rhasspy/piper/blob/9b1c6397698b1da11ad6cca2b318026b628328ec/src/python_run/piper/voices.json#L4
KEY_TO_NUM_SPEAKERS = {"en_US-libritts-high": 904, "en_US-arctic-medium": 18, "en_US-l2arctic-medium": 24}

# Default values from https://github.com/rhasspy/piper/blob/master/src/cpp/piper.hpp
@dataclass
class PiperParameters:
    length_scale: float = 1.0 # Phenome length (lower if faster)
    noise_scale: float = 0.667 # Generator noise
    noise_w: float = 0.8 # Phonme width noise
    sentence_silence: float = 0.0 # Seconds of silence after each sentence

    def as_args(self) -> list[str]:
        return [
            "--length-scale", str(self.length_scale),
            "--noise-scale", str(self.noise_scale),
            "--noise-w", str(self.noise_w),
            "--sentence-silence", str(self.sentence_silence),
        ]

def dialogue_to_mp3_piper(entries: list[Entry], segments_dir: Path):
    model = "en_US-arctic-medium"
    num_speakers = KEY_TO_NUM_SPEAKERS[model]

    for entry in entries:
        if entry.speaker_id > num_speakers:
            print(f"Speaker ID {entry.speaker_id} is out of range for model {model}, modifiying to {entry.speaker_id % num_speakers}")
            entry.speaker_id = entry.speaker_id % num_speakers
        parameters = PiperParameters(length_scale=0.85)
        command = ["piper",
                "--model", model,
                "--speaker", str(entry.speaker_id),
                "--output-dir", str(segments_dir),
                "--update-voices",
                *parameters.as_args(),
                ]
        _ = subprocess.check_output(command, input=entry.text.encode())
