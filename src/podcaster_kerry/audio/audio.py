from enum import Enum
from pathlib import Path
import wave
import re
from pydub import AudioSegment
from podcaster_kerry.audio.coqui import dialogue_to_mp3_coqui
from podcaster_kerry.audio.helpers import Entry
from podcaster_kerry.audio.piper import dialogue_to_mp3_piper

SEGMENTS_DIR = "segments"
WAVE_FILE = "combined.wav"

class Engine(Enum):
    PIPER = "piper"
    COQUI = "coqui"

def _dialogue_as_entries(content: str) -> list[Entry]:
    ret = []
    parsed = _dialogue_as_list(content)
    speaker_mapping: dict[str, int] = {}
    id_counter = 0

    for speaker, content in parsed:
        if speaker not in speaker_mapping:
            speaker_mapping[speaker] = id_counter
            id_counter += 1
        speaker_id = speaker_mapping[speaker]
        ret.append(Entry(speaker_id, content))
    return ret

def dialogue_to_mp3(content: str, working_dir: Path, output: Path, engine: Engine = Engine.COQUI):
    segments_dir = working_dir / SEGMENTS_DIR

    working_dir.mkdir(parents=True, exist_ok=True)
    segments_dir.mkdir(parents=True, exist_ok=True)

    results = _dialogue_as_entries(content)

    match engine:
        case Engine.COQUI:
            dialogue_to_mp3_coqui(results, segments_dir)
        case Engine.PIPER:
            dialogue_to_mp3_piper(results, segments_dir)
        case _:
            raise ValueError(f"Unsupported engine {engine}")     
    
    _combine_wav_files(segments_dir, working_dir / WAVE_FILE)
    _wav_to_mp3(working_dir / WAVE_FILE, output)

def _combine_wav_files(segments: Path, output: Path):
    infiles = list(segments.glob("*.wav"))
    infiles.sort()
    if not infiles:
        raise ValueError(f"No audio files found in {segments}")
    data = []
    for infile in infiles:
        with wave.open(str(infile), "rb") as w:
            data.append([w.getparams(), w.readframes(w.getnframes())])
    with wave.open(str(output), "wb") as w:
        w.setparams(data[0][0])
        for i in range(len(data)):
            w.writeframes(data[i][1])

def _wav_to_mp3(wave_file: Path, mp3_file: Path):
    AudioSegment.from_wav(str(wave_file)).export(str(mp3_file), format="mp3")

def _dialogue_as_list(content: str) -> list[tuple[str, str]]:
    """
    Inputs:
    content in the format
    H1: blah blah blah
    H2: blah blah blah
    ...
    
    Returns:
    ret[i] represents the i-th dialogue
    ret[i][0] is the speaker name
    ret[i][1] is the speaker content
    """
    content = content.strip() + "\n" # Ensure single newline at end
    pattern = r"(H\d):\s*(.*?)(?:\n(?=H\d:)|$)"
    matches = re.findall(pattern, content, re.MULTILINE)
    return [(speaker, dialogue.strip()) for speaker, dialogue in matches]
