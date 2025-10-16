from django.contrib import admin

from media.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('title', 'image_file', 'uploaded_by_user')
