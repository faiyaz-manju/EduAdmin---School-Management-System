# 📚 School Management System - Complete Project Context

**Project:** EduAdmin - School Management System  
**Framework:** Django 6.0.4  
**Database:** SQLite3  
**UI:** Tailwind CSS + Tabler Icons  
**Python Version:** 3.12  

---

## 🏗️ Project Architecture

### Directory Structure
```
schoolmanagement/
├── account/                 # Authentication & User Management
├── dashboard/              # Admin Dashboard
├── student/                # Student Management
├── teacher/                # Teacher & Class Management
├── fees/                   # Fee & Payment Management
├── expenditure/            # Expenditure Tracking
├── receipts/               # Receipt Management
├── theme/                  # Tailwind CSS Theme
├── schoolmanagement/       # Main Project Settings
├── templates/              # HTML Templates
├── manage.py               # Django Management
├── db.sqlite3              # Database
└── requirements.txt        # Dependencies
```

---

## 🔐 Authentication System

### User Roles
- **ADMIN** - Full system access, can manage users, teachers, students, fees, expenditure
- **TEACHER** - Can view students and classes, view dashboard
- **PARENT** - Access to parent portal, view child's information

### Models: `account/models.py`

#### CustomUser
- Custom user model extending AbstractBaseUser
- Uses **email** as USERNAME_FIELD (not username)
- Fields:
  - `email` (unique, login credential)
  - `first_name`, `last_name`
  - `role` (ADMIN, TEACHER, PARENT)
  - `is_active`, `is_staff`, `is_superuser`
  - `must_change_password` (enforces password change on first login)
  - `date_joined`

#### TeacherProfile
- Links CustomUser with TeacherModel
- One-to-One relationship with CustomUser
- Fields: `user`, `teacher`, `phone`

#### ParentsProfile
- Links CustomUser with Students (Many-to-Many)
- One-to-One relationship with CustomUser
- Fields: `user`, `students`, `phone`

### Context Processor: `account/context_processors.py`
Exposes role booleans to all templates:
- `is_admin` - True if user.role == 'ADMIN'
- `is_teacher` - True if user.role == 'TEACHER'
- `is_parent` - True if user.role == 'PARENT'

### Views: `account/views.py`

| View | Purpose | Role Required |
|------|---------|---------------|
| `login_view()` | User login | None (public) |
| `logout_view()` | User logout | Authenticated |
| `register_view()` | Admin registration (setup only) | None (one-time) |
| `change_password_view()` | Password change | Authenticated |
| `parents_portal()` | Parent dashboard | PARENT |

### Decorator: `account/decorator.py`
`@role_required('ADMIN', 'TEACHER')` - Restricts views to specific roles

---

## 📚 Student Module

### Model: `student/models.py`

#### Student
```python
- name (CharField)
- father_name, mother_name (CharField)
- date_of_birth (DateField)
- phone_number (CharField)
- adhar_number (unique CharField)
- email (unique EmailField)
- address (TextField)
- student_class (ForeignKey → ClassModel)
- created_at (DateTimeField, auto-created)
```

### Views: `student/views.py`

| View | Purpose | Role Required |
|------|---------|---------------|
| `show_students()` | List all students | ADMIN, TEACHER |
| `add_student()` | Create new student | ADMIN |
| `edit_student()` | Edit student details | ADMIN |
| `student_profile()` | View student details | ADMIN, TEACHER |

### URLs: `student/urls.py`
```
/students/ → show_students
/students/add/ → add_student
/students/<id>/edit/ → edit_student
/students/<id>/ → student_profile
```

---

## 👨‍🏫 Teacher Module

### Models: `teacher/models.py`

#### TeacherModel
```python
- name (CharField)
- phone_number (CharField)
- subject (CharField)
- email (unique EmailField)
```

#### ClassModel
```python
- class_name (CharField)
- section (CharField)
- capacity (BigIntegerField)
- class_teacher (ForeignKey → TeacherModel)
```

### Views: `teacher/views.py`

| View | Purpose | Role Required |
|------|---------|---------------|
| `show_teacher()` | List/Add teachers | ADMIN, TEACHER |
| `show_class()` | List/Add classes | ADMIN, TEACHER |
| `edit_teacher()` | Edit teacher info | ADMIN |
| `delete_teacher()` | Delete teacher | ADMIN |
| `edit_class()` | Edit class info | ADMIN |
| `delete_class()` | Delete class | ADMIN |

### URLs: `teacher/urls.py`
```
/teachers/ → show_teacher
/teachers/<id>/edit/ → edit_teacher
/teachers/<id>/delete/ → delete_teacher
/teachers/classes/ → show_class
/teachers/classes/<id>/edit/ → edit_class
/teachers/classes/<id>/delete/ → delete_class
```

---

## 💰 Fees Module

### Models: `fees/models.py`

#### FeesMasterModel
```python
- student_class (ForeignKey → ClassModel)
- admission (DecimalField)
- hostel (DecimalField)
- transport (DecimalField)
- school (DecimalField)
- tuition (DecimalField)
- updated_at (DateTimeField, auto-updated)
```

#### PaymentModel
```python
- receipt_number (unique CharField)
- student_name (ForeignKey → Student)
- amount (DecimalField)
- date (DateTimeField, auto-created)
```

#### ReceiptCounter
```python
- year (IntegerField, unique)
- last (BigIntegerField) - tracks receipt number sequence
```

### Views: `fees/views.py`

| View | Purpose | Role Required |
|------|---------|---------------|
| `master()` | Manage fee structures by class | ADMIN |
| `payment()` | View all payments | ADMIN |
| `add_payment()` | Record new payment | ADMIN |
| `generate_receipt()` | Generate receipt PDF | ADMIN |

### Receipt Generation Logic
- Auto-generates receipt number: `RCP-YYYY-NNN`
- Uses atomic transaction to prevent race conditions
- Receipt counter is incremented per year

### URLs: `fees/urls.py`
```
/fees/master/ → master (fee structure)
/fees/payments/ → payment (payment list)
/fees/add-payment/ → add_payment
/fees/receipt/<id>/ → generate_receipt
```

---

## 📊 Expenditure Module

### Model: `expenditure/models.py`

#### ExpenditureModel
```python
- category (CharField)
- description (TextField)
- amount (BigIntegerField)
- date (DateField)
```

### Views: `expenditure/views.py`
- View & manage school expenditures
- Role Required: ADMIN

---

## 📋 Receipts Module

### Views: `receipts/views.py`
- Manage and view generated receipts
- Role Required: ADMIN

---

## 📊 Dashboard Module

### Views: `dashboard/views.py`
- Admin/Teacher dashboard overview
- Role Required: ADMIN, TEACHER

---

## 🎨 Frontend Components

### Base Template: `templates/base.html`

**Layout Structure:**
```
┌─────────────────────────────────────┐
│ SIDEBAR (56px width)  │  MAIN AREA  │
├───────────────────────┼─────────────┤
│ Logo                  │  TOPBAR     │
│ Navigation            │  MESSAGES   │
│ • Overview            │  CONTENT    │
│ • Academics           │             │
│ • Finance             │             │
│ • Portals             │             │
│ Settings & Logout     │             │
└─────────────────────────────────────┘
```

**Color Scheme:**
- `ink: #0C0C0E` - Dark background
- `panel: #141416` - Component background
- `gold: #D4A843` - Accent/Active state
- `danger: #C94F4F` - Error/Delete
- `success: #3D9E6E` - Success
- `info: #4A7FCC` - Information

**Navigation Sections (Conditional Display):**

1. **Overview** (ADMIN, TEACHER)
   - Dashboard
   - User Management (ADMIN only)

2. **Academics** (ADMIN, TEACHER)
   - Students
   - Classes
   - Teachers

3. **Finance** (ADMIN only)
   - Fee Master
   - Payments
   - Expenditure
   - Receipts

4. **Portals**
   - Parents (PARENT only)
   - Reports

**Sidebar Features:**
- Dynamic active link highlighting using `request.resolver_match.app_name`
- Role-based menu visibility
- User role badge display
- Notification bell with indicator
- User avatar with initials

---

## ⚙️ Django Settings: `schoolmanagement/settings.py`

### Installed Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'django_browser_reload',
    'dashboard',
    'student',
    'expenditure',
    'theme',
    'account',
    'fees',
    'receipts',
    'teacher',
]
```

### Middleware
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'account.middleware.LoginRequiredMiddleware',  # Custom
]
```

### Key Settings
- **AUTH_USER_MODEL:** `account.CustomUser`
- **LOGIN_URL:** `/account/login/`
- **LOGIN_REDIRECT_URL:** `/dashboard/`
- **TAILWIND_APP_NAME:** `theme`
- **TEMPLATES:** Context processors include `account.context_processors.user_roles`

---

## 🔗 URL Routing: `schoolmanagement/urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('students/', include('student.urls')),
    path('expenditure/', include('expenditure.urls')),
    path('account/', include('account.urls')),
    path('receipts/', include('receipts.urls')),
    path('fees/', include('fees.urls')),
    path('teachers/', include('teacher.urls')),
    path('__reload__/', include('django_browser_reload.urls')),
]
```

---

## 📦 Dependencies: `requirements.txt`

**Key Packages:**
- `Django==6.0.4` - Web framework
- `django-tailwind==4.4.2` - Tailwind CSS integration
- `django-browser-reload==1.21.0` - Auto-reload in development
- `Pillow==11.3.0` - Image processing
- `WeasyPrint` - PDF generation (for receipts)
- Various utility packages (arrow, Babel, cryptography, etc.)

---

## 🔒 Security Features

1. **Custom Authentication:**
   - Email-based login
   - Password validation (min 8 characters)
   - Force password change on first login

2. **Role-Based Access Control:**
   - `@role_required()` decorator on views
   - Template-level checks with `{% if is_admin %}`
   - Role-based sidebar menu filtering

3. **Permission Hierarchy:**
   - ADMIN: Full access to all modules
   - TEACHER: Read-only access to students/classes, dashboard access
   - PARENT: Restricted to parent portal only

4. **CSRF Protection:** Enabled by default

---

## 🚀 Development Setup

### Environment
- Virtual Environment: `myenv/` (Linux) and `mydjvenv/` (Windows)
- Python: 3.12
- Database: SQLite3 (`db.sqlite3`)

### Quick Start
```bash
# Activate virtual environment
source myenv/bin/activate  # Linux
# or
mydjvenv\Scripts\activate  # Windows

# Run migrations
python manage.py migrate

# Create admin (only once)
python manage.py runserver
# Navigate to /account/register/ to create first admin

# Run development server
python manage.py runserver
```

---

## 📋 Form Models

### StudentForm (`student/form.py`)
- Fields: name, father_name, mother_name, date_of_birth, phone_number, adhar_number, email, address, student_class

### TeacherForm (`teacher/form.py`)
- Fields: name, phone_number, subject, email

### ClassForm (`teacher/form.py`)
- Fields: class_name, section, capacity, class_teacher

### FeesMasterForm (`fees/form.py`)
- Fields: student_class, admission, hostel, transport, school, tuition

### PaymentForm (`fees/form.py`)
- Fields: student_name, amount

---

## 🎯 Key Features Summary

✅ Multi-role authentication system  
✅ Student management (CRUD)  
✅ Teacher & Class management  
✅ Fee structure by class  
✅ Payment tracking with receipt generation  
✅ Expenditure tracking  
✅ Role-based dashboard access  
✅ Parent portal  
✅ Dark theme with Tailwind CSS  
✅ Responsive design  
✅ Auto-reload in development mode  

---

## 🔄 Data Flow Example: Payment Processing

```
1. Admin adds payment via /fees/add-payment/
2. PaymentForm validated
3. Payment record created
4. ReceiptCounter incremented atomically
5. Receipt number generated: RCP-2026-001
6. Redirect to /fees/receipt/<payment_id>/
7. Receipt HTML rendered with payment details
8. Can be printed/exported as PDF
```

---

## 📝 Notes

- **SingletonPattern used:** FeesMasterModel uses `update_or_create()` - only one fee structure per class
- **Transaction Safety:** Receipt generation uses `transaction.atomic()` to prevent duplicate receipts
- **Template Inheritance:** All pages extend `base.html` for consistent layout
- **CSS Delivery:** Tailwind CSS via CDN (not compiled)
- **Icon Library:** Tabler Icons (1000+ icons available)

---

*Last Updated: 2026-06-17*
*Django Version: 6.0.4*
