from django.contrib import admin
from courses.models import Course
from folders.models import Folder


class FolderCourseInline(admin.TabularInline):
    model = Course
    extra = 0
    autocomplete_fields = ("author",)
    readonly_fields = ("created",)
    fields = ("title", "author", "is_public", "created")
    show_change_link = True


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_select_related = ("owner", "parent_folder")

    list_display = ("public_id", "title", "owner", "parent_folder", "created")
    list_filter = ("owner",)  # если добавить "parent_folder" вызывает огромные запросы в бд
    search_fields = ("title", "owner__email")
    autocomplete_fields = ("owner", "parent_folder")
    ordering = ("created",)

    inlines = [FolderCourseInline]
