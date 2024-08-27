import streamlit as st
import pandas as pd
from dashboard import dashfunc, dashresults
from architechture import sysarcfunc
from issues import sysissues


st.set_page_config(page_title="Dashboard", page_icon="🍩", layout="wide")


def main():
    PAGES = ["📊 Dashboard", "🪧 Issues"]

    st.header("🧮 Dashboard", divider="red")

    archtab, testtab, resultstab, issuestab = st.tabs(["Architecture", "Test Schedule", "Test Results", "Warnings/Issues"])
    with testtab:
        dashfunc()
    with archtab:
        sysarcfunc()
    with resultstab:
        dashresults()
    with issuestab:
        sysissues()

    
if __name__ == "__main__":
    main()