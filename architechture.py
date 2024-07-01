import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts
import plotly.express as px
import plotly.graph_objects as go
import itertools


def sysarcfunc():

    top_cols = st.columns([3,1])

    with top_cols[0]:
        systemarc_sankey("System Architechture")

def systemarc_sankey(plot_title = "Graph of System Architechture"):
    system = pd.read_csv("reports/SystemArchitecture.csv", index_col=0)
    function = pd.read_csv("reports/FunctionalArchitecture.csv", index_col=0)
    mission = pd.read_csv("reports/Mission.csv", index_col=0)
    missionenv = pd.read_csv("reports/Environment.csv", index_col=0)

    dfs = [system, function.drop(columns=["SuperFunction"]), mission, missionenv]
    customnames = ["System", "AssignedFunctions", "Mission", "Environment"]

    links = []
    name = 0
    posx, posy = 1, 1
    for df in dfs:
        for prevcol, nextcol in itertools.combinations(df.columns, r=2):
            links.extend([{"source": x, "target": y, "value": 1, "customname": customnames[name], "posx": posx/5, "posy": (posy := posy-.1)} 
                          for x,y in zip(df[prevcol], df[nextcol]) if (pd.isna(x) or pd.isna(y)) != True])
            posy = 1
        name += 1
        posx += 1
        
    
    df = pd.DataFrame(links).drop_duplicates()
    nodes = np.unique(df[["source","target"]], axis=None)
    nodes = pd.Series(index=nodes, data=range(len(nodes)))

    min_posx = {node: float('inf') for node in nodes.index}
    min_posy = {node: float('inf') for node in nodes.index}
    customnames = {node: "" for node in nodes.index}
    for index, row in df.iterrows():
        min_posx[row['source']] = min(min_posx[row['source']], row['posx'])
        min_posx[row['target']] = min(min_posx[row['target']], row['posx'])

        min_posy[row['source']] = min(min_posy[row['source']], row['posy'])
        min_posy[row['target']] = min(min_posy[row['target']], row['posy'])

        if customnames[row["source"]] == "":
            customnames[row["source"]] = row["customname"]
        if customnames[row["target"]] == "":
            customnames[row["target"]] = row["customname"]

    fig = go.Figure(
        go.Sankey(
            arrangement = "snap",
            node = dict(
                pad = 15,
                thickness = 15,
                line = dict(color = "black", width = 0.5),
                label = nodes.index,
                x = [min_posx[node] for node in nodes.index],
                y = [min_posy[node] for node in nodes.index],
                customdata = list(customnames.values()),
                hovertemplate = "Belongs to %{customdata}",
                # color = "blue",
                align = "right"
            ),
            link = dict(
                # arrowlen=15,
                source =  nodes.loc[df["source"]],
                target =  nodes.loc[df["target"]],
                value =  df["value"],
                label =  (df["source"] + " to " + df["target"]).tolist(),
                customdata = df["customname"],
                # color =  "rgba(30,30,30,.3)",
                hovertemplate = "\n %{customdata}    \
                                \n %{label}"
            )
        )
    )

    fig.update_layout(
        font_size=14,
        title = plot_title,

    )

    st.plotly_chart(fig, use_container_width=True)

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