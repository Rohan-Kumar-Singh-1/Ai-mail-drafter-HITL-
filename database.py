import sqlite3

conn = sqlite3.connect("emails.db", check_same_thread=False)
cursor = conn.cursor()


# ---------------- DATABASE INIT ---------------- #

def init_db():

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # CHATS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        chat_id TEXT PRIMARY KEY,
        title TEXT,
        user_id INTEGER
    )
    """)

    # PROMPTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        prompt TEXT
    )
    """)

    # DRAFTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drafts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        draft TEXT,
        version INTEGER,
        sent INTEGER
    )
    """)

    conn.commit()


# ---------------- USER AUTH ---------------- #

def create_user(username, password):

    try:
        cursor.execute(
            "INSERT INTO users (username,password) VALUES (?,?)",
            (username, password)
        )

        conn.commit()
        return True

    except:
        return False


def authenticate_user(username, password):

    cursor.execute(
        "SELECT id, username FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        return {
            "id": user[0],
            "username": user[1]
        }

    return None


# ---------------- CHAT MANAGEMENT ---------------- #

def create_chat(chat_id, title, user_id):

    cursor.execute(
        "INSERT INTO chats VALUES (?,?,?)",
        (chat_id, title, user_id)
    )

    conn.commit()


def get_chats(user_id):

    cursor.execute(
        "SELECT chat_id,title FROM chats WHERE user_id=?",
        (user_id,)
    )

    return cursor.fetchall()


def update_chat_title(chat_id, title):

    cursor.execute(
        "UPDATE chats SET title=? WHERE chat_id=?",
        (title, chat_id)
    )

    conn.commit()


def delete_chat(chat_id):

    cursor.execute(
        "DELETE FROM chats WHERE chat_id=?",
        (chat_id,)
    )

    cursor.execute(
        "DELETE FROM prompts WHERE chat_id=?",
        (chat_id,)
    )

    cursor.execute(
        "DELETE FROM drafts WHERE chat_id=?",
        (chat_id,)
    )

    conn.commit()


# ---------------- PROMPTS ---------------- #

def save_prompt(chat_id, prompt):

    cursor.execute(
        "INSERT INTO prompts (chat_id,prompt) VALUES (?,?)",
        (chat_id, prompt)
    )

    conn.commit()


# ---------------- DRAFTS ---------------- #

def save_draft(chat_id, draft, version):

    cursor.execute(
        "INSERT INTO drafts (chat_id,draft,version,sent) VALUES (?,?,?,0)",
        (chat_id, draft, version)
    )

    conn.commit()


def mark_sent(chat_id, version):

    cursor.execute(
        "UPDATE drafts SET sent=1 WHERE chat_id=? AND version=?",
        (chat_id, version)
    )

    conn.commit()


def get_drafts(chat_id):

    cursor.execute(
        "SELECT draft,version,sent FROM drafts WHERE chat_id=? ORDER BY version",
        (chat_id,)
    )

    return cursor.fetchall()

