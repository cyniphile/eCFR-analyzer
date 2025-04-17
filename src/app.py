import streamlit as st
from title_changes import page2
from word_counts import page1


st.set_page_config(page_title="Title Changes Analyzer", layout="wide")


def page3():
    st.write("This is the home page")


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
