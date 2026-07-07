import os
from datetime import datetime

from config import *
from storage import *
from ollama import ask_ai



def get_existing_memory():

    memories = []

    if not os.path.exists(MEMORY_FOLDER):
        return ""

    for file in os.listdir(MEMORY_FOLDER):

        if file.endswith(".md"):

            path = os.path.join(
                MEMORY_FOLDER,
                file
            )

            content = read_file(path)

            memories.append(
                f"\nFILE: {file}\n{content}"
            )


    return "\n".join(memories)



def create_memory(conversation):

    prompt = f"""

Analyze this conversation.

Only extract information useful for future conversations.

Do not summarize everything.

Return:

FACTS:
- important facts about Christian

INTERESTS:
- long term interests

PROJECTS:
- projects mentioned

PREFERENCES:
- communication preferences


Conversation:

{conversation}

"""


    memory = ask_ai(prompt)


    if (
        "FACTS" in memory
        or
        "PROJECTS" in memory
        or
        "PREFERENCES" in memory
    ):

        update_memory(memory)



def update_memory(thought):

    existing_memory = get_existing_memory()


    prompt=f"""

You manage Mars' Obsidian memory system.

Current memory:

{existing_memory[-6000:]}


New information:

{thought}


Decide where this belongs.

Rules:

- Prefer updating existing notes.
- Avoid duplicate information.
- Use Obsidian links.
- Create meaningful connections.
- Do not create fake facts.
- Only save information explicitly known.


Available files:

Christian.md
Projects.md
Concepts.md
Preferences.md


Return exactly:

FILE:
filename.md


CONTENT:

markdown text here

"""


    update = ask_ai(prompt)


    try:

        if "FILE:" not in update:
            return


        if "CONTENT:" not in update:
            return


        filename = (
            update
            .split("FILE:",1)[1]
            .split("\n")[0]
            .strip()
        )


        content = (
            update
            .split("CONTENT:",1)[1]
            .strip()
        )


        if not filename or not content:
            return


        path=os.path.join(
            MEMORY_FOLDER,
            filename
        )


        append_file(
            path,
            "\n\n" + content
        )


        update_memory_index(
            filename,
            content
        )


        print(
            "Memory updated:",
            filename
        )


    except Exception as e:

        print(
            "Memory update failed:",
            e
        )



def update_memory_index(filename,content):

    links=[]


    for word in content.split():

        clean = (
            word
            .replace(",","")
            .replace(".","")
        )


        if (
            clean.startswith("[[")
            and
            clean.endswith("]]")
        ):

            links.append(clean)



    if not links:
        return


    text=f"""

## {filename}

Connections:

"""


    for link in links:

        text += f"- {link}\n"



    append_file(
        MEMORY_INDEX_FILE,
        text
    )
