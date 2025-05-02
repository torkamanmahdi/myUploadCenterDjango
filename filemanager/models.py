from django.db import models
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)

class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_file_path)
    file_type = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.title
    
    def get_file_type(self):
        filename = self.file.name.lower()
        if filename.endswith(('.mp4', '.avi', '.mov', '.wmv')):
            return 'video'
        elif filename.endswith(('.mp3', '.wav', '.ogg')):
            return 'audio'
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return 'image'
        elif filename.endswith(('.pdf')):
            return 'pdf'
        else:
            return 'other'
    
    def save(self, *args, **kwargs):
        self.file_type = self.get_file_type()
        super().save(*args, **kwargs)
    
    @property
    def file_size(self):
        if self.file and hasattr(self.file, 'size'):
            return self.file.size
        return 0

# Create your models here.
