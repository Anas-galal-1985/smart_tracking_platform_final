from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

# إلغاء تسجيل User الافتراضي
admin.site.unregister(User)

# إنشاء Inline لـ Profile ليظهر داخل صفحة User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# إعادة تسجيل User مع Profile Inline
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)  # إضافة الـ Profile داخل صفحة User
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')




# تسجيل Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'role', 'created_at')
    search_fields = ('user__username', 'full_name', 'role')
    list_filter = ('role', 'created_at')

# ملاحظة: لا تسجل User مرة أخرى إذا كان مسجل مسبقًا

