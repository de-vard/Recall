from django.contrib import admin


from .models import Course, CourseStudent, CourseLike


# ---------- INLINES ----------

class CourseStudentInline(admin.TabularInline):
    model = CourseStudent
    extra = 0
    autocomplete_fields = ("user",)
    readonly_fields = ("date_joined",)
    fields = ("user", "role", "date_joined")
    search_fields = ("user__username", "user__email")


class CourseLikeInline(admin.TabularInline):
    model = CourseLike
    extra = 0
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at",)
    fields = ("user", "created_at")
    search_fields = ("user__username", "user__email")


# ---------- ADMIN COURSE ----------

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "title",
        "author",
        "folder",
        "is_public",
        "students_count",
        "likes_count",
        "created",
    )

    list_filter = ("is_public", "folder", "created")
    search_fields = ("title", "description", "author__username", "folder__name")
    autocomplete_fields = ("author", "folder")
    ordering = ("-created",)

    inlines = [CourseStudentInline, CourseLikeInline]

    readonly_fields = ("created", "updated")
    fields = (
        "title",
        "description",
        "author",
        "folder",
        "is_public",
        ("created", "updated"),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.with_related().with_students().with_likes_count()

    # ----- Custom columns -----

    @admin.display(description="Студентов", ordering="students")
    def students_count(self, obj):
        return obj.students.count()

    @admin.display(description="Лайков")
    def likes_count(self, obj):
        return getattr(obj, "likes_count", obj.likes.count())


# ---------- ADMIN COURSE STUDENT ----------

@admin.register(CourseStudent)
class CourseStudentAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "user", "role", "date_joined")
    search_fields = ("course__title", "user__username")
    list_filter = ("role", "date_joined")
    autocomplete_fields = ("course", "user")


# ---------- ADMIN COURSE LIKE ----------

@admin.register(CourseLike)
class CourseLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "user", "created_at")
    search_fields = ("course__title", "user__username")
    list_filter = ("created_at",)
    autocomplete_fields = ("course", "user")
