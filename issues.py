import streamlit as st

# hyperlink that shows issues from the issues graph
# warning that requirements have not been verified (green) or failed (red)
# test schedules, if not scheduled in metrics and warning that tests have not been scheduled
# changes needed in confidence values

def sysissues():


    top_cols = st.columns(3)

    with top_cols[0]:
        conflicts = st.expander("⚠️ Four tests have overlapping schedule", expanded=True)

        with conflicts:
            st.error("TerrainTraversalExercise has potential schedule conflict with other tests", icon="❗")
            st.error("PayloadDeploymentTest has potential schedule conflict with other tests", icon="❗")
            st.error("MobilityDeploymentTest has potential schedule conflict with other tests", icon="❗")
            st.error("AntennaDeploymentTest has potential schedule conflict with other tests", icon="❗")

def issuesinfo():
    st.markdown("<h6>Issues</h6>", True)
    with st.container(border=True, height=150):
        st.warning('Four tests have overlapped scheduling (find more info on Issues tab)', icon="⚠️")