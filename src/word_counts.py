import streamlit as st
import plotly.express as px
import pandas as pd
from scripts import word_count
from utils import data_dir

# Set page config
st.set_page_config(layout="wide", page_title="Agency Word Count")


df = pd.read_csv(data_dir / "agencies_word_count.csv")


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
    # title=f"Word Count Treemap",
    color="value",
    color_continuous_scale="Blues",
    hover_data=["short_name"],
)

# Update layout and traces
fig.update_layout(
    height=700,
    margin=dict(l=10, r=10, t=30, b=10),
)

fig.update_traces(
    hovertemplate="<b>%{label}</b><br>Short Name: %{customdata[0]}<br>Word Count: %{value:,.0f}<extra></extra>",
    texttemplate="<b>%{label}</b><br>%{value:,.0f} words",
)

# Display the treemap
st.plotly_chart(fig, use_container_width=True)
