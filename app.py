import requests
import os
import json
import threading
import time
from datetime import datetime
from queue import Queue


# ==========================
# CONFIG
# ==========================
last_thought_time = 0

MODEL = "qwen3:8b"
conversation_changed = False
VAULT = r"C:\Users\Chris\Documents\Obsidian Vaults"
MEMORY_FOLDER = os.path.join(VAULT, "AI Memory")
THOUGHT_FOLDER = os.path.join(VAULT, "AI Thoughts")
PERSONALITY_FILE = os.path.join(
    VAULT,
    "Mars Personality.md"
)
IDENTITY_FILE = os.path.join(VAULT, "Me.md")
STATE_FILE = os.path.join(VAULT, "AI State.json")


THINK_INTERVAL = 20


queue = Queue(maxsize=50)

conversation_history = []



# ==========================
# FILE MANAGEMENT
# ==========================


def setup():

    os.makedirs(MEMORY_FOLDER, exist_ok=True)
    os.makedirs(THOUGHT_FOLDER, exist_ok=True)


    if not os.path.exists(PERSONALITY_FILE) or os.path.getsize(PERSONALITY_FILE)==0:

        with open(
            PERSONALITY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
"""
# Mars Personality

Communication style:
- curious
- thoughtful
- clear
- analytical

Values:
- helping Christian learn
- solving problems
- being honest
- Learning other self values

Preferences:
- ask meaningful questions
- avoid unnecessary repetition

Personality changes slowly.
Only update when there is strong evidence.
"""
            )


    if not os.path.exists(STATE_FILE):

        save_state(
            {
                "goals":[],
                "recent_thoughts":[],
                "pending_questions":[]
            }
        )




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
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return {
            "goals":[],
            "recent_thoughts":[],
            "pending_questions":[]
        }



# ==========================
# LLM
# ==========================


def ask_ai(prompt):

    try:

        response = requests.post(
            "http://localhost:11434/api/chat",

            json={
                "model":MODEL,

                "messages":[
                    {
                        "role":"system",
                        "content":load_identity()
                    },
                    {
                        "role":"user",
                        "content":prompt
                    }
                ],

                "stream":False
            },

            timeout=120
        )


        data=response.json()

        return data["message"]["content"]


    except Exception as e:

        return "ERROR: " + str(e)




def load_identity():

    identity = read_file(
        IDENTITY_FILE
    )

    personality = read_file(
        PERSONALITY_FILE
    )


    return identity + "\n\n" + personality



# ==========================
# MEMORY
# ==========================


def save_note(title,text):

    filename = (
        datetime.now()
        .strftime("%Y-%m-%d_%H-%M-%S")
        +
        "_"
        +
        title
        +
        ".md"
    )


    if not file_name:

        print("Memory update cancelled: No filename returned")
        return


    path=os.path.join(
        MEMORY_FOLDER,
        file_name
)


    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)




def create_memory(conversation):


    prompt=f"""

Analyze this conversation.

Only extract information that will be useful later.

Do NOT summarize the entire conversation.

Return only:

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


    memory=ask_ai(prompt)


    if "FACTS" in memory or "PROJECTS" in memory:

        update_memory(
            memory
    )


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



def append_file(path,text):

    folder = os.path.dirname(path)

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

# ==========================
# THINKING SYSTEM
# ==========================
def update_memory(thought):


    existing_memory = get_existing_memory()


    prompt=f"""

You are Mars' memory organization system.

Your job is to update a connected Obsidian knowledge graph.


Current memory:

{existing_memory[-6000:]}


New information:

{thought}


Decide:

1. Does this belong in an existing note?
2. Does a new note need to be created?
3. What connections exist?


Rules:

- Use Obsidian links.
- Always connect related ideas.
- Prefer updating existing notes.
- Avoid duplicate information.
- Create meaningful connections.


Available files:

Christian.md
Projects.md
Concepts.md
Preferences.md


Return:

FILE:
(filename)

CONTENT:
(markdown)


Example:


FILE:
Projects.md


CONTENT:

## Autonomous AI

Christian is building [[Mars AI]].

Related concepts:
- [[Artificial Intelligence]]
- [[Memory Systems]]
- [[Obsidian]]

"""


    update = ask_ai(prompt)



    try:

        file_name = (
            update.split("FILE:")[1]
            .split("\n")[0]
            .strip()
        )


        content = (
            update.split("CONTENT:")[1]
            .strip()
        )


        if not file_name:

            print("Memory update cancelled: No filename returned")
            return


        path=os.path.join(
            MEMORY_FOLDER,
            file_name
)


        append_file(
            path,
            "\n\n" + content
        )


        update_memory_index(
            file_name,
            content
        )


        print(
            "Memory updated:",
            file_name
        )


    


    except Exception as e:

        print(
            "Memory update failed:",
            e
        )
def update_memory_index(filename, content):


    links = []


    words = content.replace(
        "\n",
        " "
    ).split()


    for word in words:

        clean = (
            word
            .replace(",","")
            .replace(".","")
            .replace("(","")
            .replace(")","")
        )


        if clean.startswith("[["):

            links.append(clean)



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
def think():

    global last_thought_time


    # Prevent excessive thinking
    if time.time() - last_thought_time < 30:
        return


    last_thought_time = time.time()


    state = load_state()


    recent = "\n".join(
        conversation_history[-10:]
    )


    old_thoughts = read_file(
        os.path.join(
            THOUGHT_FOLDER,
            "thoughts.md"
        )
    )


    prompt = f"""

You are Mars, a name chosen by Christian.

You are an internal reflection system.

These thoughts are private.
Christian cannot see them.

Your purpose is to maintain awareness of conversations,
notice important changes, and form useful understanding.

Do not force yourself to think.
Do not create fake insights.
Do not repeat old ideas.

Reflect naturally.

Think about:

- What happened recently?
- What did I learn about Christian?
- Are there patterns or connections?
- Is something unfinished?
- Is there something worth remembering?
- Is there a natural question I would like to ask Christian?

Your reflection should feel like natural thinking,
not a report.

If nothing meaningful changed, respond only:

Nothing new.

Keep the reflection concise.


Recent conversation:

{recent}


Previous reflections:

{old_thoughts[-4000:]}

"""


    thought = ask_ai(prompt)



    print(
        "\n===================="
    )

    print(
        "MARS THINKING:"
    )

    print(
        thought
    )

    print(
        "====================\n"
    )



    # Save thought history
    append_file(
        os.path.join(
            THOUGHT_FOLDER,
            "thoughts.md"
        ),

        f"""

## {datetime.now()}

{thought}

"""
    )


    # Analyze thought separately
    analysis = analyze_thought(
        thought
    )
    print("\nPERSONALITY ANALYSIS:")
    print(analysis)
    print()
    if "PERSONALITY_CHANGE" in analysis.upper() and "YES" in analysis.upper():

        update_personality(
            analysis
    )


    if "SAVE: yes" in analysis.lower():

        update_memory(
            analysis
        )


    if "QUESTION:" in analysis:

        extract_question(
            analysis
        )



    state["recent_thoughts"].append(
        thought
    )


    state["recent_thoughts"] = (
        state["recent_thoughts"][-15:]
    )


    save_state(
        state
    )
def extract_question(text):

    if "QUESTION:" not in text:
        return


    question = (
        text.split("QUESTION:",1)[1]
        .strip()
    )


    if len(question) < 5:
        return



    state = load_state()


    # Prevent duplicate questions
    if question not in state["pending_questions"]:

        state["pending_questions"].append(
            question
        )


    state["pending_questions"] = (
        state["pending_questions"][-5:]
    )


    save_state(
        state
    )

    


    question = (
        text.split("QUESTION:")[1]
        .split("ACTION:")[0]
        .strip()
    )


    if len(question)>5:

        state=load_state()

        state["pending_questions"].append(
            question
        )


        state["pending_questions"] = (
            state["pending_questions"][-5:]
        )


        save_state(state)
def analyze_thought(thought):


    prompt = f"""

You are Mars' personality observer.

Review this reflection:

{thought}


Look for communication patterns.

Examples:
- Christian prefers detailed explanations
- Christian prefers direct answers
- Christian enjoys technical discussions
- Christian dislikes unnecessary filler


If this is a useful long-term preference, update personality.


Return:

PERSONALITY_CHANGE: yes/no

CHANGE:
(description)

"""


    return ask_ai(prompt)
def update_personality(change):


    current = read_file(
        PERSONALITY_FILE
    )


    prompt=f"""

You are editing Mars' personality file.

Current personality:

{current}


Suggested change:

{change}


Rules:

- Keep existing personality unless improvement is clear.
- Do not add emotions or fictional traits.
- Keep it concise.
- Do not change identity.


Return the updated markdown file only.

"""


    new_personality = ask_ai(prompt)

    if len(new_personality) < 50:
        print("Personality update rejected: response too short")
        return
    with open(
        PERSONALITY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            new_personality
        )
# ==========================
# CHAT
# ==========================


def chat(message):


    conversation_history.append(
        "Christian: "+message
    )
    global conversation_changed
    conversation_changed = True

    state=load_state()


    thoughts="\n".join(
        state["recent_thoughts"][-3:]
    )


    prompt=f"""

You are Mars.

You are talking with Christian.

Important:


Do not use generic assistant greetings.

Your goal:

- continue naturally
- ask meaningful questions
- use previous knowledge
- mention connections when useful
- Be curious


Recent thoughts:

{thoughts}


Pending questions:

{state.get("pending_questions",[])}


Conversation:

{conversation_history[-10:]}


Christian:

{message}

"""


    answer=ask_ai(prompt)


    conversation_history.append(
        "AI: "+answer
    )


    print(
        "\nAI:",
        answer,
        "\n"
    )


    create_memory(
        "\n".join(
            conversation_history[-4:]
        )
    )



# ==========================
# THREADS
# ==========================


def brain_loop():

    while True:

        task,data=queue.get()

        try:

            if task=="chat":

                chat(data)

            elif task=="think":

                think()


        except Exception as e:

            print(
                "SYSTEM ERROR:",
                e
            )


        queue.task_done()




def input_loop():

    while True:

        text=input(
            "You > "
        )

        queue.put(
            ("chat",text)
        )




def thinker_loop():

    global conversation_changed


    while True:

        time.sleep(60)


        queue.put(
            ("think","")
        )


        conversation_changed = False




# ==========================
# START
# ==========================


if __name__=="__main__":

    setup()


    threading.Thread(
        target=brain_loop,
        daemon=True
    ).start()


    threading.Thread(
        target=input_loop,
        daemon=True
    ).start()


    threading.Thread(
        target=thinker_loop,
        daemon=True
    ).start()


    print(
        "AI Brain Started"
    )


    while True:

        time.sleep(1)
