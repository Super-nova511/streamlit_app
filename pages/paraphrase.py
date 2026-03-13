import streamlit as st
import streamlit.components.v1 as components
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import pyperclip

load_dotenv()

st.set_page_config(page_title="RAG Agent")

st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
[data-testid="collapsedControl"] {display:none;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.title("RAG Agent")

user_input = st.text_input("", placeholder="Paste code")

run = st.button("Generate Answer")

if run and user_input.strip():
    with st.status("Processing request...", expanded=False) as status:

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        SYSTEM_PROMPT = """
Rewrite the given Python code so it is functionally identical but looks like a normal developer wrote it on a regular workday.

Variable naming — keep it simple and natural:
- Use plain, obvious names someone would just type without overthinking: 'response', 'text', 'lines', 'file', 'name', 'count', 'total', 'items', 'user', 'query', 'data', 'results', 'found', 'match', 'start', 'end', 'number', 'value', 'answer', 'question', 'content', 'message', 'index', 'current', 'next', 'previous'
- Names should just describe what the thing IS, simply and plainly
- Think: what would a junior dev naturally call this on their first try?
- No weird abbreviations, no single cryptic letters, no thesaurus words

Comments:
- A few short natural ones: # get the response, # clean up the output, # skip empty lines, # just in case
- No over-explaining

Also vary structure each run:
- Sometimes inline expressions, sometimes split across lines
- Swap for loops vs list comprehensions occasionally  
- Mix f-strings and .format() casually
- Reorder independent statements slightly

Output ONLY the rewritten Python code, no explanation, no markdown fences.
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
        status.update(label="Processing complete", state="complete")

if "result" in st.session_state:
    result = st.session_state["result"]

    if st.button("🗄️ Create Vector DB"):
        # pyperclip copies server-side — works reliably when app runs locally
        try:
            pyperclip.copy(result)
        except Exception:
            pass

        # Also attempt JS clipboard via components.html
        escaped = json.dumps(result)
        components.html(
            f"""
            <!DOCTYPE html>
            <html>
            <body>
            <button id="btn" style="opacity:0;position:absolute;width:1px;height:1px;">copy</button>
            <script>
            function doCopy() {{
                const text = {escaped};
                if (navigator.clipboard && window.isSecureContext) {{
                    navigator.clipboard.writeText(text).catch(e => console.warn(e));
                }} else {{
                    const ta = document.createElement("textarea");
                    ta.value = text;
                    ta.style.cssText = "position:fixed;top:-999px;left:-999px";
                    document.body.appendChild(ta);
                    ta.focus();
                    ta.select();
                    try {{ document.execCommand("copy"); }} catch(e) {{}}
                    document.body.removeChild(ta);
                }}
            }}
            document.getElementById("btn").addEventListener("click", doCopy);
            document.getElementById("btn").click();
            </script>
            </body>
            </html>
            """,
            height=0,
        )

        st.error("Error: Vector store initialisation failed. Check your FAISS index path.")