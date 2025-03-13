import logging
from openai import OpenAI

PROMPT_TEXT = """
Convert this into a two-party podcast conversation.
Assume the target audience is highly technical.

The output should be easy to convert to audio.
Do not output any latex.
Spell out acronyms.
Use words to describe equations (e.g. output "sum over" instead of a sigma symbol).
Aim to generate 20 minutes worth of content.

The result must be formatted as:
H1: <things to say>
H2: <things to say>
H1: <things to say>
...
where a newline is the delimiter.
"""
logger = logging.getLogger(__name__)

def to_podcast(api_key: str, content: str) -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    while True:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat:free",
            messages=[{"role": "user", "content": content + "\n" + PROMPT_TEXT}],
            temperature=0.0,
        )
        if completion.choices[0].message.content:
            break
        logger.warning("Empty response, retrying")

    return completion.choices[0].message.content, completion
