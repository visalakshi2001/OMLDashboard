import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from datetime import datetime, timedelta



def set_datewise_color(df):
    df["color"] = df['datetime'].duplicated(keep=False).map({True: '#ff4b4b', False: 'royalblue'})

    return df

def dashfunc():

    COLORS = px.colors.qualitative.Plotly

    st.subheader("Schedule", "Performance", divider="orange")

    top_columns = st.columns(2)

    with top_columns[0]:
        programs = pd.read_csv("reports/TestPrograms.csv", index_col=0)

        st.markdown("<h6>Scheduled Test Programs</h6>", True)
        metriccols = st.columns(4)
        for i,num in enumerate(programs["num_Tests"]):
            metriccols[i].metric(label=programs.iloc[i]["TestProgram"], value=num, delta=f"{num-2} Scheduled")

    with top_columns[1]:
        st.markdown("<h6>Issues</h6>", True)
        with st.container(border=True, height=150):
            st.warning('Four tests have overlapped scheduling (find more info on Issues tab)', icon="⚠️")
            

    middle_columns = st.columns([0.75, 0.25])
    with middle_columns[0]:
        testscheduling = pd.read_csv("reports/Query6_Scheduling 2.csv", index_col=0)
        testscheduling["Start"] = pd.to_datetime(testscheduling["Start"])
        testscheduling["End"] = pd.to_datetime(testscheduling["End"])

        # Define a function to extract the week of year
        testscheduling['Week'] = testscheduling['Start'].dt.strftime('%Y-W%U')

        # Creating the Plotly figure
        fig = px.timeline(testscheduling, x_start="Start", x_end="End", y="Site", color="VMName", text="VMName", hover_name="VM",
                        category_orders={"Site": sorted(testscheduling['Site'].unique(), key=lambda x: str(x))})

        
        # Update layout to include a dropdown menu for week selection
        week_options = testscheduling['Week'].unique()

        fig.update_layout(
            title="Test Site Schedule",
            xaxis_title="Time",
            yaxis_title="Test Site",
            xaxis=dict(
                tickformat="%d %b %Y\n%H:%M",
                range=[testscheduling['Start'].min() - pd.Timedelta(days=1), testscheduling['End'].min() + pd.Timedelta(days=6)],
            ),
            updatemenus=[{
                "buttons": [
                    {
                        "args": [
                            {"xaxis.range": [testscheduling[testscheduling['Week'] == week]['Start'].min(), testscheduling[testscheduling['Week'] == week]['End'].max()]}
                        ],
                        "label": week,
                        "method": "relayout"
                    }
                    for week in week_options
                ],
                "direction": "down",
                "showactive": True,
                "x": 0.17,
                "xanchor": "left",
                "y": 1.15,
                "yanchor": "top"
            }],
            legend=dict(xanchor="left", x=0, y=1, yanchor="bottom", orientation="h")
        )
        vlinedate = datetime.today().date()
        fig.add_vline(x=datetime(vlinedate.year, vlinedate.month, vlinedate.day).timestamp() * 1000, annotation_text= f"today {vlinedate.month}/{vlinedate.day}")
        st.plotly_chart(fig, use_container_width=True)
        # st.write("Add test subjects to the labels on the graph")
        # st.write("Raise issues when conflicting")
    
    with middle_columns[1]:
        tests = pd.read_csv("reports/TestProcedures.csv", index_col=0)
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
            st.progress(value=score, text=tests.iloc[i]["Test"] + f"$~~~~~~~~~~~$ **{np.round(score*100, decimals=1)}%**")
        
        # st.dataframe(tests[["Test", "TestConf"]], 
        #              column_config = { "TestConf":
        #                  st.column_config.ProgressColumn("Test Confidence Scores", 
        #                                                  help="Confidence scores for the scheduled tests", min_value=0.0, max_value=1.0,
        #                                                  width="large"
        #                                                  )
        #                 },
        #              hide_index=True,
        #              use_container_width=True,                     
        #             )


    st.subheader("Performance", divider="violet")

    middle_columns2 = st.columns([0.7, 0.3])

    with middle_columns2[0]:
        keycaprates = pd.read_csv("reports/Query5_KeyCapabilities 2.csv", index_col=0)
        keycaprates["UnitSymbols"] = keycaprates["Unit"].map({"percent": "%", "degrees": "deg", "second": "sec", "kilogram": "kg"})

        fig = go.Figure()
        for i in range(len(keycaprates["KCName"])):
            fig.add_trace(go.Scatter(
                x=[keycaprates["Threshold"][i], keycaprates["Objective"][i]],
                y=[keycaprates["KCName"][i], keycaprates["KCName"][i]],
                mode='lines',
                line=dict(color='gray'),
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=[keycaprates["Threshold"][i]],
                y=[keycaprates["KCName"][i]],
                mode='markers+text',
                marker=dict(size=10, color="blue"),
                name="Threshold" if i==0 else "",
                showlegend=(i==0),
                text=[f"{keycaprates['Threshold'][i]} {keycaprates['UnitSymbols'][i]}"],
                textposition="bottom center",
                hovertemplate=f" <b> Satisfied by:</b> {keycaprates['SatisfiedBy'][i]}" + ""
            ))
            fig.add_trace(go.Scatter(
                x=[keycaprates["Objective"][i]],
                y=[keycaprates["KCName"][i]],
                mode='markers+text',
                marker=dict(size=10, color="red"),
                name="Objective" if i==0 else "",
                showlegend=(i==0),
                text=[f"{keycaprates['Objective'][i]} {keycaprates['UnitSymbols'][i]}"],
                textposition="top center",
                hovertemplate=f" <b> Satisfied by:</b> {keycaprates['SatisfiedBy'][i]}" + ""
            ))
            # fig.add_annotation(x=keycaprates["Threshold"][i], y=keycaprates["KCName"][i], text=keycaprates["Threshold"][i].astype(str), 
            #                    yshift=10, showarrow=False)
            # fig.add_annotation(x=keycaprates["Objective"][i], y=keycaprates["KCName"][i], text=keycaprates["Objective"][i].astype(str), 
            #                    yshift=10, showarrow=False)
        
        fig.update_layout(title="Threshold vs Objective for Each Key Capacities",
                            xaxis_title="Value",
                            yaxis_title="KCName",
                            yaxis=dict(tickmode='linear'),
                            legend=dict(orientation="h", x=0.3, y=10))

        st.plotly_chart(fig, use_container_width=True)
    
    with middle_columns2[1]:
        keycaprates["VerificationStatus"] = np.where(pd.notnull(keycaprates["VerificationMethodName"]),  "Verified", "Unverified")
        
        fig = go.Figure(data=[
            go.Bar(name="Satisfied", y=keycaprates["KCName"], x=np.where(pd.notnull(keycaprates["SatisfiedBy"]), 1, 0),
                    orientation="h", marker=dict(color=COLORS[2]), text=keycaprates["SatisfiedBy"]),
            go.Bar(name="Verified", y=keycaprates["KCName"], x=np.where(pd.notnull(keycaprates["VerificationMethodName"]), 1, 0),
                    orientation="h",marker=dict(color=COLORS[0]), text=keycaprates["VerificationMethodName"])
        ])
        fig.update_layout(barmode="stack",
                            title="Key Capabilities Verification and Satisfaction Status")
        fig.update_traces(textposition="inside", textfont_size=16)
        fig.update_xaxes(showticklabels=False)
        st.plotly_chart(fig, True)

    
    decisionreview = pd.read_csv("reports/Query3_Decisions.csv", index_col=0)
    decisionreview['ReviewStart'] = pd.to_datetime(decisionreview['ReviewStart'])
    # Define ReviewEnd as 1 hour after ReviewStart (since no end times are given)
    decisionreview['ReviewEnd'] = decisionreview['ReviewStart'] + pd.Timedelta(hours=1)
    # Define a function to extract the week of year
    decisionreview['Week'] = decisionreview['ReviewStart'].dt.strftime('%Y-W%U')

    # Creating the Plotly figure
    fig = px.timeline(decisionreview, x_start="ReviewStart", x_end="ReviewEnd", y="Review", color="Decision", text="Milestone", hover_name="Milestone",
                    category_orders={"Review": sorted(decisionreview['Review'].unique(), key=lambda x: str(x))})

    # Update layout to include a dropdown menu for week selection
    week_options = decisionreview['Week'].unique()

    fig.update_layout(
        title="Review Schedule",
        xaxis_title="Time",
        yaxis_title="Review",
        # xaxis=dict(
        #     tickformat="%d %b %Y\n%H:%M",
        #     # range=[decisionreview['ReviewStart'].min() - pd.Timedelta(days=1), decisionreview['ReviewEnd'].min() + pd.Timedelta(days=6)],
        # ),
        updatemenus=[{
            "buttons": [
                {
                    "args": [
                        {"xaxis.range": [decisionreview[decisionreview['Week'] == week]['ReviewStart'].min() - pd.Timedelta(days=1), decisionreview[decisionreview['Week'] == week]['ReviewEnd'].max() + pd.Timedelta(days=6)]}
                    ],
                    "label": week,
                    "method": "relayout"
                }
                for week in week_options
            ],
            "direction": "down",
            "showactive": True,
            "x": 0.17,
            "xanchor": "left",
            "y": 1.15,
            "yanchor": "top"
        }]
    )
    st.plotly_chart(fig, True)
   

    heatmap_pivot = decisionreview.pivot_table(index='Milestone', columns='Review', aggfunc='size', fill_value=None)
    heatmap_pivot.mask(heatmap_pivot > 1, 1, inplace=True)

    # Create text for each cell
    decisionreview['Text'] = decisionreview.apply(lambda row: f"Decision: {row['Decision']}<br>Data: {row['Data']}<br>TestData: {row['TestData']}", axis=1)
    # text_pivot = decisionreview.pivot(index='Milestone', columns='Review', values='Text').fillna('')
    text_pivot = decisionreview[["Milestone", "Review", "Text"]].pivot_table(index="Milestone", columns="Review", values="Text", aggfunc=lambda x: "|".join(x.astype("str")))

    # Generate the heatmap
    fig = go.Figure(go.Heatmap(
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        z=heatmap_pivot.values,
        text=text_pivot.values,
        texttemplate="%{text}",
        textfont={"size": 16}
    ))

    # st.dataframe(decisionreview.pivot_table(index=['Milestone', "ReviewStart"], columns=['Review'], aggfunc='size', fill_value=None))
    # st.dataframe(heatmap_pivot)


    # Update layout
    fig.update_layout(
        title='Decision Review Data Grid',
        xaxis_title="Review",
        yaxis_title="Milestone",
        plot_bgcolor='white'
    )
    st.plotly_chart(fig, True)
    # st.dataframe(decisionreview)


##########################################################################################################
# REFERENCES  # 
#  hover templates: https://plotly.com/python/hover-text-and-formatting/ #
#  scatterplot annotations: https://stackoverflow.com/questions/71875067/adding-text-labels-to-a-plotly-scatter-plot-for-a-subset-of-points #
#   #
##########################################################################################################