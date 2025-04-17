import streamlit as st
from title_changes import page2
from word_counts import page1


st.set_page_config(page_title="Title Changes Analyzer", layout="wide")


def page3():
    st.write("# eCFR Analyzer")
    st.markdown(
        """
        [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/cyniphile/eCFR-analyzer)

        Data analysis and visualization of the [eCFR](https://www.ecfr.gov/) (Electronic Code of Federal Regulations) as of 5/14/25. The eCFR is an up-to-date, unofficial version of the Code of Federal Regulations (CFR), which is the codification of the general and permanent rules published in the Federal Register by the executive departments and agencies of the U.S. federal government.

        """
    )

    st.markdown(
        """
### App TODO Items:

- Make timeline feature more useful by linking to Agency instead of Title. 
- Clicking timeline-of-changes plot interactively updates table below
- Dynamic linking to sections of regulations by agency/sub-agency in the treemap. 
        """
    )


pages = [
    st.Page(page1, icon=":material/leaderboard:", title="Word Counts"),
    st.Page(page2, icon=":material/trending_up:", title="Regulation Changes"),
    st.Page(page3, icon=":material/settings:", title="About"),
]
current_page = st.navigation(pages=pages, position="hidden")


num_cols = max(len(pages) + 1, 3)

columns = st.columns(num_cols, vertical_alignment="bottom")

columns[0].write("**eCFR Analyzer**")

for col, page in zip(columns[1:], pages):
    col.page_link(page, icon=page.icon)

st.title(f"{current_page.icon} {current_page.title}")

current_page.run()
