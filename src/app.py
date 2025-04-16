import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
from pathlib import Path
from download_versions import RAW_VERSIONS_PATH

st.set_page_config(page_title="Title Changes Analyzer", layout="wide")

st.title("📊 Title Changes Analyzer")
st.markdown("Select options to visualize changes in title content over time.")

# Sidebar for controls
st.sidebar.header("📋 Controls")


# Find all title JSON files
def find_title_files():
    """Find all title_X_changes.json files in the specified directory"""
    title_files = []
    # Assuming files are in the current directory or a specific path
    # Update RAW_VERSIONS_PATH to your actual path if needed

    for i in range(1, 50):  # Up to 50 titles as in your original code
        file_path = RAW_VERSIONS_PATH / f"title_{i}_changes.json"
        if os.path.exists(file_path):
            title_files.append((i, f"Title {i}"))

    return title_files


# Function to load and process data
@st.cache_data
def load_data(title_number):
    """Load and process data for a specific title number"""
    file_path = RAW_VERSIONS_PATH / f"title_{title_number}_changes.json"

    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        # Convert to DataFrame
        df = pd.DataFrame(data["content_versions"])

        # Convert 'issue_date' to datetime
        df["issue_date"] = pd.to_datetime(df["issue_date"])

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


# Get available title files
title_files = find_title_files()

if not title_files:
    st.warning("No title files found. Please check the file path and naming convention.")
else:
    # Title selection
    title_options = [f"Title {i}" for i, _ in title_files]
    selected_title_display = st.sidebar.selectbox("Select Title", title_options)
    selected_title_number = int(selected_title_display.split(" ")[1])

    # Load data for selected title
    df = load_data(selected_title_number)

    if df is not None and not df.empty:
        # Date range selection
        min_date = df["issue_date"].min().date()
        max_date = df["issue_date"].max().date()

        date_range = st.sidebar.date_input(
            "Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date
        )

        # Handle single date selection
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range

        # Filter data by date range
        filtered_df = df[
            (df["issue_date"].dt.date >= start_date) & (df["issue_date"].dt.date <= end_date)
        ]

        # Aggregation options
        aggregation_options = ["Day", "Week", "Month", "Quarter", "Year"]
        selected_aggregation = st.sidebar.selectbox("Select Aggregation", aggregation_options)

        # Map selected aggregation to pandas period strings
        aggregation_map = {"Day": "D", "Week": "W", "Month": "M", "Quarter": "Q", "Year": "Y"}

        if not filtered_df.empty:
            # Group by selected aggregation and count changes
            period_str = aggregation_map[selected_aggregation]
            changes_over_time = filtered_df.groupby(
                filtered_df["issue_date"].dt.to_period(period_str)
            ).size()

            # Convert to DataFrame for plotting
            changes_df = changes_over_time.reset_index()
            changes_df.columns = ["Period", "Changes"]

            # Convert period to string for Plotly
            changes_df["Period"] = changes_df["Period"].astype(str)

            # Create plot
            st.subheader(f"Changes Over Time - {selected_title_display}")

            fig = px.line(
                changes_df,
                x="Period",
                y="Changes",
                markers=True,
                title=f"Changes Over Time Grouped by {selected_aggregation}s",
            )

            fig.update_layout(
                xaxis_title=selected_aggregation,
                yaxis_title="Number of Changes",
                hovermode="x unified",
                height=600,
            )

            st.plotly_chart(fig, use_container_width=True)

            # Display data statistics
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

            # Display raw data if requested
            if st.checkbox("Show Raw Data"):
                st.dataframe(filtered_df)
        else:
            st.warning("No data available for the selected date range.")
    else:
        st.error(f"Failed to load data for {selected_title_display} or the data is empty.")
