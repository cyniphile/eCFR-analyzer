import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from download_versions import RAW_VERSIONS_PATH

st.set_page_config(page_title="Title Changes Analyzer", layout="wide")

st.title("📊 Title Changes Analyzer")
st.markdown("Select options to visualize changes in title content over time.")

# Sidebar for controls
st.sidebar.header("📋 Controls")


def find_title_files():
    title_files = []
    for i in range(1, 50):
        file_path = RAW_VERSIONS_PATH / f"title_{i}_changes.json"
        if os.path.exists(file_path):
            title_files.append(i)
    return title_files


@st.cache_data
def load_data(title_number):
    file_path = RAW_VERSIONS_PATH / f"title_{title_number}_changes.json"
    with open(file_path, "r") as file:
        data = json.load(file)

    df = pd.DataFrame(data["content_versions"])
    df["issue_date"] = pd.to_datetime(df["issue_date"])
    df["title"] = f"Title {title_number}"
    return df


title_numbers = find_title_files()

if not title_numbers:
    st.warning("No title files found.")
else:
    selected_titles = st.sidebar.multiselect(
        "Select Titles",
        [f"Title {num}" for num in title_numbers],
        default=[f"Title {title_numbers[0]}"],
    )

    all_dfs = pd.concat([load_data(int(title.split(" ")[1])) for title in selected_titles])

    if not all_dfs.empty:
        min_date = all_dfs["issue_date"].min().date()
        max_date = all_dfs["issue_date"].max().date()

        date_range = st.sidebar.date_input(
            "Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date
        )

        if isinstance(date_range, tuple):
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range

        filtered_df = all_dfs[
            (all_dfs["issue_date"].dt.date >= start_date)
            & (all_dfs["issue_date"].dt.date <= end_date)
        ]

        aggregation_options = ["Day", "Week", "Month", "Quarter", "Year"]
        selected_aggregation = st.sidebar.selectbox("Select Aggregation", aggregation_options)

        aggregation_map = {"Day": "D", "Week": "W", "Month": "M", "Quarter": "Q", "Year": "Y"}

        period_str = aggregation_map[selected_aggregation]

        filtered_df["Period"] = filtered_df["issue_date"].dt.to_period(period_str).astype(str)

        changes_df = filtered_df.groupby(["Period", "title"]).size().reset_index(name="Changes")

        st.subheader(f"Changes Over Time")

        fig = px.line(
            changes_df,
            x="Period",
            y="Changes",
            color="title",
            markers=True,
            title=f"Changes Over Time Grouped by {selected_aggregation}s",
        )

        fig.update_layout(
            xaxis_title=selected_aggregation,
            yaxis_title="Number of Changes",
            hovermode="closest",
            height=600,
        )

        selected_point = st.plotly_chart(fig, use_container_width=True)

        # Hover functionality
        hover_data = st.empty()

        def update_hover(trace, points, state):
            if points.point_inds:
                period = points.xs[0]
                title = trace.name
                details = filtered_df[
                    (filtered_df["Period"] == period) & (filtered_df["title"] == title)
                ]
                hover_data.dataframe(details[["section", "issue_date"]].reset_index(drop=True))


        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Changes", len(filtered_df))
        with col2:
            st.metric(
                f"Average Changes per {selected_aggregation}",
                round(changes_df["Changes"].mean(), 2),
            )
        with col3:
            st.metric("Date Range", f"{start_date} to {end_date}")

        st.dataframe(filtered_df)

    else:
        st.warning("No data available for the selected range or titles.")
