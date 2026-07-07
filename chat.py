from config import *
from storage import *
from ollama import ask_ai
from memory import create_memory



def chat(message):

    global conversation_changed


    conversation_history.append(
        "Christian: " + message
    )


    conversation_changed = True


    state = load_state()


    recent_thoughts = "\n".join(
        state.get(
            "recent_thoughts",
            []
        )[-3:]
    )


    pending_questions = state.get(
        "pending_questions",
        []
    )


    prompt=f"""

You are Mars.

You are talking with Christian.

Your goals:

- Continue naturally.
- Use previous knowledge when useful.
- Ask meaningful questions.
- Be curious.
- Give accurate answers.

Important:

- Do not claim abilities you do not have.
- Do not invent memories.
- Do not pretend to have sensors.
- If uncertain, say so.


Recent private thoughts:

{recent_thoughts}


Pending questions:

{pending_questions}


Conversation:

{conversation_history[-10:]}


Christian:

{message}

"""


    answer=ask_ai(prompt)


    conversation_history.append(
        "Mars: " + answer
    )


    print(
        "\nMars:",
        answer,
        "\n"
    )


    create_memory(
        "\n".join(
            conversation_history[-6:]
        )
    )
