import shutil
from pathlib import Path
from podcaster_kerry.audio import Engine, dialogue_to_mp3
from . import SAMPLE
import pytest

# @pytest.mark.skipif(not os.getenv("GITHUB_ACTIONS"), reason="Only run on GitHub Actions")
def test_create_piper_json():
    temp_dir = Path("./outputs_piper/")
    shutil.rmtree(temp_dir, ignore_errors=True)
    assert not temp_dir.exists()

    output = Path("./combined.mp3")
    output.unlink(missing_ok=True)
    assert not output.exists()

    dialogue_to_mp3(SAMPLE, temp_dir, output)

    assert temp_dir.exists()
    assert output.exists()


# @pytest.mark.skipif(not os.getenv("GITHUB_ACTIONS"), reason="Only run on GitHub Actions")
def test_coqui_ai():
    temp_dir = Path("./outputs_coqui/")
    shutil.rmtree(temp_dir, ignore_errors=True)
    assert not temp_dir.exists()

    output = Path("./combined.mp3")
    output.unlink(missing_ok=True)
    assert not output.exists()

    dialogue_to_mp3(SAMPLE, temp_dir, output, engine=Engine.COQUI)

    assert temp_dir.exists()
    assert output.exists()
