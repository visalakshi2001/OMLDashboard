import streamlit as st
from streamlit_echarts import st_echarts
import plotly.express as px
import pandas as pd
import numpy as np

from datetime import datetime, timedelta



def set_datewise_color(df):
    df["color"] = df['datetime'].duplicated(keep=False).map({True: '#ff4b4b', False: 'royalblue'})

    return df

def dashfunc():

    top_columns = st.columns(2)

    with top_columns[0]:
        programs = pd.read_csv(r"reports\TestPrograms.csv", index_col=0)

        st.markdown("<h6>Scheduled Test Programs</h6>", True)
        metriccols = st.columns(4)
        for i,num in enumerate(programs["num_Tests"]):
            metriccols[i].metric(label=programs.iloc[i]["TestProgram"], value=num, delta=f"{num-2} Scheduled", delta_color="off")

    with top_columns[1]:
        st.markdown("<h6>Issues</h6>", True)
        with st.container(border=True, height=150):
            st.warning('Four tests have overlapped scheduling', icon="⚠️",)
            st.error("TerrainTraversalExercise is colliding with other tests", icon="❗")
            st.error("PayloadDeploymentTest is colliding with other tests", icon="❗")
            st.error("MobilityDeploymentTest is colliding with other tests", icon="❗")
            st.error("AntennaDeploymentTest is colliding with other tests", icon="❗")

    middle_columns = st.columns(2)
    with middle_columns[0]:
        tests = pd.read_csv("reports\TestProcedures.csv", index_col=0)
        tests["datetime"] = pd.to_datetime(tests["datetime"])
        tests = set_datewise_color(tests)
        
        fig = px.timeline(x_start=tests["datetime"], x_end=tests["datetime"] + timedelta(days=30), y = tests["Test"], 
                          title="Scheduled Test Programs", color=tests["color"], color_discrete_map=dict(zip(tests["color"], tests["color"])),
                         )
        fig.update_layout(showlegend=False)
        
        st.plotly_chart(fig)
    
    with middle_columns[1]:
        st.markdown(
            """
            <style>
                .stProgress > div > div > div > div  {
                    background-color: #ff4b4b;
                }

            </style>
            """,
            unsafe_allow_html=True,
        )
        tests["TestConf"] = [0.374540, 0.950714, 0.731994, 0.598658, 0.156019, 0.155995]
        st.markdown("<h6>Test Confidence Scores</h6>", True)
        for i, score in enumerate(tests["TestConf"]):
            st.progress(value=score, text=tests.iloc[i]["Test"] + f"\n\t\t{score*100}%")
        
        # st.dataframe(tests["TestConf"], 
        #              column_config = { "TestConf":
        #                  st.column_config.ProgressColumn("Test Confidence Scores", 
        #                                                  help="Confidence scores for the scheduled tests", min_value=0.0, max_value=1.0,
        #                                                  width="large"
        #                                                  )
        #                 },
        #              hide_index=True,
                     
        #             )

    # middle_cols = st.columns(1)


# def plot1():
    


def treemaps():
    df = pd.read_csv("reports\SystemArchitecture.csv", index_col=0)
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
