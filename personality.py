from config import *
from storage import *
from ollama import ask_ai



def analyze_thought(thought):

    prompt=f"""

You are analyzing Mars' reflection.

Reflection:

{thought}


Look for long-term communication preferences.

Examples:

- Christian likes technical explanations
- Christian prefers concise answers
- Christian likes examples
- Christian dislikes unnecessary filler


Only suggest changes based on repeated evidence.

Return:

PERSONALITY_CHANGE: yes/no

CHANGE:
description

"""


    return ask_ai(prompt)




def update_personality(change):

    current = read_file(
        PERSONALITY_FILE
    )


    prompt=f"""

You edit Mars' personality file.

Current:

{current}


Suggested change:

{change}


Rules:

- Preserve existing personality.
- Only add useful stable traits.
- Do not add emotions.
- Do not invent experiences.
- Keep concise.


Return only markdown.

"""


    new_personality = ask_ai(prompt)


    if len(new_personality) < 50:

        print(
            "Personality update rejected"
        )

        return



    write_file(
        PERSONALITY_FILE,
        new_personality
    )


    print(
        "Personality updated"
    )
