from datetime import datetime, timezone

import streamlit as st

from src.scoring import (
    activity_score,
    completed_skill_names,
    earned_points,
    mission_complete,
    mission_skills,
    required_progress_counts,
    time_bonus_points,
    total_score,
)


def build_summary(missions):
    activity_points = activity_score(missions)
    time_bonus = time_bonus_points(missions)
    completed_required, required_total = required_progress_counts(missions)
    if st.session_state.final_score_submitted:
        activity_points = st.session_state.final_activity_score
        time_bonus = st.session_state.final_time_bonus_points
        score = st.session_state.final_score
    else:
        score = total_score(missions)
    return {
        "team_name": st.session_state.team_name,
        "email": st.session_state.email,
        "assigned_gene": st.session_state.assigned_gene,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "score": score,
        "activity_score": activity_points,
        "time_bonus_points": time_bonus,
        "required_activities_completed": completed_required,
        "required_activities_total": required_total,
        "skills_completed": completed_skill_names(missions),
        "activities": [
            {
                "id": mission["id"],
                "title": mission["title"],
                "skill": mission["skill"],
                "skills": [skill["skill"] for skill in mission_skills(mission)],
                "complete": mission_complete(mission),
                "points_awarded": earned_points(mission),
                "answers": st.session_state.answers.get(mission["id"], {}),
            }
            for mission in missions
        ],
    }
