# SmartCampusAI 🤖

SmartCampusAI is a production-ready, premium administrative and educational intelligence portal built using **Python** and **Streamlit**. It features a modern dark-themed glassmorphism interface, role-based session states, protected routes, and a local JSON-based transactional database.

---

## 🌟 Key Features

* **Secure Authentication**: Register and log in using either Username or Email. Passwords are encrypted using high-entropy `bcrypt` salts.
* **Complex Validation Rules**: Enforces alphanumeric usernames, standard email syntaxes, and strong password checks (8+ characters, uppercase, lowercase, numbers).
* **Glassmorphism Interface**: Premium design utilizing customized CSS, rounded borders, glowing micro-animations, linear gradients, dynamic KPI indicators, and responsive grids.
* **Dynamic Sidebar Navigation**: Hides default Streamlit page sidebar listings in favor of a sleek, state-controlled navigation menu powered by `streamlit-option-menu`.
* **Protect Routes**: Dynamic state verification prevents unauthenticated routing to inner pages and enforces idle session expiration.
* **Interactive AI Assistant**: Simulate complex course schedule and campus queries with configurations loaded via environment files.

---

## 📂 Project Structure

```text
SmartCampusAI/
│
├── app.py                      # Main entrypoint and session router
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables configurations
├── .gitignore                  # Git tracking rules
├── README.md                   # Project documentation
│
├── assets/
│   ├── logo.png                # Generated tech branding logo
│   ├── background.png          # Generated abstract neon theme background
│   └── style.css               # Modern glassmorphism CSS overrides
│
├── pages/
│   ├── Login.py                # User login panel
│   ├── Register.py             # User registration form
│   ├── Dashboard.py            # KPI metrics and chat panel
│   ├── Profile.py              # User info visualization and editor
│   └── Settings.py             # Config display and password resets
│
├── database/
│   ├── users.json              # Local transactional JSON database
│   └── database.py             # JSON data models and thread locks
│
├── auth/
│   ├── authentication.py       # Auth controller logic
│   ├── password_utils.py       # bcrypt wrapper functions
│   └── session.py              # Lifecycle state management
│
└── components/
    ├── sidebar.py              # Option-menu custom sidebar
    ├── navbar.py               # Glassmorphic top navigation bar
    └── cards.py                # High-end metrics cards
```

---

## ⚙️ Configuration & Environment Variables

Create a `.env` file in the root directory (included by default):

```env
API_KEY=YOUR_CAMPUS_API_KEY
MODEL_NAME=gpt-4.1
APP_NAME=SmartCampusAI
SESSION_TIMEOUT_SEC=1800
```

---

## 🚀 Local Installation & Execution

### 1. Initialize Virtual Environment
```bash
# Clone the repository and navigate inside
cd SmartCampusAI

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## ⚙️ Transactional JSON Database Schema

Users are stored under `database/users.json` using the following model:

```json
{
    "users": [
        {
            "id": 1,
            "name": "Jane Doe",
            "username": "janedoe",
            "email": "jane@example.com",
            "password": "$2b$12$R.S...",
            "created_at": "2026-07-15T11:00:00",
            "last_login": "2026-07-15T11:05:00"
        }
    ]
}
```

---

## 📦 Deployment Instructions

### Streamlit Community Cloud
1. Push the project files to a GitHub repository.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and select the repository.
3. Configure secret parameters in the Streamlit Cloud Dashboard under **Settings > Secrets**:
   ```toml
   API_KEY = "your_secret_api_key"
   MODEL_NAME = "gpt-4.1"
   APP_NAME = "SmartCampusAI"
   ```
4. Click **Deploy**.

### Railway / Render
1. Create a `Procfile` containing:
   ```text
   web: streamlit run app.py --server.port $PORT
   ```
2. Link your Git repository and deploy.
3. Add Environment Variables via the provider dashboard.
