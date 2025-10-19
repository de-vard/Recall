from django.contrib import admin

from folders.models import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    readonly_fields = ('public_id', 'created', 'updated', 'parent_folder')  # запрет на удаление
