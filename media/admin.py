from django.contrib import admin

from media.models import Image, Sound


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('title', 'path_file', 'uploaded_by_user')
    search_fields = ("title",)  # или любое поле для поиска


@admin.register(Sound)
class SoundAdmin(admin.ModelAdmin):
    fields = ('title', 'path_file', 'uploaded_by_user')
    search_fields = ("title",)  # или любое поле для поиска
