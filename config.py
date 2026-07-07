import os
from queue import Queue


# ==========================
# AI SETTINGS
# ==========================

MODEL = "qwen3:8b"


# ==========================
# OBSIDIAN PATHS
# ==========================

VAULT = r"C:\Users\Chris\Documents\Obsidian Vaults"


MEMORY_FOLDER = os.path.join(
    VAULT,
    "AI Memory"
)


THOUGHT_FOLDER = os.path.join(
    VAULT,
    "AI Thoughts"
)


PERSONALITY_FILE = os.path.join(
    VAULT,
    "Mars Personality.md"
)


IDENTITY_FILE = os.path.join(
    VAULT,
    "Me.md"
)


STATE_FILE = os.path.join(
    VAULT,
    "AI State.json"
)


MEMORY_INDEX_FILE = os.path.join(
    MEMORY_FOLDER,
    "Memory Index.md"
)



# ==========================
# SYSTEM SETTINGS
# ==========================

THINK_INTERVAL = 60


MAX_MEMORY_RESULTS = 6000


queue = Queue(maxsize=50)


conversation_history = []


last_thought_time = 0


conversation_changed = False
