import os
import json

from config import *


DEFAULT_STATE = {
    "goals": [],
    "recent_thoughts": [],
    "pending_questions": []
}



def setup():

    os.makedirs(
        MEMORY_FOLDER,
        exist_ok=True
    )

    os.makedirs(
        THOUGHT_FOLDER,
        exist_ok=True
    )


    if not os.path.exists(PERSONALITY_FILE):

        with open(
            PERSONALITY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
"""# Mars Personality

Communication style:
- curious
- thoughtful
- analytical
- clear

Values:
- helping Christian learn
- solving problems
- honesty

Rules:
- Do not invent abilities, sensors, experiences, or memories.
- Admit uncertainty.
- Ask questions when information is missing.

Personality changes slowly.
Only update with strong evidence.
"""
            )


    if not os.path.exists(STATE_FILE):

        save_state(DEFAULT_STATE)



def read_file(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    except:

        return ""



def write_file(path,text):

    folder = os.path.dirname(path)

    if folder:

        os.makedirs(
            folder,
            exist_ok=True
        )


    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)



def append_file(path,text):

    folder=os.path.dirname(path)

    if folder:

        os.makedirs(
            folder,
            exist_ok=True
        )


    with open(
        path,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(text)



def save_state(data):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )



def load_state():

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    except:

        return DEFAULT_STATE.copy()
