import random
from uuid import uuid4

import streamlit as st


TEAM_NAME_ADJECTIVES = [
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
TEAM_NAME_TOPICS = [
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
TEAM_NAME_NOUNS = [
    "Analysts",
    "Explorers",
    "Mappers",
    "Reviewers",
    "Scouts",
    "Team",
    "Trackers",
    "Working Group",
]
TEAM_NAME_CODE_RANGE = range(100, 1000)


def random_team_name():
    code = random.choice(TEAM_NAME_CODE_RANGE)
    return (
        f"{random.choice(TEAM_NAME_ADJECTIVES)} "
        f"{random.choice(TEAM_NAME_TOPICS)} "
        f"{random.choice(TEAM_NAME_NOUNS)} {code}"
    )


def initialize_state(assignment_pool):
    defaults = {
        "team_name": random_team_name(),
        "email": "",
        "assigned_gene": random.choice(assignment_pool),
        "leaderboard_entry_id": uuid4().hex,
        "leaderboard_submitted": False,
        "final_score_submitted": False,
        "final_score": None,
        "final_activity_score": None,
        "final_time_bonus_points": None,
        "hunt_started": False,
        "timer_started_at": None,
        "timer_stopped_at": None,
        "answers": {},
        "completed_missions": set(),
        "mission_completed_at": {},
        "mission_base_points_awarded": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
