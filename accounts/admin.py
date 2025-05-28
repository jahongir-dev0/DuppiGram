from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "phone_number", "is_online", "last_seen", "show_friends_status")
    search_fields = ("username", "email", "phone_number")
    list_filter = ("is_online", "show_friends_status", "gender")
    readonly_fields = ("last_seen",)  # ✅ Last seen faqat ko‘rish uchun

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "profile_image", "phone_number", "location", "gender")
        }),
        ("Status", {"fields": ("is_online", "last_seen", "show_friends_status")}),
        ("Social Media", {"fields": ("facebook", "instagram", "linkedin")}),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2",
                "phone_number", "location", "gender", "profile_image",
                "is_online", "show_friends_status",
                "facebook", "instagram", "linkedin"
            ),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")  # ✅ Admin uchun qulaylik

admin.site.register(CustomUser, CustomUserAdmin)