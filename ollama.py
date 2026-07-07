import requests

from config import *
from storage import read_file



def load_identity():

    identity = read_file(
        IDENTITY_FILE
    )

    personality = read_file(
        PERSONALITY_FILE
    )


    return f"""
{identity}


{personality}


Reality rules:
- You are a software system.
- You do not have physical sensors unless explicitly connected.
- Do not claim to see, hear, feel, or measure anything.
- Do not create fake statistics.
- If you do not know something, say so.
"""



def ask_ai(prompt):

    try:

        response=requests.post(

            "http://localhost:11434/api/chat",

            json={

                "model": MODEL,

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

        return f"ERROR: {e}"
