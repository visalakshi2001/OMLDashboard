import streamlit as st
import pandas as pd

from dashboard import dashschedule, dashresults, dashreqs
from architecture import sysarcfunc
from issues import sysissues
from home import homefunc, progmgmtfunc


st.set_page_config(page_title="Dashboard", page_icon="🍩", layout="wide")


def main():
    TABS = ["Home", "Program Management", "Requirements",
             "Architecture", "Test Schedule", "Test Results", "Warnings/Issues"]

    st.header("🧮 Dashboard", divider="red")

    tabs = st.tabs(TABS)

    with tabs[0]:
        homefunc()
    with tabs[1]:
        progmgmtfunc()
    with tabs[2]:
        dashreqs()
    with tabs[3]:
        sysarcfunc()
    with tabs[4]:
        dashschedule()
    with tabs[5]:
        dashresults()
    with tabs[6]:
        sysissues()

    
if __name__ == "__main__":
    main()