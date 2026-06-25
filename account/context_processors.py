def user_roles(request):
    """Expose simple role booleans to templates: is_admin, is_teacher, is_parent.

    Returns False for each when the user is anonymous or the attribute is missing.
    """
    is_admin = False
    is_teacher = False
    is_parent = False

    user = getattr(request, 'user', None)
    if user and getattr(user, 'is_authenticated', False):
        role = getattr(user, 'role', '') or ''
        role = role.upper()
        is_admin = (role == 'ADMIN')
        is_teacher = (role == 'TEACHER')
        is_parent = (role == 'PARENT')

    return {
        'is_admin': is_admin,
        'is_teacher': is_teacher,
        'is_parent': is_parent,
    }
