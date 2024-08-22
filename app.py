import streamlit as st
import pandas as pd
from dashboard import dashfunc
from architechture import sysarcfunc
from issues import sysissues


st.set_page_config(page_title="Dashboard", page_icon="🍩", layout="wide")

def sidebar(pages: list):
    with st.sidebar:
        page = st.radio("Navigation", pages)
    
    return page


def main():
    PAGES = ["📊 Dashboard", "🪧 Issues"]

    st.header("🧮 Dashboard", divider="red")

    page = sidebar(PAGES)

    if page == PAGES[0]:
        testtab, archtab = st.tabs(["Testing", "Architecture"])
        with testtab:
            dashfunc()

        with archtab:
            sysarcfunc()
    if page == PAGES[1]:
        sysissues()

    
    
if __name__ == "__main__":
    main()