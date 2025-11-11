# 💸 **Smart Expenses**

Automate your expense tracking effortlessly.  
**Smart Expenses** is a Python-based automation that reads expense-related emails and logs them into **Google Sheets** — running **manually or automatically** every day at **20:00 (Madrid time)** via **GitHub Actions**.

---

## 🧠 **Overview**

This project connects to your email account through **IMAP**, retrieves messages matching specific filters (sender, subject, date), parses and classifies them into spending categories, and records the results in **Google Sheets** using a Google Service Account.

It can run locally or automatically in the cloud, ensuring your expense log is always **up-to-date and accurate**.

---

## ⚙️ **Technologies Used**

- 🐍 **Python 3.13**
- 🧾 **Google Sheets API**
- 📬 **IMAP / Gmail**
- ⚡ **python-dotenv**
- 🤖 **GitHub Actions** for automation
- 🧱 **Logging** for structured runtime monitoring

---

## 🧩 **Project Structure**

```bash
smart_expenses/
├── app.py                 # Main entry point
├── utils/
│   ├── retrieve_emails.py # Fetch and parse emails via IMAP
│   ├── parser.py          # Extract expense data from email content
│   ├── classifier.py      # Categorize expenses using predefined rules
│   ├── sheets.py          # Append parsed data into Google Sheets
│   └── connection.py      # Handles IMAP connection and errors
├── config/
│   ├── settings.py        # Loads environment variables and constants
│   ├── constants.py       # Shared constant values
│   └── categories.json    # Category definitions for classification
├── secrets/
│   └── key.json           # Google service account key (ignored by Git)
├── .github/
│   └── workflows/
│       └── daily.yml      # GitHub Actions workflow (runs daily)
└── requirements.txt
```

---

## 🚀 **Local Setup**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/matiassanroman/smart_expenses.git
cd smart_expenses
```

### 2️⃣ Create a virtual environment

```bash
python -m venv env
# macOS / Linux
source env/bin/activate
# Windows
env\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Create a file named `.env.local` in the project root:

```env
IMAP_SERVER=imap.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
SEARCH_FROM="no-reply@somewhere.com"
SEARCH_SUBJECT="Your Expense Receipt"
SPREADSHEET_ID=your_google_sheet_id
SERVICE_ACCOUNT_KEY_PATH=secrets/key.json
```

💡 *For Gmail, you must enable [App Passwords](https://myaccount.google.com/apppasswords) to connect via IMAP securely.*

### 5️⃣ Add your Google service account key

1. Create a service account in your [Google Cloud Console](https://console.cloud.google.com/).  
2. Enable the **Google Sheets API**.  
3. Download the JSON key file and save it as `secrets/key.json`.  
4. Share your Google Sheet with the service account email (`xxxx@xxxx.iam.gserviceaccount.com`).

---

## 🧪 **Run Locally**

```bash
python app.py
```

This will:

1. Connect to your Gmail inbox  
2. Retrieve yesterday’s expense emails  
3. Classify and parse them  
4. Append the data into your Google Sheet  

---

## 🤖 **Automate with GitHub Actions**

The included workflow `.github/workflows/daily.yml` runs automatically every day at **20:00 (Madrid time)**.

### ✅ How it works

1. GitHub Actions checks out your repository  
2. Installs Python and dependencies  
3. Securely reconstructs `.env.local` and `secrets/key.json` from GitHub Secrets  
4. Runs `app.py`  
5. Sends an email notification about success or failure  

---

## 🔐 **Required GitHub Secrets**

| Secret name           | Description                             |
| --------------------- | --------------------------------------- |
| `IMAP_SERVER`         | IMAP server (e.g., `imap.gmail.com`)    |
| `EMAIL_USER`          | Your Gmail address                      |
| `EMAIL_PASS`          | Your Gmail App Password                 |
| `SEARCH_FROM`         | Sender filter for expenses              |
| `SEARCH_SUBJECT`      | Subject filter for expenses             |
| `SPREADSHEET_ID`      | Your Google Sheet ID                    |
| `SERVICE_ACCOUNT_KEY` | JSON string of your service account key |

---

## 🧹 **Security Notes**

- `.env.local` and `secrets/key.json` are **dynamically generated** during the workflow and **never committed** to Git.  
- All sensitive data is stored in **GitHub Secrets**.  
- The workflow automatically **removes temporary credentials** after each run.
