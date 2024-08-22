import streamlit as st

# hyperlink that shows issues from the issues graph
# warning that requirements have not been verified (green) or failed (red)
# test schedules, if not scheduled in metrics and warning that tests have not been scheduled
# changes needed in confidence values

def sysissues():


    top_cols = st.columns(3)

    with top_cols[0]:
        conflicts = st.expander("⚠️ Four tests have overlapped scheduling", expanded=True)

        with conflicts:
            st.error("TerrainTraversalExercise is colliding with other tests", icon="❗")
            st.error("PayloadDeploymentTest is colliding with other tests", icon="❗")
            st.error("MobilityDeploymentTest is colliding with other tests", icon="❗")
            st.error("AntennaDeploymentTest is colliding with other tests", icon="❗")