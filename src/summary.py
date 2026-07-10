from datetime import datetime, timezone

import streamlit as st

from src.scoring import (
    activity_score,
    completed_skill_names,
    earned_points,
    mission_complete,
    mission_skills,
    time_bonus_points,
    total_score,
)


def build_summary(missions):
    required = [mission for mission in missions if mission["points"]]
    activity_points = activity_score(missions)
    time_bonus = time_bonus_points(missions)
    return {
        "team_name": st.session_state.team_name,
        "email": st.session_state.email,
        "assigned_gene": st.session_state.assigned_gene,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "score": total_score(missions),
        "activity_score": activity_points,
        "time_bonus_points": time_bonus,
        "required_activities_completed": sum(
            mission_complete(mission) for mission in required
        ),
        "required_activities_total": len(required),
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
