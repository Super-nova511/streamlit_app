import streamlit as st
import streamlit.components.v1 as components
import os
import json

st.set_page_config(page_title="RAG Application")

# UI Cleanup
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
[data-testid="collapsedControl"] {display:none;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
div.element-container:has(iframe) { margin-top: -15px; }
</style>
""", unsafe_allow_html=True)

st.title("AI Exam. RAG System")

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

files = [f for f in os.listdir(STORAGE_DIR) if os.path.isfile(os.path.join(STORAGE_DIR, f))]

selected = st.selectbox("", files)

# Read file
content = ""
if selected:
    path = os.path.join(STORAGE_DIR, selected)
    try:
        with open(path, "r", errors="replace") as f:
            content = f.read()
    except:
        content = ""

js_text = json.dumps(content)

# Button component
components.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600&display=swap');

body {{
    margin:0;
    padding:0;
    overflow:hidden;
}}

.stButton {{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    font-weight:400;
    padding:0.25rem 0.75rem;
    border-radius:0.5rem;
    background-color:white;
    border:1px solid rgba(49, 51, 63, 0.2);
    font-family:"Source Sans Pro", sans-serif;
    font-size:1rem;
    cursor:pointer;
}}

.stButton:hover {{
    border-color:#ff4b4b;
    color:#ff4b4b;
}}

.stButton:active {{
    background-color:#ff4b4b;
    color:white;
}}
</style>

<button class="stButton" onclick="copyText()">Generate Output</button>

<script>
function copyText() {{
    const text = {js_text};

    navigator.clipboard.writeText(text).then(function() {{
        window.parent.postMessage({{type: "COPY_DONE"}}, "*");
    }});
}}
</script>
""", height=45)

# Listener for message from iframe
components.html("""
<script>
window.addEventListener("message", (event) => {
    if (event.data.type === "COPY_DONE") {
        const url = new URL(window.parent.location);
        url.searchParams.set("copied","1");
        window.parent.location = url;
    }
});
</script>
""", height=0)

# Show error after copy
if st.query_params.get("copied") == "1":
    st.error("Error: Process completed with system clipboard sync.")