from datetime import datetime, timezone

import streamlit as st

from scoring import (
    completed_skill_names,
    earned_points,
    mission_complete,
    mission_skills,
)


def build_summary(missions):
    required = [mission for mission in missions if not mission["bonus"]]
    return {
        "team_name": st.session_state.team_name,
        "leader_email": st.session_state.leader_email,
        "team_label": st.session_state.team_label,
        "assigned_gene": st.session_state.assigned_gene,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "score": sum(earned_points(mission) for mission in missions),
        "required_activities_completed": sum(
            mission_complete(mission) for mission in required
        ),
        "required_activities_total": len(required),
        "skills_completed": completed_skill_names(missions),
        "hints_used": sorted(st.session_state.hints_used),
        "activities": [
            {
                "id": mission["id"],
                "title": mission["title"],
                "skill": mission["skill"],
                "skills": [skill["skill"] for skill in mission_skills(mission)],
                "bonus": mission["bonus"],
                "complete": mission_complete(mission),
                "points_awarded": earned_points(mission),
                "answers": st.session_state.answers.get(mission["id"], {}),
            }
            for mission in missions
        ],
    }
