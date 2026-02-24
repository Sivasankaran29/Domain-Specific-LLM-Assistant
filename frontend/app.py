import streamlit as st
import requests
import time

API = "http://localhost:8000"

st.set_page_config(page_title="Law Chatbot", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
section[data-testid="stSidebar"] {width:260px !important;}
.block-container {max-width:900px;margin:auto;}
.stChatMessage {padding:14px 18px;border-radius:14px;animation:fadeIn .2s;}
@keyframes fadeIn {from{opacity:0;}to{opacity:1;}}
textarea {border-radius:20px;border:1px solid #444;}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------ STATE ------------------
defaults = {
    "token": None,
    "email": None,
    "session_id": None,
    "sessions": [],
    "chat_history": []
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ------------------ LOGIN ------------------
if not st.session_state.token:
    st.title("⚖️ Law Chatbot")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1,col2 = st.columns(2)

    if col1.button("Login"):
        try:
            r = requests.post(f"{API}/auth/login",
                json={"email":email,"password":password})
            if r.status_code == 200:
                st.session_state.token = r.json()["token"]
                st.session_state.email = email
                st.rerun()
            else:
                st.error("Invalid login")
        except:
            st.error("Server error")

    if col2.button("Register"):
        try:
            r = requests.post(f"{API}/auth/register",
                json={"email":email,"password":password})
            if r.status_code == 200:
                st.session_state.token = r.json()["token"]
                st.session_state.email = email
                st.rerun()
            else:
                st.error("User exists")
        except:
            st.error("Server error")

    st.stop()

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown(f"**👤 {st.session_state.email}**")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.divider()

    if st.button("➕ New Chat"):
        st.session_state.session_id = None
        st.session_state.chat_history = []
        st.rerun()

    # load sessions
    try:
        r = requests.get(
            f"{API}/sessions",
            headers={"Authorization":f"Bearer {st.session_state.token}"}
        )
        if r.status_code == 200:
            st.session_state.sessions = r.json()["sessions"]
    except:
        pass

    st.markdown("### Chats")

    for s in st.session_state.sessions:
        title = s.get("title","Chat")
        if st.button(title, key=s["id"], use_container_width=True):
            st.session_state.session_id = s["id"]
            st.session_state.chat_history = []
            st.rerun()

# ------------------ TITLE ------------------
st.markdown("# ⚖️ Law Assistant")
st.caption("Indian legal informational AI")

chat_container = st.container()

# ------------------ LOAD HISTORY ------------------
if st.session_state.session_id:
    try:
        r = requests.get(
            f"{API}/history/{st.session_state.session_id}",
            headers={"Authorization":f"Bearer {st.session_state.token}"}
        )
        if r.status_code == 200:
            st.session_state.chat_history = r.json()["history"]
    except:
        pass

# ------------------ TYPEWRITER ------------------
def typewriter(text):
    placeholder = st.empty()
    out = ""
    for i in range(0,len(text),5):
        out += text[i:i+5]
        placeholder.markdown(out+"▌")
        time.sleep(0.01)
    placeholder.markdown(out)

# ------------------ RENDER ------------------
def render_response(resp):
    if resp["type"] == "refusal":
        st.warning(resp["data"]["message"])
        return

    d = resp["data"]

    answer = d.get("answer","")
    typewriter(answer)

    if d.get("relevant_laws"):
        st.markdown("**Relevant Laws**")
        for x in d["relevant_laws"]:
            st.markdown(f"- {x}")

    if d.get("general_process"):
        st.markdown("**Process**")
        st.markdown(d["general_process"])

    if d.get("disclaimer"):
        st.caption(d["disclaimer"])

# ------------------ DISPLAY CHAT ------------------
with chat_container:
    for item in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(item["question"])

        with st.chat_message("assistant"):
            render_response(item["response"])

# ------------------ INPUT ------------------
query = st.chat_input("Ask about Indian law...")

if query:
    with chat_container:
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            loader = st.empty()
            loader.markdown("▌")

    try:
        r = requests.post(
            f"{API}/chat",
            json={"session_id":st.session_state.session_id,"query":query},
            headers={"Authorization":f"Bearer {st.session_state.token}"},
            timeout=120
        )

        if r.status_code == 200:
            data = r.json()
            st.session_state.session_id = data["session_id"]

            with chat_container:
                with st.chat_message("assistant"):
                    loader.empty()
                    render_response(data["response"])

            st.session_state.chat_history.append({
                "question":query,
                "response":data["response"]
            })

        else:
            st.error("Server error")

    except:
        st.error("Connection failed")

# auto scroll
st.markdown("""
<script>
window.scrollTo(0, document.body.scrollHeight);
</script>
""", unsafe_allow_html=True)