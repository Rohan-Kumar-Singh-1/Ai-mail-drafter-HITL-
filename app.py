import streamlit as st
import uuid
from graph import graph
from database import *

from auth import login_page

# ---------------- LOGIN CHECK ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    init_db()
    login_page()
    st.stop()

init_db()

st.set_page_config(page_title="AI Email Agent", page_icon="📧")

# ---------------- SESSION ---------------- #

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    create_chat(chat_id, "New Email Chat", st.session_state.user_id)

chat_id = st.session_state.current_chat


# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    # ---------- ACCOUNT INFO ---------- #

    st.markdown("### 👤 Account")

    st.write(f"Logged in as: **{st.session_state.user}**")

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.user_id = None
        st.session_state.current_chat = None

        st.rerun()

    st.divider()

    # ---------- CHAT SECTION ---------- #

    st.title("💬 Chats")

    if st.button("➕ New Chat"):

        chat_id = str(uuid.uuid4())
        create_chat(chat_id, "New Email Chat", st.session_state.user_id)
        st.session_state.current_chat = chat_id

        st.rerun()

    st.divider()

    st.subheader("Chat History")

    chats = get_chats(st.session_state.user_id)

    for cid, title in chats:

        col1, col2 = st.columns([4,1])

        # Open chat
        with col1:
            if st.button(title, key=f"open_{cid}"):

                st.session_state.current_chat = cid
                st.rerun()

        # Delete chat
        with col2:
            if st.button("🗑️", key=f"delete_{cid}"):

                delete_chat(cid)

                if st.session_state.current_chat == cid:

                    new_chat_id = str(uuid.uuid4())
                    create_chat(new_chat_id, "New Email Chat", st.session_state.user_id)

                    st.session_state.current_chat = new_chat_id

                st.rerun()


# ---------------- MAIN ---------------- #

st.title("📧 AI Email Draft Agent")

prompt = st.text_input("Describe the email you want to send")


# -------- GENERATE EMAIL (STREAMING) -------- #

if st.button("Generate Email"):

    save_prompt(chat_id, prompt)

    drafts = get_drafts(chat_id)

    # Auto-title chat from first prompt
    if len(drafts) == 0:
        update_chat_title(chat_id, prompt[:40])

    placeholder = st.empty()
    streamed_text = ""

    for chunk in graph.stream(
        {"prompt": prompt},
        config={"configurable": {"thread_id": chat_id}},
    ):

        if "__interrupt__" in chunk:

            draft = chunk["__interrupt__"][0].value["draft"]

            version = len(drafts) + 1

            save_draft(chat_id, draft, version)

            break

        if "drafter" in chunk:

            token = chunk["drafter"]

            streamed_text += token

            placeholder.text_area(
                "Generating Draft...",
                value=streamed_text,
                height=200
            )

    st.rerun()


# ---------------- SHOW DRAFTS ---------------- #

drafts = get_drafts(chat_id)

if drafts:

    st.subheader("Email Draft Versions")

    for draft, version, sent in drafts:

        if sent:
            st.success(f"📧 Draft Version {version} Sent Successfully!")

        st.text_area(
            f"Draft Version {version}",
            value=draft,
            height=200,
            key=f"{chat_id}_{version}"
        )

    latest_version = drafts[-1][1]

    col1, col2 = st.columns(2)

    # -------- APPROVE EMAIL -------- #

    with col1:

        if st.button("Approve & Send"):

            graph.invoke(
                {"approved": True},
                config={"configurable": {"thread_id": chat_id}},
            )

            mark_sent(chat_id, latest_version)

            st.rerun()

    # -------- FEEDBACK / REVISION -------- #

    with col2:

        feedback = st.text_input("Request changes")

        if st.button("Submit Feedback"):

            result = graph.invoke(
                {
                    "approved": False,
                    "feedback": feedback,
                },
                config={"configurable": {"thread_id": chat_id}},
            )

            if "__interrupt__" in result:

                draft = result["__interrupt__"][0].value["draft"]

                version = latest_version + 1

                save_draft(chat_id, draft, version)

                st.rerun()