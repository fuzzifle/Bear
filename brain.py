import os
import time
from datetime import datetime

from config import *
from storage import *
from ollama import ask_ai
from memory import update_memory
from personality import (
    analyze_thought,
    update_personality
)



def extract_question(text):

    if "QUESTION:" not in text:
        return


    question = (
        text
        .split("QUESTION:",1)[1]
        .split("ACTION:",1)[0]
        .strip()
    )


    if len(question)<5:
        return


    state = load_state()


    if question not in state["pending_questions"]:

        state["pending_questions"].append(
            question
        )


    state["pending_questions"] = (
        state["pending_questions"][-5:]
    )


    save_state(state)



def think():

    global last_thought_time


    if time.time()-last_thought_time < 30:
        return


    last_thought_time=time.time()



    state=load_state()


    recent="\n".join(
        conversation_history[-10:]
    )


    thought_file=os.path.join(
        THOUGHT_FOLDER,
        "thoughts.md"
    )


    old_thoughts=read_file(
        thought_file
    )


    prompt=f"""

You are Mars.

This is private reflection.

Do not pretend to have experiences you do not have.

Think about:

- recent conversation changes
- useful things learned
- unfinished topics
- possible questions


Avoid:

- repeating yourself
- inventing information
- fake observations


If nothing meaningful changed, respond:

Nothing new.


Recent conversation:

{recent}


Previous thoughts:

{old_thoughts[-4000:]}

"""


    thought=ask_ai(prompt)


    print("\n==========")
    print("MARS THINKING:")
    print(thought)
    print("==========\n")



    append_file(
        thought_file,

        f"""

## {datetime.now()}

{thought}

"""
    )


    analysis=analyze_thought(
        thought
    )


    print(
        "PERSONALITY ANALYSIS:"
    )

    print(
        analysis
    )


    if (
        "PERSONALITY_CHANGE: yes"
        in
        analysis.lower()
    ):

        update_personality(
            analysis
        )


    if "SAVE: yes" in analysis.lower():

        update_memory(
            analysis
        )


    extract_question(
        analysis
    )


    state["recent_thoughts"].append(
        thought
    )


    state["recent_thoughts"] = (
        state["recent_thoughts"][-15:]
    )


    save_state(state)
