# library_manager.py
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="My Library", page_icon="Books", layout="wide")
st.title("Personal Library Manager")
st.markdown("---")

# File to save data
DATA_FILE = "library.csv"

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Title", "Author", "Genre", "Year", "Pages", "Read"])

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Initialize
if 'df' not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# Sidebar - Add Book
with st.sidebar:
    st.header("Add New Book")
    with st.form("add_book"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Sci-Fi", "Romance", "Thriller", "Biography", "Self-Help", "Other"])
        year = st.number_input("Year", min_value=1000, max_value=2025, value=2025)
        pages = st.number_input("Pages", min_value=1, value=100)
        submitted = st.form_submit_button("Add Book")
        if submitted and title and author:
            new_book = pd.DataFrame([{
                "Title": title, "Author": author, "Genre": genre,
                "Year": year, "Pages": pages, "Read": False
            }])
            st.session_state.df = pd.concat([st.session_state.df, new_book], ignore_index=True)
            save_data(st.session_state.df)
            st.success("Book added!")

# Main Tabs
tab1, tab2, tab3 = st.tabs(["All Books", "Search", "Stats"])

with tab1:
    if df.empty:
        st.info("No books yet. Add one from sidebar!")
    else:
        # Edit Read status
        edited_df = st.data_editor(
            df,
            column_config={
                "Read": st.column_config.CheckboxColumn("Read?", default=False)
            },
            num_rows="dynamic",
            use_container_width=True
        )
        if st.button("Save Changes"):
            st.session_state.df = edited_df
            save_data(edited_df)
            st.success("Library updated!")

        # Delete selected
        if st.button("Delete Selected Rows"):
            selected = st.session_state.get("selected_rows", [])
            if selected:
                st.session_state.df = df.drop(selected).reset_index(drop=True)
                save_data(st.session_state.df)
                st.success("Deleted!")
                st.rerun()

with tab2:
    search = st.text_input("Search by Title or Author")
    if search:
        results = df[df["Title"].str.contains(search, case=False) | df["Author"].str.contains(search, case=False)]
        if not results.empty:
            st.write(results)
        else:
            st.warning("No books found.")

with tab3:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Books", len(df))
    with col2:
        st.metric("Read", len(df[df["Read"] == True]))
    with col3:
        st.metric("Unread", len(df[df["Read"] == False]))

    if not df.empty:
        st.bar_chart(df["Genre"].value_counts())

# Export
if not df.empty:
    csv = df.to_csv(index=False).encode()
    st.download_button("Download Library (CSV)", csv, "my_library.csv", "text/csv")

st.markdown("---")
st.caption("Made with Streamlit | Save data locally | No login needed")