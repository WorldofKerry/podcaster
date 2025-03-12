
from functools import cache
import os
from pathlib import Path
from typing import Iterator
from TTS.api import TTS
import torch
from podcaster_kerry.audio.helpers import Entry

FAV_XTTS_V2_SPEAKERS = [
    "Damien Black",
    # "Andrew Chipper", # Bad
    # "Craig Gusty", # Bad
    # Below are still figuring out if I like them
    "Luis Moray",
]

@cache
def _get_model():
    os.environ["COQUI_TOS_AGREED"] = "1"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def dialogue_to_mp3_coqui(entries: Iterator[Entry], paths: Iterator[Path]):
    model = _get_model()

    for entry, path in zip(entries, paths):
        speaker_id = entry.speaker_id % len(FAV_XTTS_V2_SPEAKERS)
        model.tts_to_file(
            text=entry.text,
            speaker=FAV_XTTS_V2_SPEAKERS[speaker_id],
            language="en",
            file_path=path,
        )

if __name__ == "__main__":
    model = _get_model()
    print(model.speakers)
