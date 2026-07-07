import time

from config import *
from chat import chat
from brain import think



def brain_loop():

    while True:

        task,data = queue.get()

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

        try:

            text=input(
                "You > "
            )


            if text.strip():

                queue.put(
                    (
                    "chat",
                    text
                    )
                )


        except KeyboardInterrupt:

            break



def thinker_loop():

    while True:

        time.sleep(
            THINK_INTERVAL
        )


        queue.put(
            (
            "think",
            ""
            )
        )
