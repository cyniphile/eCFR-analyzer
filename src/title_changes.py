import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import json
import os
from scripts.download_versions import RAW_VERSIONS_PATH
from st_files_connection import FilesConnection

# TODO: add filters for removals and "substantive"
# TODO: map to agency
# TODO: seems like changes before this are not properly recorded in the eCFR
MIN_DATE = datetime(2017, 1, 3)


def page2():
    conn = st.connection("s3", type=FilesConnection)
    st.markdown(
        "Select options to visualize changes in title content over time. In the table below, click on the Links to see the actual changes to the text."
    )

    # Sidebar for controls
    st.sidebar.header("📋 Controls")

    def find_title_files():
        title_files = []
        for i in range(1, 50):
            file_path = RAW_VERSIONS_PATH / f"title_{i}_changes.json"
            if os.path.exists(file_path):
                title_files.append(i)
        return title_files

    REMOVED_BASE_URL_TEMPLATE = (
        "https://www.ecfr.gov/on/current/title-{title_number}/section-{section_number}"
    )

    def create_link(row):
        subpart = row["subpart"]
        title = row["title"].split("Title ")[1]

        date = row["date"]
        removed = row["removed"]
        if removed:
            return REMOVED_BASE_URL_TEMPLATE.format(
                title_number=title,
                section_number=row["identifier"],
            )
        today = (datetime.strptime(date, "%Y-%m-%d") - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        if subpart:
            return "https://www.ecfr.gov/compare/{date}/to/{today}/title-{title}/part-{part}/subpart-{subpart}/section-{section}".format(
                title=title,
                today=today,
                part=row["part"],
                date=date,
                subpart=subpart,
                section=row["identifier"],
            )
        else:
            return "https://www.ecfr.gov/compare/{date}/to/{today}/title-{title}/part-{part}/section-{section}".format(
                removed=removed,
                today=today,
                title=title,
                date=date,
                part=row["part"],
                section=row["identifier"],
            )

    @st.cache_data
    def load_data(title_number):
        data = conn.read(
            f"luke-ecfr-analyzer/title_changes/title_{title_number}_changes.json",
            input_format="json",
            ttl=600,
        )

        # TODO: use env vars to use local files in dev
        # file_path = RAW_VERSIONS_PATH / f"title_{title_number}_changes.json"
        # with open(file_path, "r") as file:
        #     data = json.load(file)

        df = pd.DataFrame(data["content_versions"])
        df["issue_date"] = pd.to_datetime(df["issue_date"])
        df["filter_date"] = pd.to_datetime(df["date"])
        df = df[df["filter_date"] >= MIN_DATE]
        df.drop(columns=["filter_date"], inplace=True)
        df["title"] = f"Title {title_number}"
        df["link"] = df.apply(
            create_link,
            axis=1,
        )

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
        dfs = [load_data(int(title.split(" ")[1])) for title in selected_titles]
        if len(dfs):
            all_dfs = pd.concat(dfs)
        else:
            all_dfs = pd.DataFrame()

        if not all_dfs.empty:
            min_date = all_dfs["issue_date"].min().date()
            max_date = all_dfs["issue_date"].max().date()

            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )

            try:
                if isinstance(date_range, tuple):
                    start_date, end_date = date_range  # type: ignore
                else:
                    start_date = end_date = date_range
            except ValueError:
                st.error("Invalid date range selected.")
                start_date = min_date
                end_date = max_date

            filtered_df = all_dfs[
                (all_dfs["issue_date"].dt.date >= start_date)
                & (all_dfs["issue_date"].dt.date <= end_date)
            ]

            aggregation_options = ["Day", "Week", "Month", "Year"]
            selected_aggregation = st.sidebar.selectbox("Select Aggregation", aggregation_options)

            aggregation_map = {"Day": "D", "Week": "W", "Month": "M", "Quarter": "Q", "Year": "Y"}

            period_str = aggregation_map[selected_aggregation]

            filtered_df["Period"] = filtered_df["issue_date"].dt.to_period(period_str).astype(str)

            changes_df = filtered_df.groupby(["Period", "title"]).size().reset_index(name="Changes")

            fig = px.line(
                changes_df,
                x="Period",
                y="Changes",
                color="title",
                markers=True,
                title=f"Changes Over Time Grouped by {selected_aggregation}s.",
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

            st.dataframe(
                filtered_df.drop(
                    columns=[
                        "Period",
                        "issue_date",
                        "identifier",
                        "amendment_date",
                        "part",
                        "subpart",
                        "type",
                    ]
                ),
                column_config={
                    "link": st.column_config.LinkColumn(),
                },
                hide_index=True,
            )

        else:
            st.warning("No data available for the selected range or titles.")
