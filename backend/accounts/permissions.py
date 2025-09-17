from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    السماح بالقراءة للجميع، والكتابة فقط للمستخدمين الذين لديهم is_staff = True
    """
    def has_permission(self, request, view):
        # كل المستخدمين يمكنهم GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # الكتابة فقط للمسؤولين
        return request.user and request.user.is_staff
