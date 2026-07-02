import streamlit as st

from leaderboard_store import leaderboard_configured, leaderboard_rows, load_leaderboard


st.set_page_config(
    page_title="NIAGADS Workshop Leaderboard",
    page_icon="🏆",
    layout="wide",
)

st.title("Workshop Leaderboard")
st.caption("Scores are sorted by points, required activity progress, completed skills, and fewer hints used.")

if not leaderboard_configured():
    st.warning("Leaderboard storage is not configured yet.")
    st.stop()

try:
    entries = load_leaderboard()
except Exception as error:
    st.error("Could not load the leaderboard from Google Sheets.")
    st.caption(str(error))
    st.stop()

rows = leaderboard_rows(entries)
if rows:
    st.dataframe(rows, hide_index=True, use_container_width=True)
else:
    st.caption("No leaderboard submissions yet.")

st.markdown("[Return to workshop challenge](../)")
