import streamlit as st
import plotly.express as px
import pandas as pd
from utils import app_data_dir


def page1():
    # Custom CSS to improve fonts
    st.markdown(
        """
    <style>
        .main .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3 {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-weight: 600;
        }
        h1 {
            font-size: 3.5rem !important;
            margin-bottom: 1rem;
        }
        p, li, div {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 1.1rem !important;
        }
        .stPlotlyChart {
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    df = pd.read_csv(app_data_dir / "agencies_word_count.csv")

    # Function to prepare the data for Plotly treemap
    def prepare_treemap_data(df):
        # Create a new dataframe for the treemap
        treemap_data = []

        # First, add the root node
        treemap_data.append(
            {
                "id": "All Agencies",
                "parent": "",
                "name": "All Agencies",
                "short_name": "",
                "value": df["word_count"].sum(),
            }
        )

        # Add parent organizations (those where name == parent_agency)
        parent_orgs = df[df["name"] == df["parent_agency"]]
        parent_word_counts = df.groupby("parent_agency")["word_count"].sum().to_dict()

        for _, row in parent_orgs.iterrows():
            treemap_data.append(
                {
                    "id": row["name"],
                    "parent": "All Agencies",
                    "name": row["display_name"] if pd.notna(row["display_name"]) else row["name"],
                    "value": parent_word_counts[row["name"]],
                    "short_name": row["short_name"] if pd.notna(row["short_name"]) else "",
                    "org_type": "parent",
                }
            )

        # Add child organizations (those where name != parent_agency)
        child_orgs = df[df["name"] != df["parent_agency"]]
        for _, row in child_orgs.iterrows():
            treemap_data.append(
                {
                    "id": row["name"],
                    "parent": row["parent_agency"],
                    "name": row["display_name"] if pd.notna(row["display_name"]) else row["name"],
                    "value": row["word_count"],
                    "short_name": row["short_name"] if pd.notna(row["short_name"]) else "",
                    "org_type": "child",
                }
            )

        return pd.DataFrame(treemap_data)

    # Title and description
    st.title("Agencies Word Count Treemap")
    st.write("Organizations sized by word count. Click on an organization to drill down.")

    # Prepare the treemap data
    treemap_df = prepare_treemap_data(df)
    filtered_df = treemap_df

    # Create the treemap
    fig = px.treemap(
        filtered_df,
        ids="id",
        names="name",
        parents="parent",
        values="value",
        color="value",
        color_continuous_scale="Blues",
        hover_data=["short_name"],
    )

    # Update layout and traces with improved typography
    fig.update_layout(
        height=700,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(
            family="Helvetica Neue, Arial, sans-serif",
            size=16,  # Increased base font size
        ),
        coloraxis_colorbar=dict(
            tickfont=dict(size=16),
            # The title needs to be set using 'title' with nested 'text' and 'font' properties
            title=dict(text="Word Count", font=dict(size=18)),
        ),
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Short Name: %{customdata[0]}<br>Word Count: %{value:,.0f}<extra></extra>",
        texttemplate="<b>%{label}</b><br>%{value:,.0f} words",
        textfont=dict(
            family="Helvetica Neue, Arial, sans-serif",
            size=18,  # Increased text size within treemap boxes
        ),
        insidetextfont=dict(
            family="Helvetica Neue, Arial, sans-serif",
            size=18,  # Ensures text inside treemap boxes is also larger
        ),
    )

    # Display the treemap
    st.plotly_chart(fig, use_container_width=True)

    # Add a footer with additional information
    st.markdown(
        """
    ---
    ### About This Visualization
    This treemap visualizes the word count across different agencies. The size and color intensity of 
    each box represent the total word count. Parent organizations contain their child agencies.
    """
    )
