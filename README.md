# 🧠 AI-First CRM HCP Module

An AI-powered Customer Relationship Management (CRM) system designed for **life-science field representatives** to
log and manage interactions with Healthcare Professionals (HCPs).

This project combines a **structured form-based interface** with an **AI-driven conversational assistant**
powered by LangGraph and Groq LLMs.

---

## 🚀 Features

### 📋 Interaction Logging

* Structured form to log HCP interactions
* Fields include:

* HCP Name
* Interaction Type
* Date
* Topics Discussed
* Materials Shared
* Samples Distributed
* Sentiment
* Outcome
* Follow-up Action

---

### 🤖 AI Assistant (Core Feature)

* Conversational interface to log interactions using natural language

* Example:

> “Met Dr. Smith and discussed Product X. Positive sentiment and shared brochures.”

* AI automatically:

* Extracts structured data
* Populates the form
* Generates summaries

---

### 🧠 LangGraph AI Agent

Implements a multi-tool AI agent with dynamic intent routing.

#### Tools implemented:

1. ** Log Interaction Tool**

* Extracts structured CRM data from text

2. ** Edit Interaction Tool**

* Updates existing interactions in the database

3. ** Suggest Follow-up Tool**

* Recommends next actions based on interaction

4. ** HCP Lookup Tool**

* Extracts HCP-related queries

5. ** Material Recommendation Tool**

* Suggests relevant materials (brochures, studies)

---

### 🔄 Real-Time Updates

* Interaction list updates instantly after:

* New entry
* AI-based edits

---

### 💬 Enhanced Chat UI

* Chat history view
* Auto-scroll behavior
* Typing animation
* “Apply to Form” button for AI responses

---

## 🏗️ Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS
* Axios
* Redux (optional extension)

### Backend

* FastAPI
* SQLAlchemy
* MySQL

### AI Layer

* LangGraph
* LangChain
* Groq LLM (`llama-3.3-70b-versatile`)

---

## 📁 Project Structure

```text
root/
├── frontend/
│   ├── src/
│   ├── package.json
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── routes/
│   │   ├── models.py
│   │   ├── main.py
│   ├── .env
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone AI_CRM
cd <project_folder>
```

---

## 🔧 Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Create `.env` file

```env
GROQ_API_KEY=your_api_key_here
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/ai_crm
```

### Run backend

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

## 🗄️ Database Setup

In MySQL:

```sql
CREATE DATABASE ai_crm;
```

Tables will be auto-created by SQLAlchemy.

---

## 💻 Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## 🧪 How to Use

### 1. Manual Logging

* Fill the form and click **Save Interaction**

---

### 2. AI Logging

Type in AI Assistant:

```text
Met Dr. Smith and discussed Product X efficiency. Positive sentiment and shared brochures.
```

Click:

```text
Apply to Form → Save Interaction
```

---

### 3. Edit via AI

```text
Edit interaction 1 and change sentiment to Neutral
```

---

### 4. AI Suggestions

```text
Suggest follow-up for Product X discussion
```

```text
Recommend materials for Product X
```

---

## 🔐 Environment Variables

| Variable     | Description             |
| ------------ | ----------------------- |
| GROQ_API_KEY | This is the API key used for Groq's Large Language Model |
| DATABASE_URL | MySQL connection string |

---

## 🧠 Key Highlights

* AI-first CRM design
* Multi-tool LangGraph agent
* Real-time database updates via AI
* Clean UI with conversational interface
* Production-style architecture

---

## 📌 Future Improvements

* Role-based authentication
* HCP profile enrichment
* Analytics dashboard
* Voice input for field reps
* Deployment (Docker / Cloud)

---

## 👨‍💻 Author

Built as part of an **AI-first CRM system assignment** focusing on real-world healthcare sales workflows.
