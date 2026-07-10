import streamlit as st

from data.gene_scavenger_hunt import (
    ASSIGNMENT_POOL,
    AWARD_ICON,
    INTRO_VIDEO_PATH,
    MISSIONS,
    RESOURCES,
)
from src.scoring import (
    completed_skill_names,
    mission_complete,
    mission_ready,
    mission_skills,
    required_progress_counts,
    skill_complete,
    total_score,
)
from src.state import initialize_state
from src.summary import build_summary
from src.ui import (
    render_landing_page,
    render_leaderboard_view,
    render_missions,
    render_page_header,
    render_sidebar,
    render_styles,
    render_summary_and_submit,
)

st.set_page_config(
    page_title="NIAGADS Open Access AD Gene Challenge",
    page_icon="🧬",
    layout="wide",
)


def resource_url(resource):
    return RESOURCES[resource]


initialize_state(ASSIGNMENT_POOL)
render_styles()


if st.query_params.get("view") == "leaderboard":
    render_leaderboard_view()

if not st.session_state.hunt_started:
    render_landing_page(INTRO_VIDEO_PATH)
    st.stop()


completed_required, required_count = required_progress_counts(MISSIONS)
progress = completed_required / required_count
score = total_score(MISSIONS)
completed_skills = completed_skill_names(MISSIONS)

render_sidebar(
    score,
    progress,
    completed_required,
    required_count,
    completed_skills,
    ASSIGNMENT_POOL,
    AWARD_ICON,
)
render_page_header(
    completed_required, required_count, score, completed_skills, AWARD_ICON
)
render_missions(
    MISSIONS,
    AWARD_ICON,
    mission_complete,
    mission_ready,
    mission_skills,
    skill_complete,
    resource_url,
)

summary = build_summary(MISSIONS)
render_summary_and_submit(summary, MISSIONS)
