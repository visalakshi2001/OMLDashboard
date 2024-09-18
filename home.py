import streamlit as st
import pandas as pd
from datetime import datetime

from widgets import make_calendar

def homefunc():

    sections = st.columns(3)

    with sections[0]:
        tc = st.container(border=True)
        bc = st.container(border=True)

        tc.markdown("<h5>Today's Schedule</h3>", True)
        tc.write(datetime.today().date().strftime("%A, %B %d, %Y"))

        calwid = make_calendar()
        with tc:
            calwid


    with sections[1]:
        co = st.container(border=True, height=500)
        co.markdown("<h5>Task List</h5>", True)

    with sections[2]:
        tc = st.container(border=True, height=350)
        bc = st.container(border=True, height=120)

        tc.markdown("<h5>Recent Changes</h5>", True)
        bc.markdown("<h5>Warnings Summary</h5>", True)


def progmgmtfunc():
    roles = pd.read_csv("reports/Responsibilities copy.csv", index_col=0)
    st.markdown("<h6>Assigned Responsibilities</h6>", True)
    st.dataframe(roles,hide_index=True)
