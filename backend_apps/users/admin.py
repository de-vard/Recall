from django.contrib import admin
from django.utils.html import format_html
from .models import User, Follow


# ---------------------- INLINE FOLLOW ---------------------- #
class FollowingInline(admin.TabularInline):
    model = Follow
    fk_name = "user_from"
    extra = 0
    autocomplete_fields = ("user_to",)
    readonly_fields = ("created", "updated")
    fields = ("user_to", "created", "updated")
    verbose_name = "Подписка"
    verbose_name_plural = "Подписки"


class FollowersInline(admin.TabularInline):
    model = Follow
    fk_name = "user_to"
    extra = 0
    autocomplete_fields = ("user_from",)
    readonly_fields = ("created", "updated")
    fields = ("user_from", "created", "updated")
    verbose_name = "Подписчик"
    verbose_name_plural = "Подписчики"


# ---------------------- USER ADMIN ---------------------- #
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username", "public_id", "email",
        "first_name", "last_name", "is_staff",
        "is_active", "created", "avatar_preview"
    )
    list_filter = ("is_staff", "is_active", "created")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-created",)

    readonly_fields = ("created", "updated", "avatar_preview")
    fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "password",
        "avatar",
        "avatar_preview",
        ("created", "updated")
    )

    inlines = [FollowingInline, FollowersInline]

    # ---------------- AVATAR PREVIEW ---------------- #
    @admin.display(description="Аватар")
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width:50px;height:50px;border-radius:50%;" />', obj.avatar.url)
        return "Нет аватара"


# ---------------------- FOLLOW ADMIN ---------------------- #
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user_from", "user_to", "created", "updated")
    search_fields = ("user_from__username", "user_from__email", "user_to__username", "user_to__email")
    list_filter = ("created",)
    autocomplete_fields = ("user_from", "user_to")
    ordering = ("-created",)
    readonly_fields = ("created", "updated")
    fields = ("user_from", "user_to", "created", "updated")
