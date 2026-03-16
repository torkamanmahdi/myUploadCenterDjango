from django.db import models
from django.contrib.auth import get_user_model
import uuid
import os


User = get_user_model()


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)


class UploadedFile(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='uploaded_files',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_file_path)
    file_type = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_public = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_file_type(self):
        filename = self.file.name.lower()
        if filename.endswith(('.mp4', '.avi', '.mov', '.wmv')):
            return 'video'
        if filename.endswith(('.mp3', '.wav', '.ogg')):
            return 'audio'
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return 'image'
        if filename.endswith('.pdf'):
            return 'pdf'
        return 'other'

    def save(self, *args, **kwargs):
        self.file_type = self.get_file_type()
        super().save(*args, **kwargs)

    @property
    def file_size(self):
        if self.file and hasattr(self.file, 'size'):
            return self.file.size
        return 0


class SiteThemeSettings(models.Model):
    logo = models.ImageField(upload_to='branding/', blank=True, null=True)
    brand_name = models.CharField(max_length=120, default='Upload Center')
    primary_color = models.CharField(max_length=20, default='#2563eb')
    accent_color = models.CharField(max_length=20, default='#0ea5e9')
    navigation_links = models.TextField(
        blank=True,
        help_text='One menu item per line as "Label|/path/".',
    )

    class Meta:
        verbose_name = 'Site theme settings'
        verbose_name_plural = 'Site theme settings'

    def __str__(self):
        return 'Site theme'


class UploadCenterSettings(models.Model):
    allowed_extensions = models.CharField(
        max_length=255,
        default='jpg,jpeg,png,gif,mp4,mp3,pdf',
        help_text='Comma separated file extensions without dot.',
    )
    max_file_size_mb = models.PositiveIntegerField(
        default=50,
        help_text='Maximum file size in megabytes.',
    )

    class Meta:
        verbose_name = 'Upload center settings'
        verbose_name_plural = 'Upload center settings'

    def __str__(self):
        return 'Upload center config'
