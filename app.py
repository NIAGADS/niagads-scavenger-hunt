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
    earned_points,
    mission_complete,
    mission_ready,
    mission_skills,
    skill_complete,
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


required_missions = [mission for mission in MISSIONS if mission["points"]]
completed_required = sum(mission_complete(mission) for mission in required_missions)
progress = completed_required / len(required_missions)
score = sum(earned_points(mission) for mission in MISSIONS)
completed_skills = completed_skill_names(MISSIONS)

render_sidebar(
    score,
    progress,
    completed_required,
    len(required_missions),
    completed_skills,
    ASSIGNMENT_POOL,
    AWARD_ICON,
)
render_page_header(
    completed_required, len(required_missions), score, completed_skills, AWARD_ICON
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
render_summary_and_submit(summary, score)
