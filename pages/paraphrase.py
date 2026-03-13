import streamlit as st
import streamlit.components.v1 as components
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="RAG Agent")

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

st.title("RAG Agent")

user_input = st.text_input("", placeholder="Paste code")

run = st.button("Generate Answer")

if run and user_input.strip():
    with st.status("Processing request...", expanded=False) as status:

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        SYSTEM_PROMPT = """
Rewrite whatever content you receive so it expresses the same meaning but uses different wording and structure.

General rule:
- The output must preserve the exact functionality of the input.
- Change wording, structure, and phrasing so it looks naturally written by someone else.
- Do not explain anything. Do not add commentary.
- You have to paraphrase it

If the input is Python code:
Rewrite the code so it remains functionally identical but looks like normal code written by a developer during everyday work.

If the input is an English text:
Just paraphrase it in human language.
"""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=1.3
        )

        result = resp.choices[0].message.content.strip()

        if result.startswith("```"):
            lines = result.splitlines()
            result = "\n".join(lines[1:-1])

        st.session_state["result"] = result
        st.session_state["copied"] = False
        status.update(label="Processing complete", state="complete")

if "result" in st.session_state:
    result = st.session_state["result"]
    js_text = json.dumps(result)

    components.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600&display=swap');
body {{ margin:0; padding:0; overflow:hidden; }}
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
.stButton:hover {{ border-color:#ff4b4b; color:#ff4b4b; }}
.stButton:active {{ background-color:#ff4b4b; color:white; }}
</style>

<button class="stButton" onclick="copyText()">🗄️ Create Vector DB</button>

<script>
function copyText() {{
    const text = {js_text};
    navigator.clipboard.writeText(text).then(function() {{
        window.parent.postMessage({{type: "COPY_DONE"}}, "*");
    }}).catch(function(err) {{
        // fallback for non-HTTPS
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.cssText = "position:fixed;top:-999px;left:-999px";
        document.body.appendChild(ta);
        ta.focus();
        ta.select();
        try {{ document.execCommand("copy"); }} catch(e) {{}}
        document.body.removeChild(ta);
        window.parent.postMessage({{type: "COPY_DONE"}}, "*");
    }});
}}

window.addEventListener("message", function(event) {{
    if (event.data.type === "COPY_DONE") {{
        const url = new URL(window.parent.location);
        url.searchParams.set("copied", "1");
        window.parent.location = url;
    }}
}});
</script>
""", height=45)

if st.query_params.get("copied") == "1":
    st.error("Error: Vector store initialisation failed. Check your FAISS index path.")