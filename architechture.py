import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts
import plotly.express as px

def treemaps():
    df = pd.read_csv("reports/SystemArchitecture.csv", index_col=0)
    data = {'Rover_System': [
            {'Rover_Comms': {}}, 
            {'Rover_Mobility': {}}
        ]
        }
    option = {
    "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
    "series": [
        {
            "type": "tree",
            "data": [data],
            "top": "1%",
            "left": "7%",
            "bottom": "1%",
            "right": "20%",
            "symbolSize": 7,
            "label": {
                "position": "left",
                "verticalAlign": "middle",
                "align": "right",
                "fontSize": 9,
            },
            "leaves": {
                "label": {
                    "position": "right",
                    "verticalAlign": "middle",
                    "align": "left",
                }
            },
            "emphasis": {"focus": "descendant"},
            "expandAndCollapse": True,
            "animationDuration": 550,
            "animationDurationUpdate": 750,
        }
    ],
}
    st.dataframe(df)
    st_echarts(options=option, height="500px")