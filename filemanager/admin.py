from django.contrib import admin
from django.db.models import FileField
from django.utils.html import format_html
from .models import UploadedFile
import os

class FileSizeFilter(admin.SimpleListFilter):
    title = 'File Size'
    parameter_name = 'file_size'
    
    def lookups(self, request, model_admin):
        return (
            ('small', 'Small (< 1MB)'),
            ('medium', 'Medium (1MB - 10MB)'),
            ('large', 'Large (> 10MB)'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'small':
            return queryset.filter(file__size__lt=1024*1024)
        if self.value() == 'medium':
            return queryset.filter(file__size__gte=1024*1024, file__size__lt=10*1024*1024)
        if self.value() == 'large':
            return queryset.filter(file__size__gte=10*1024*1024)

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'upload_date', 'get_file_size', 'file_preview')
    list_filter = ('file_type', 'upload_date', FileSizeFilter)
    search_fields = ('title', 'file_type')
    readonly_fields = ('file_type', 'unique_id', 'get_file_size', 'file_preview')
    date_hierarchy = 'upload_date'
    
    def get_file_size(self, obj):
        try:
            size_bytes = obj.file.size
            if size_bytes < 1024:
                return f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes/1024:.2f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                return f"{size_bytes/(1024*1024):.2f} MB"
            else:
                return f"{size_bytes/(1024*1024*1024):.2f} GB"
        except:
            return "Unknown"
    get_file_size.short_description = 'File Size'
    
    def file_preview(self, obj):
        if obj.file_type == 'image':
            return format_html('<img src="{}" width="100" height="auto" />', obj.file.url)
        elif obj.file_type == 'video':
            return format_html('<video width="100" height="auto" controls><source src="{}"></video>', obj.file.url)
        elif obj.file_type == 'audio':
            return format_html('<audio controls><source src="{}"></audio>', obj.file.url)
        elif obj.file_type == 'pdf':
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.file.url)
        else:
            return format_html('<a href="{}" target="_blank">Download File</a>', obj.file.url)
    file_preview.short_description = 'Preview'
