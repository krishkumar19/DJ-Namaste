# DJ Namaste — Admin Dashboard

<p align="center">
  <img src="DJ Namasta/img/logo.png" alt="DJ Namaste Logo" width="120"/>
</p>

<p align="center">
  <b>A full-featured Python PyQt5 Admin Dashboard for the DJ Namaste service platform</b><br/>
  Built with PyQt5 · Flask · SQLite3 · Custom Painted Charts
</p>

---

## 📋 Overview

**DJ Namaste** is an on-demand home services platform (DJ, Plumbing, Cleaning, Technicians) with two components:

| Component | Technology | Purpose |
|---|---|---|
| `DJ Namasta/` | HTML / CSS / JS | Customer-facing website to book services |
| `loadi.py` + PyQt5 | Python / PyQt5 | Admin desktop dashboard to manage requests |
| `app.py` | Python / Flask | Bridge server — receives web submissions, writes to SQLite |
| `database.py` | Python / SQLite3 | Database abstraction layer |

**When a customer submits a service request on the website → Flask writes it to `database.db` → Admin opens the desktop app and sees the request instantly in the Analysis section.**

---

## 🚀 Features

- **Splash screen** with animated progress bar
- **Obsidian Dark theme** (`#121212`) across all screens
- **Animated bar chart** on dashboard — hover to see daily INR revenue
- **Analysis / Customer Info screen** — full CRUD (Add, Update, Delete, Search, Select)
- **Service Requests screen** — live hardcoded service allotment table
- **Earnings screen** — INR KPI cards (Monthly Revenue, Net Profit, GST), Quarterly breakdown, interactive hover line chart
- **Insights screen** — NPS, top city, peak hours, avg. ticket value
- **Progress screen** — animated progress bars for operational KPIs
- **Threads screen** — service activity log with status badges
- **Account screen** — admin profile and system info
- **Hamburger sidebar** — collapsible menu

---

## 🗂️ Project Structure

```
progress/
├── loadi.py              # Main PyQt5 admin app — all screens & logic
├── app.py                # Flask web server — receives form submissions
├── database.py           # SQLite3 CRUD layer
├── init_db.py            # One-time DB setup script
├── main.py               # Entry point
├── style.qss             # Global dark theme stylesheet
├── krish.ui              # Qt Designer — Dashboard screen
├── mainfile.ui           # Qt Designer — Analysis screen
├── anlysis.ui            # Qt Designer — Customer Info / CRUD screen
├── costumer.ui           # Qt Designer — Service Requests screen
├── splash.ui             # Qt Designer — Splash screen
├── database.db           # SQLite3 database (auto-created)
├── DJ Namasta/           # Customer website (HTML/CSS/JS)
│   ├── index.html
│   ├── contact.html
│   ├── css/
│   └── img/
└── icons/                # UI icons
```

---

## ⚙️ Setup & Run

### Prerequisites
- Python 3.9+
- pip

### 1. Install Dependencies
```bash
pip install PyQt5 Flask
```

### 2. Initialize the Database
```bash
python init_db.py
```

### 3. Run the Admin Dashboard
```bash
python loadi.py
```

### 4. (Optional) Run the Web Server
To receive live customer requests from the website:
```bash
python app.py
```
Then open `http://localhost:5000` in your browser.

---

## 🔄 How the Data Pipeline Works

```
Customer fills form on website
        ↓
Flask (app.py) catches POST /submit_request
        ↓
Writes to database.db → service_requests table
        ↓
Admin opens loadi.py → Analysis screen auto-fetches
        ↓
All customer requests appear instantly in the table
```

---

## 🎨 Tech Stack

- **UI Framework:** PyQt5
- **Web Backend:** Flask
- **Database:** SQLite3
- **Charts:** Custom `QPainter` — animated bars & interactive hover line charts
- **Styling:** Qt Style Sheets (`.qss`) — Obsidian Dark theme

---

## 📸 Screens

| Screen | Description |
|---|---|
| Dashboard | KPI overview, animated bar chart, financial summary |
| Analysis | Customer CRUD with live DB search |
| Service Requests | Current allotments table |
| Earnings | INR revenue cards, quarterly breakdown, trend chart |
| Insights | Business KPIs — NPS, peak hours, top city |
| Progress | Operational progress bars |
| Threads | Activity log with status badges |
| Account | Admin profile & system status |

---

## 🛡️ License

This project is private and developed for **DJ Namaste** internal use.

---

<p align="center">Made with ❤️ by the DJ Namaste Team</p>
