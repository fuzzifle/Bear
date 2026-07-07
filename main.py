import threading
import time


from storage import setup

from threads import (
    brain_loop,
    input_loop,
    thinker_loop
)



if __name__=="__main__":


    setup()


    print(
        """
==========================
       MARS AI
==========================

Brain starting...

"""
    )


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
        "Mars is running."
    )



    while True:

        time.sleep(1)
