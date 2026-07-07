import streamlit as st


def mission_ready(mission):
    answers = st.session_state.answers.get(mission["id"], {})
    return all(
        str(answers.get(field["key"], "")).strip()
        for field in mission["fields"]
        if field.get("required", True)
        and field.get("type") != "section"
        and not field.get("bonus_points")
    )


def mission_complete(mission):
    return mission["id"] in st.session_state.completed_missions


def skill_complete(mission, skill):
    if not mission_complete(mission):
        return False
    answers = st.session_state.answers.get(mission["id"], {})
    return all(str(answers.get(field_key, "")).strip() for field_key in skill["fields"])


def mission_skills(mission):
    if "sub_skills" in mission:
        return mission["sub_skills"]
    return [
        {
            "skill": mission["skill"],
            "fields": [
                field["key"]
                for field in mission["fields"]
                if field.get("type") != "section"
                and field.get("required", True)
                and not field.get("bonus_points")
            ],
        }
    ]


def completed_skill_names(missions):
    skills = []
    for mission in missions:
        if "sub_skills" in mission:
            skills.extend(
                skill["skill"]
                for skill in mission["sub_skills"]
                if skill_complete(mission, skill)
            )
        elif mission_complete(mission):
            skills.append(mission["skill"])
    return skills


def earned_points(mission):
    answers = st.session_state.answers.get(mission["id"], {})
    bonus_points = sum(
        field.get("bonus_points", 0)
        for field in mission["fields"]
        if field.get("bonus_points") and str(answers.get(field["key"], "")).strip()
    )
    if not mission_complete(mission):
        return bonus_points
    base_points = max(
        mission["points"] - (1 if mission["id"] in st.session_state.hints_used else 0),
        0,
    )
    return base_points + bonus_points
