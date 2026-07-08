# EduAdmin — School Management System

A full-featured Django web application for managing school operations — students, teachers, classes, fees, receipts, and expenditures. Built with Django 6.0, Python 3.12, and Tailwind CSS. Supports three roles: **Admin**, **Teacher**, and **Parent**, each with their own views and permissions.

---

## Project Structure

```
schoolmanagement/          # Django project config (settings, urls, wsgi/asgi)
account/                   # Auth & user management — custom user model, roles, registration, login
dashboard/                 # Dashboard with stats, recent payments, expenditure overview
student/                   # Student CRUD — add, edit, view profiles, search, class filters
teacher/                   # Teacher & class management — add, edit, delete, assign class teachers
fees/                      # Fee structure (master) and payment recording with receipt generation
expenditure/               # Expense tracking — categories, amounts, dates
receipts/                  # Receipt viewer and PDF download (WeasyPrint)
theme/                     # Tailwind CSS source and compiled styles
templates/                 # All HTML templates organized by app
  ├── base.html            # Master layout with sidebar, topbar, flash messages
  ├── account/             # Login, register, change password, portal, user management
  ├── dashboard/           # Dashboard page
  ├── students/            # Student list, add, edit, profile pages
  ├── teacher/             # Teachers and classes pages
  ├── fees/                # Fee master and payment pages
  ├── expenditure/         # Expenditure page
  └── receipts/            # Receipt list and printable receipt
```

---

## Features

### Authentication & User Management
- Email-based login (no username)
- Role-based access control using a `@role_required()` decorator
- One-time admin registration on first visit
- Forced password change on first login
- Full user CRUD for admins
- Auto-linking of teacher/parent profiles to user accounts

### Student Management
- Add, edit, view, and list students
- Search and filter by class
- Auto-link parents by matching father/mother name to parent accounts
- Aadhaar number as a unique identifier

### Teacher & Class Management
- Manage teachers and classes with full CRUD
- Assign class teachers and set section/capacity
- Auto-link teacher profiles to user accounts by email

### Fee Management
- Set fee structures per class (admission, hostel, transport, school, tuition)
- Record payments with auto-generated receipt numbers (`RCP-YYYY-NNN`)
- Thread-safe receipt counter using `select_for_update()`
- View complete payment ledger

### Receipts
- View all receipts with search and date filters
- Print-styled receipt view
- PDF download via WeasyPrint (accessible to Admin, Teacher, and Parent)

### Parent Portal
- Parents see their linked children's fee details
- Fee breakdown with progress bars by type
- Payment history and receipt downloads

### Expenditure Tracking
- Log expenses by category (salaries, utilities, maintenance, supplies, etc.)
- View all expenditures in a table

### Dashboard
- Stats cards: total students, fees collected, expenditure, surplus
- Recent payments and expenditure tables
- Outstanding fee breakdown by class
- Quick action button to add a student

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0.4, Python 3.12 |
| Database | SQLite3 (default) |
| Frontend | Tailwind CSS (CDN), Tabler Icons, Google Fonts (Syne + DM Sans) |
| PDF | WeasyPrint 68.1 |
| Auth | Custom user model with email-based login and role-based permissions |

---

## Setup

### Prerequisites
- Python 3.12
- pip (or uv for faster installs)

### Steps

```bash
# 1. Clone the repo
git clone <repo-url>
cd EduAdmin---School-Management-System-main

# 2. Create a virtual environment
# Windows:
python -m venv venv
venv\Scripts\activate

# Linux / Mac:
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start the dev server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

### First-Time Setup
1. Go to `http://127.0.0.1:8000/account/register/` to create the first Admin user (this page only works if no admin exists yet).
2. Log in with those credentials.
3. You'll be asked to change your password — do that.
4. Head to `/account/users/` to create Teacher and Parent accounts.

### Environment Variables (optional)
Create a `.env` file in the project root if you want to override defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | A dev fallback key | Django secret key |
| `DJANGO_DEBUG` | `True` | Set to `False` in production |

### Notes
- Tailwind CSS is loaded via CDN — no build step needed.
- The repo includes a pre-populated `db.sqlite3` if you want to poke around immediately. Delete it and re-run `migrate` for a fresh start.
- WeasyPrint needs system libraries on Linux (`libpango`, `libcairo`, etc.) — install them if PDF downloads don't work.

---

## Roles & Permissions

| Role | Access |
|------|--------|
| **Admin** | Everything — dashboard, students, teachers, classes, fees, receipts, expenditure, user management |
| **Teacher** | Dashboard, view students and teachers, view receipts |
| **Parent** | Portal with linked children's fee details and receipt downloads |
