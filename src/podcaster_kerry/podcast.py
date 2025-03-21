import logging
from openai import OpenAI

PROMPT_TEXT = """
Convert this into a two-party podcast conversation.
Assume the target audience is highly technical.

The output should be easy to convert to audio.
Do not output any latex.
Spell out acronyms.
Use words to describe equations (e.g. output "sum over" instead of a sigma symbol).
Aim to generate at least 20 entries in result.

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
    for model in ["meta-llama/llama-3.3-70b-instruct:free", "deepseek/deepseek-chat:free"]:
        logging.info(f"Using {model}")
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": PROMPT_TEXT},
                {"role": "user", "content": content},
            ],
            temperature=0.0,
        )
        try:
            if completion.choices[0].message.content:
                break
        except TypeError:
            pass
        logger.warning("Empty response, retrying")

    return completion.choices[0].message.content, completion
