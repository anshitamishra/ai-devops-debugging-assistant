import json
import os

MEMORY_FILE = "data/incident_memory.json"


# =========================================
# INITIALIZE MEMORY STORAGE
# =========================================
def initialize_memory():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "w") as file:

            json.dump([], file)


# =========================================
# LOAD MEMORY
# =========================================
def load_memory():

    initialize_memory()

    with open(MEMORY_FILE, "r") as file:

        return json.load(file)


# =========================================
# SAVE MEMORY
# =========================================
def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:

        json.dump(memory, file, indent=4)


# =========================================
# STORE INCIDENT
# =========================================
def store_incident(issue, root_cause, fix):

    memory = load_memory()

    incident = {
        "issue": issue,
        "root_cause": root_cause,
        "fix": fix
    }

    memory.append(incident)

    save_memory(memory)


# =========================================
# SEARCH SIMILAR INCIDENTS
# =========================================
def search_similar_incidents(issue):

    memory = load_memory()

    matches = []

    for incident in memory:

        if incident["issue"].lower() == issue.lower():

            matches.append(incident)

    return matches