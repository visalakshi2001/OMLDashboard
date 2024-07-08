import streamlit as st
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
        programs = pd.read_csv("reports/TestPrograms.csv", index_col=0)
        programs = pd.read_csv("reports/TestPrograms.csv", index_col=0)

        st.markdown("<h6>Scheduled Test Programs</h6>", True)
        metriccols = st.columns(4)
        for i,num in enumerate(programs["num_Tests"]):
            metriccols[i].metric(label=programs.iloc[i]["TestProgram"], value=num, delta=f"{num-2} Scheduled")

    with top_columns[1]:
        st.markdown("<h6>Issues</h6>", True)
        with st.container(border=True, height=150):
            st.warning('Four tests have overlapped scheduling', icon="⚠️",)
            st.error("TerrainTraversalExercise is colliding with other tests", icon="❗")
            st.error("PayloadDeploymentTest is colliding with other tests", icon="❗")
            st.error("MobilityDeploymentTest is colliding with other tests", icon="❗")
            st.error("AntennaDeploymentTest is colliding with other tests", icon="❗")

    middle_columns = st.columns([0.6, 0.4])
    with middle_columns[0]:
        tests = pd.read_csv("reports/TestProcedures.csv", index_col=0)
        tests = pd.read_csv("reports/TestProcedures.csv", index_col=0)
        tests["datetime"] = pd.to_datetime(tests["datetime"])
        tests = set_datewise_color(tests)
        
        fig = px.timeline(x_start=tests["datetime"], x_end=tests["datetime"] + timedelta(days=30), y = tests["Test"], 
                          title="Scheduled Test Programs", color=tests["color"], color_discrete_map=dict(zip(tests["color"], tests["color"])),
                         )
        vlinedate = datetime.today().date()
        fig.add_vline(x=datetime(vlinedate.year, vlinedate.month, vlinedate.day).timestamp() * 1000, annotation_text= f"today {vlinedate.month}/{vlinedate.day}")

        fig.update_layout(showlegend=False, yaxis={'title': None, 'visible': True, 'showticklabels': True})
        
        st.plotly_chart(fig, use_container_width=True)
    
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
        # for i, score in enumerate(tests["TestConf"]):
        #     st.progress(value=score, text=tests.iloc[i]["Test"] + f"$~~~~~~~~~~~$ **{np.round(score*100, decimals=1)}%**")
        
        st.dataframe(tests[["Test", "TestConf"]], 
                     column_config = { "TestConf":
                         st.column_config.ProgressColumn("Test Confidence Scores", 
                                                         help="Confidence scores for the scheduled tests", min_value=0.0, max_value=1.0,
                                                         width="large"
                                                         )
                        },
                     hide_index=True,
                     use_container_width=True,                     
                    )

    # middle_cols = st.columns(1)

