import random
from uuid import uuid4

import streamlit as st


TEAM_LABEL_ADJECTIVES = [
    "Agile",
    "Bright",
    "Careful",
    "Focused",
    "Insightful",
    "Lively",
    "Methodical",
    "Quick",
    "Sharp",
    "Steady",
]
TEAM_LABEL_TOPICS = [
    "Amyloid",
    "Atlas",
    "Cohort",
    "Genome",
    "Haplotype",
    "Hippocampus",
    "Microglia",
    "Signal",
    "Synapse",
    "Tau",
    "Variant",
]
TEAM_LABEL_NOUNS = [
    "Analysts",
    "Explorers",
    "Mappers",
    "Reviewers",
    "Scouts",
    "Team",
    "Trackers",
    "Working Group",
]
TEAM_LABEL_CODE_RANGE = range(100, 1000)


def random_team_label():
    code = random.choice(TEAM_LABEL_CODE_RANGE)
    return (
        f"{random.choice(TEAM_LABEL_ADJECTIVES)} "
        f"{random.choice(TEAM_LABEL_TOPICS)} "
        f"{random.choice(TEAM_LABEL_NOUNS)} {code}"
    )


def initialize_state(assignment_pool):
    defaults = {
        "team_name": "",
        "leader_email": "",
        "team_label": random_team_label(),
        "assigned_gene": random.choice(assignment_pool),
        "leaderboard_entry_id": uuid4().hex,
        "leaderboard_submitted": False,
        "timer_started_at": None,
        "answers": {},
        "hints_used": set(),
        "field_hints_used": set(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
