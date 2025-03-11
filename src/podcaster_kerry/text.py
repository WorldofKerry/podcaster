import os

def extract_text(in_path: os.PathLike):
    output = subprocess.check_output(["pdftotext", str(in_path), "-"], stderr=subprocess.STDOUT)
    text = output.decode("utf-8")
    return text