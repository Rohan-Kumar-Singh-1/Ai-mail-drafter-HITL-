# 📧 AI Email Draft Agent

An intelligent, persistent email assistant built with **LangGraph**, **Streamlit**, and **OpenAI**. This application allows users to generate professional email drafts, provide feedback for revisions, and manage a history of conversations through a dedicated SQLite backend.

---

## 🚀 Features

* **Human-in-the-Loop:** Uses LangGraph `interrupt` to pause the workflow, allowing users to approve or request changes to drafts.
* **Persistent Memory:** State is saved using `SqliteSaver`, enabling you to resume email drafting sessions anytime.
* **User Authentication:** Secure login and registration system to keep your drafts private.
* **Version Control:** Automatically tracks multiple versions of an email draft based on your feedback.
* **Streaming UI:** Real-time text generation in the Streamlit interface for a responsive experience.

---

## 🏗️ Architecture

The application follows a modular structure to separate logic, state, and UI:

* **`app.py`**: The main Streamlit entry point and UI logic.
* **`graph.py`**: Defines the LangGraph state machine and workflow transitions.
* **`nodes.py`**: Contains the LLM logic for drafting emails and the `interrupt` for human review.
* **`database.py`**: Handles SQLite operations for users, chat history, and draft persistence.
* **`state.py`**: Defines the `TypedDict` schema for the graph's shared state.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-email-agent.git
cd ai-email-agent

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Setup Environment Variables

Create a `.env` file in the root directory and add your API keys:

```env
OPENROUTER_API_KEY=your_api_key_here

```

*(Note: The current configuration uses OpenRouter; you can modify `nodes.py` to use OpenAI directly if preferred.)*

---

## 🚦 Usage

1. **Start the Application:**
```bash
streamlit run app.py

```


2. **Register/Login:** Create an account to start your first session.
3. **Generate:** Enter a prompt (e.g., *"Request a follow-up meeting with the marketing team for next Tuesday"*).
4. **Review:** * If you like the draft, click **Approve & Send**.
* If it needs changes, type your feedback in the **Request Changes** box and submit.


5. **History:** Use the sidebar to switch between different email threads or delete old ones.

---

## 🧠 Tech Stack

| Component | Technology |
| --- | --- |
| **Orchestration** | [LangGraph](https://github.com/langchain-ai/langgraph) |
| **LLM** | GPT-4o-mini (via OpenRouter/LangChain) |
| **Frontend** | Streamlit |
| **Database** | SQLite3 |
| **State Management** | LangGraph Checkpointers |

---

## 📝 License

This project is licensed under the MIT License.
