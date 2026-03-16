from django.contrib import admin
from django.utils.html import format_html
from .models import UploadedFile, SiteThemeSettings, UploadCenterSettings

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

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'file_type',
        'is_public',
        'upload_date',
        'view_count',
        'download_count',
        'get_file_size',
        'file_preview',
    )
    list_filter = ('file_type', 'is_public', 'upload_date', FileSizeFilter)
    search_fields = ('title', 'file_type', 'owner__username')
    readonly_fields = ('file_type', 'unique_id', 'get_file_size', 'file_preview', 'view_count', 'download_count')
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
        return format_html('<a href="{}" target="_blank">Download File</a>', obj.file.url)
    file_preview.short_description = 'Preview'


admin.site.register(UploadedFile, UploadedFileAdmin)


@admin.register(SiteThemeSettings)
class SiteThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'primary_color', 'accent_color')


@admin.register(UploadCenterSettings)
class UploadCenterSettingsAdmin(admin.ModelAdmin):
    list_display = ('max_file_size_mb', 'allowed_extensions')
