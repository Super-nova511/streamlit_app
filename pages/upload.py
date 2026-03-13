import streamlit as st
import os

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
[data-testid="collapsedControl"] {display: none;}
</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="RAG Application",
    layout="centered"
)

st.title("RAG Application")
st.write("Upload files to test the retrieval system.")

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

uploaded_files = st.file_uploader(
    "Upload files",
    accept_multiple_files=True
)

if st.button("Create Vector DB"):

    if not uploaded_files:
        st.warning("Please upload at least one file.")

    else:
        for file in uploaded_files:
            path = os.path.join(STORAGE_DIR, file.name)
            
            with open(path, "wb") as f:
                f.write(file.getbuffer())

        st.success("Vectorization successful")
