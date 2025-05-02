from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedFile
from .forms import UploadFileForm
import os
import mimetypes

def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            return redirect('file_detail', unique_id=uploaded_file.unique_id)
    else:
        form = UploadFileForm()
    return render(request, 'filemanager/home.html', {'form': form})

def file_detail(request, unique_id):
    file = get_object_or_404(UploadedFile, unique_id=unique_id)
    return render(request, 'filemanager/file_detail.html', {'file': file})

def file_view(request, unique_id):
    file = get_object_or_404(UploadedFile, unique_id=unique_id)
    context = {
        'file': file,
        'file_type': file.file_type,
    }
    return render(request, 'filemanager/file_view.html', context)

def file_download(request, unique_id):
    file = get_object_or_404(UploadedFile, unique_id=unique_id)
    
    # For download page with timer
    if request.GET.get('download') != 'true':
        return render(request, 'filemanager/download_wait.html', {'file': file})
    
    # Actual file download after timer
    file_path = file.file.path
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if not mime_type:
        mime_type = 'application/octet-stream'
        
    response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file.file.name)}"'
    return response
