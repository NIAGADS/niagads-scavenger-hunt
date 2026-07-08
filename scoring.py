import time

import streamlit as st

TIME_LIMIT_SECONDS = 20 * 60


def mission_ready(mission):
    answers = st.session_state.answers.get(mission["id"], {})
    return all(
        str(answers.get(field["key"], "")).strip()
        for field in mission["fields"]
        if field.get("required", True)
        and field.get("type") != "section"
        and not field.get("bonus_points")
    )


def mission_started(mission):
    answers = st.session_state.answers.get(mission["id"], {})
    return any(
        str(answers.get(field["key"], "")).strip()
        for field in mission["fields"]
        if (
            field.get("required", True)
            and field.get("type") != "section"
            and not field.get("bonus_points")
        )
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
    if timer_expired_before_completion(mission["id"]):
        return 0
    if mission["id"] in st.session_state.mission_base_points_awarded:
        return (
            st.session_state.mission_base_points_awarded[mission["id"]]
            + bonus_points(mission)
        )
    return current_points(mission)


def bonus_points(mission):
    answers = st.session_state.answers.get(mission["id"], {})
    return sum(
        field.get("bonus_points", 0)
        for field in mission["fields"]
        if field.get("bonus_points") and str(answers.get(field["key"], "")).strip()
    )


def current_points(mission):
    earned_bonus_points = bonus_points(mission)
    if not mission_complete(mission):
        return earned_bonus_points
    return mission["points"] + earned_bonus_points


def timer_expired_before_completion(mission_id):
    started_at = st.session_state.timer_started_at
    if started_at is None:
        return False
    completed_at = st.session_state.mission_completed_at.get(mission_id)
    if completed_at is None:
        completed_at = time.time()
    return completed_at > started_at + TIME_LIMIT_SECONDS
