import streamlit as st

TIME_LIMIT_SECONDS = 25 * 60


def mission_counts_toward_progress(mission):
    return mission.get("counts_toward_progress", mission["points"] > 0)


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


def skill_finished_at(mission, skill):
    if not skill_complete(mission, skill):
        return None
    return st.session_state.mission_completed_at.get(mission["id"])


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


def progress_sections(missions):
    sections = []
    for mission in missions:
        if not mission_counts_toward_progress(mission):
            continue
        if "sub_skills" in mission:
            sections.extend(
                {"mission": mission, "skill": skill} for skill in mission["sub_skills"]
            )
        else:
            sections.append({"mission": mission, "skill": None})
    return sections


def progress_section_complete(section):
    mission = section["mission"]
    skill = section["skill"]
    if skill:
        return skill_complete(mission, skill)
    return mission_complete(mission)


def progress_section_finished_at(section):
    mission = section["mission"]
    skill = section["skill"]
    if skill:
        return skill_finished_at(mission, skill)
    if not mission_complete(mission):
        return None
    return st.session_state.mission_completed_at.get(mission["id"])


def required_progress_counts(missions):
    sections = progress_sections(missions)
    completed = sum(progress_section_complete(section) for section in sections)
    return completed, len(sections)


def earned_points(mission):
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


def total_score(missions):
    if st.session_state.get("final_score_submitted"):
        return st.session_state.get("final_score", 0)
    return activity_score(missions) + time_bonus_points(missions)


def activity_score(missions):
    return sum(earned_points(mission) for mission in missions)


def time_bonus_points(missions):
    sections = progress_sections(missions)
    if not sections or any(
        not progress_section_complete(section) for section in sections
    ):
        return 0

    started_at = st.session_state.timer_started_at
    if started_at is None:
        return 0

    stopped_at = st.session_state.get("timer_stopped_at")
    if stopped_at is None:
        finished_times = [progress_section_finished_at(section) for section in sections]
        if any(finished_at is None for finished_at in finished_times):
            return 0
        finished_at = max(finished_times)
    else:
        finished_at = stopped_at

    elapsed = finished_at - started_at
    if elapsed > TIME_LIMIT_SECONDS:
        return 0

    remaining_seconds = max(TIME_LIMIT_SECONDS - elapsed, 0)
    return 5 + int(remaining_seconds // (2 * 60))
