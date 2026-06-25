# School Management System — Bug Fixing Session

## Status: Session complete — all 20 bugs fixed

## Fixed Bugs (✅)

1. ✅ **teacher/views.py:48,70** — `edit_teacher`/`edit_class` — Renamed single-instance vars (`teacher`, `std_class`) and added full querysets to avoid variable shadowing in templates
2. ✅ **expenditure/views.py:20-22** — Fixed `NameError` on invalid POST by attaching `else` to `if form.is_valid()` instead of `if request.method == 'POST'`
3. ✅ **dashboard/views.py:7** — Added `'TEACHER'` to `@role_required` decorator
4. ✅ **fees/views.py:90** — Added `@role_required('ADMIN')` to `generate_receipt`
5. ✅ **receipts/views.py:50** — Added `@role_required('ADMIN','TEACHER','PARENT')` to `download_receipt`
6. ✅ **student/models.py:14** — Changed `CASCADE` → `PROTECT` on `student_class` FK
7. ✅ **teacher/models.py:19** — Changed `CASCADE` → `PROTECT` on `class_teacher` FK
8. ✅ **account/models.py:53-64** — Removed `self.is_superuser = True` from ADMIN branch in `save()`
9. ✅ **fees/views.py:72-76** — Chained `select_for_update()` with `get_or_create()` to fix race condition
10. ✅ **student/views.py:4** — Changed import from `.models` to `teacher.models` for `ClassModel`
11. ✅ **base.html:96** — Fixed Students link: `'students'` → `'show_students'`
12. ✅ **base.html:109** — Fixed Teachers link: `'teachers'` → `'show_teachers'`
13. ✅ **base.html:133** — Fixed Payments link: `'payments'` → `'payment'`
14. ✅ **base.html:103-106** — Added active highlighting block for Classes link

15. ✅ **settings.py:23** — Hardcoded `SECRET_KEY` → `os.environ.get()` with fallback
16. ✅ **settings.py:26** — `DEBUG = True` → env var (`os.environ.get('DJANGO_DEBUG', 'True') == 'True'`)
17. ✅ **account/views.py:189** — Removed redundant role check after decorator
18. ✅ **requirements.txt** — Removed unnecessary packages (paramiko, pyserial, pexpect, etc.)
19. ✅ **fees/urls.py, expenditure/urls.py** — Removed duplicate `/add/` routes pointing to same view
20. ✅ **schoolmanagement/views.py** — Emptied file, removed dead import from urls.py

## Project Context
- Django 6.0.4, Python 3.12, SQLite3
- Apps: account, dashboard, student, teacher, fees, expenditure, receipts, theme
- Custom user model (email-based login), roles: ADMIN, TEACHER, PARENT
- Fee management with receipt PDF generation (WeasyPrint)
- Dark theme UI with Tailwind CSS (CDN)
