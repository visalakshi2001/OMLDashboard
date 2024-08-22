import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts
import plotly.express as px
import plotly.graph_objects as go
import itertools

import graphviz


# seperate the relationship arrows by type or color
# hide detectfault
# python script checks the test conflicts and other conflicts

def sysarcfunc():

    top_cols = st.columns([2.5,1.5])

    with top_cols[0]:
        # systemarc_sankey("System Architechture")
        function = pd.read_csv("reports/FunctionalArchitecture.csv", index_col=0)
        system = pd.read_csv("reports/Query2_SystemArchitecture.csv", index_col=0)
        environment = pd.read_csv("reports/Environment.csv", index_col=0)
        mission = pd.read_csv("reports/Query1_MissionArchitecture.csv", index_col=0)
        moe = pd.read_csv("reports/Query4_MOEs.csv", index_col=0)

        graphchoice = st.selectbox("Select view", ["Functional Architechture", "System Architechture", "Missions",
                                                             "MOE", "Environments"],
                                   index=0)

        dot = graphviz.Digraph(comment='Hierarchy', strict=True)
        
        if graphchoice == "Functional Architechture":
            for index, row in function.iterrows():
                func = row['Function']
                super_func = row['SuperFunction']
                allocated_to = row['AllocatedTo']
                
                # Add the function node
                dot.node(func)
                
                # Add edge from SuperFunction to Function if SuperFunction exists
                if pd.notna(super_func):
                    dot.edge(func, super_func, arrowhead="diamond")
                
                # Add AllocatedTo node and edge if it doesn't already exist
                if pd.notna(allocated_to):
                    if allocated_to not in dot.body:
                        dot.node(allocated_to, shape='box')
                    dot.edge(func, allocated_to)
            st.graphviz_chart(dot, True)
        
        elif graphchoice == "System Architechture":
            for index, row in system.iterrows():
                sys = row["SystemName"]
                subsys = row["SubsystemName"]
                subsubsys = row["SubsubsystemName"]

                if pd.notna(sys):
                    dot.node(sys)

                if pd.notna(subsys):
                    if subsys not in dot.body:
                        dot.node(subsys)
                    if pd.notna(sys):
                        dot.edge(sys, subsys, label="has subsystem")
                
                if pd.notna(subsubsys):
                    if subsubsys not in dot.body:
                        dot.node(subsubsys, shape="box")
                    if pd.notna(subsys):
                        dot.edge(subsys, subsubsys, label="has subsubsystem")  
            st.graphviz_chart(dot, True)
        
        elif graphchoice == "Environments":
            for index, row in environment.iterrows():
                mission = row["Mission"]
                env = row["Environment"]
                entity = row["EnvironmentalEntity"]

                dot.node(mission)

                if pd.notna(env):
                    dot.edge(mission, env)
                if pd.notna(entity):
                    dot.edge(env, entity, arrowhead="diamond")
            st.graphviz_chart(dot, True)
        
        elif graphchoice == "Missions":
            for index, row in  mission.iterrows():
                program = row["ProgramName"]
                missname = row["MissionName"]
                misscomp = row["MissionComponentName"]
                subsys = row["SubsystemName"]

                dot.node(program)

                if pd.notna(missname):
                    if missname not in dot.body:
                        dot.node(missname, shape="box")
                    dot.edge(program, missname, label="has mission")
                if pd.notna(misscomp):
                    dot.node(misscomp, shape="box")
                    dot.edge(missname, misscomp, arrowhead="diamond", label="has component")
                if pd.notna(subsys):
                    dot.edge(misscomp, subsys, arrowhead="vee", label="has subsystem")
            st.graphviz_chart(dot, True)
        
        elif graphchoice == "MOE":
            for index, row in moe.iterrows():
                missname = row["MissionName"]
                moename = row["MOEName"]

                dot.node(missname)

                if pd.notna(moename):
                    dot.edge(missname, moename, label="has moe")
            st.graphviz_chart(dot, True)
        
        # st.dataframe(moe)

    
    with top_cols[1]:
        roles = pd.read_csv("reports/Responsibilities.csv", index_col=0)
        resultsdocument = pd.read_csv("reports/DocumentSearch.csv", index_col=0)

        st.markdown("<h6>Assigned Responsibilities</h6>", True)
        st.dataframe(roles,hide_index=True)

        st.markdown("<h6>Test Data Results</h6>", True)

        metricchoice = st.selectbox("Select Test Data Document", options=["Payload Test Data Report"], index=0)

        if metricchoice == "Payload Test Data Report":
            metriccols = st.columns([1, 1.5, 1.5], gap="small") 
            for index,row in resultsdocument.iterrows():
                with metriccols[index]:
                    value = str(row["Value"]) + " " + str(row["Unit"]) if (pd.isna(row["Unit"]) != True) else str(row["Value"])
                    st.metric(label=row["TestData"], value=value, delta=row["TestDataSubject"], help="Test, followed by result value for given test subject")

        st.write(
            """
            <style>
            [data-testid="stMetricDelta"] svg {
                display: none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )




