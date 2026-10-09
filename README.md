# 🏡 AI - Real Estate Platform

A cutting-edge, AI-powered real estate platform demonstrating a sophisticated multi-agent system integrated into a full-stack web application. 

This platform allows users to explore properties, add them to wishlists, book site visits, and get instant assistance from specialized AI agents (Sales, Support, and Data Analytics).

---

## ✨ Key Features

- **Multi-Persona AI Chatbot**: A contextual LLM assistant capable of dynamically routing queries to specific sub-agents:
  - 📈 **Sales Agent**: Helps customers find properties matching specific budgets and locations, and calculates mortgage EMIs using integrated financial tools.
  - 🛠️ **Support Agent**: Handles customer service, books site visits, and files support tickets directly into the database.
  - 📊 **Data Agent**: *(Admin Only)* Analyzes system data and generates real-time platform performance summaries.
- **Beautiful Modern UI**: Built with React and Tailwind CSS v4, featuring a glassmorphism design, floating chat widgets, and responsive dashboards.
- **Role-Based Access Control**: Distinct experiences and dashboards for `Admin` and `Customer` roles.
- **Robust Backend**: Powered by FastAPI, SQLAlchemy, and SQLite for high-performance API routing and data management.

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React + Vite (TypeScript)
- **Styling:** Tailwind CSS v4
- **Routing:** React Router v6
- **Icons:** Lucide React

### Backend
- **Framework:** FastAPI (Python)
- **Database:** SQLite + SQLAlchemy ORM
- **Migrations:** Alembic
- **AI Integration:** OpenAI API (GPT-4)
- **Security:** JWT (JSON Web Tokens) + bcrypt

---

## 🚀 Getting Started

Follow these steps to run the project locally. 

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Set up the Backend
```bash
cd backend

# Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000
```
*The backend API will be running at `http://localhost:8000`*

### 2. Set up the Frontend
Open a **new terminal tab**:
```bash
cd frontend

# Install dependencies (if not already installed)
npm install

# Start the development server
npm run dev
```
*The frontend will be running at `http://localhost:5173`*

---

## 🔑 Demo Accounts

The database comes pre-seeded with test data and users. You can easily test the platform by clicking the "Demo Accounts" buttons directly on the login page, or by using the credentials below:

**Admin Account** (Access to Data Agent & Analytics Dashboard)
- **Email:** `admin@demo.com`
- **Password:** `password123`

**Customer Account** (Standard features and workflows)
- **Email:** `customer1@demo.com`
- **Password:** `password123`

---

## 🤖 AI Interaction Examples

Test the dynamic routing and tool-calling capabilities of the AI by asking the floating assistant:

* **Sales Prompt:** *"I am looking for a luxury villa in Chennai under 4,000,000. What is my monthly EMI if I put down 500,000 for 20 years at an 8% rate?"*
* **Support Prompt:** *"I want to book a site visit for property ID 5 tomorrow at 3 PM, and file a support ticket because I have a question about my account."*
* **Admin Analytics Prompt** *(Must be logged in as Admin)*: *"Give me a summary of our platform's current performance and total user count."*
