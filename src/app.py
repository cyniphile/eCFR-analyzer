import streamlit as st
from changes import page2


st.set_page_config(page_title="Title Changes Analyzer", layout="wide")


def page1():
    st.write("This is the home page")


def page3():
    st.write("This is the settings page")


def page4():
    st.write("This is the map page")


pages = [
    st.Page(page1, icon=":material/home:", title="Home"),
    st.Page(page2, icon=":material/filter:", title="Filter"),
    st.Page(page3, icon=":material/settings:", title="Settings"),
    st.Page(page4, icon=":material/map:", title="Map"),
]
current_page = st.navigation(pages=pages, position="hidden")


num_cols = max(len(pages) + 1, 8)

columns = st.columns(num_cols, vertical_alignment="bottom")

columns[0].write("**My App Name**")

for col, page in zip(columns[1:], pages):
    col.page_link(page, icon=page.icon)

st.title(f"{current_page.icon} {current_page.title}")

current_page.run()
