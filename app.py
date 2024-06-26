import streamlit as st
import pandas as pd
from dashboard import dashfunc
from architechture import sysarcfunc


st.set_page_config(page_title="Dashboard", page_icon="🍩", layout="wide")

testtab, archtab = st.tabs(["Testing", "Architechture"])

with testtab:
    dashfunc()

with archtab:
    sysarcfunc()