from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponseForbidden
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Sum
from .models import UploadedFile, UploadCenterSettings
from .forms import (
    UploadFileForm,
    SignUpForm,
    LoginForm,
)
import os
import mimetypes


def _get_upload_settings():
    settings_obj = UploadCenterSettings.objects.first()
    if not settings_obj:
        settings_obj = UploadCenterSettings.objects.create()
    return settings_obj


def home(request):
    upload_settings = _get_upload_settings()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.cleaned_data['file']
            max_bytes = upload_settings.max_file_size_mb * 1024 * 1024
            if file_obj.size > max_bytes:
                form.add_error('file', 'File is larger than allowed size.')
            else:
                allowed_exts = [
                    ext.strip().lower()
                    for ext in upload_settings.allowed_extensions.split(',')
                    if ext.strip()
                ]
                ext = os.path.splitext(file_obj.name)[1].lstrip('.').lower()
                if allowed_exts and ext not in allowed_exts:
                    form.add_error('file', 'File extension is not allowed.')
                else:
                    uploaded_file = form.save(commit=False)
                    if request.user.is_authenticated:
                        uploaded_file.owner = request.user
                    uploaded_file.save()
                    return redirect('file_detail', unique_id=uploaded_file.unique_id)
    else:
        form = UploadFileForm()

    stats = UploadedFile.objects.aggregate(
        total_views=Sum('view_count'),
        total_downloads=Sum('download_count'),
    )
    latest_public = UploadedFile.objects.filter(is_public=True).order_by('-upload_date')[:6]

    context = {
        'form': form,
        'upload_settings': upload_settings,
        'latest_public': latest_public,
        'total_files': UploadedFile.objects.count(),
        'total_views': stats.get('total_views') or 0,
        'total_downloads': stats.get('total_downloads') or 0,
    }
    return render(request, 'filemanager/home.html', context)


def file_detail(request, unique_id):
    file = get_object_or_404(UploadedFile, unique_id=unique_id)
    return render(request, 'filemanager/file_detail.html', {'file': file})


def file_view(request, unique_id):
    file = get_object_or_404(UploadedFile, unique_id=unique_id)
    file.view_count += 1
    file.save(update_fields=['view_count'])
    context = {
        'file': file,
        'file_type': file.file_type,
    }
    return render(request, 'filemanager/file_view.html', context)


def file_download(request, unique_id):
    file = get_object_or_404(UploadedFile, unique_id=unique_id)

    if request.GET.get('download') != 'true':
        return render(request, 'filemanager/download_wait.html', {'file': file})

    file.download_count += 1
    file.save(update_fields=['download_count'])

    file_path = file.file.path
    mime_type, _ = mimetypes.guess_type(file_path)

    if not mime_type:
        mime_type = 'application/octet-stream'

    response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file.file.name)}"'
    return response


def public_gallery(request):
    files = UploadedFile.objects.filter(is_public=True).order_by('-upload_date')
    return render(request, 'filemanager/public_gallery.html', {'files': files})


@login_required
def dashboard(request):
    files = UploadedFile.objects.filter(owner=request.user).order_by('-upload_date')
    return render(request, 'filemanager/dashboard.html', {'files': files})


@login_required
def delete_file(request, unique_id):
    file = get_object_or_404(UploadedFile, unique_id=unique_id)
    if file.owner != request.user:
        return HttpResponseForbidden('You do not own this file.')
    if request.method == 'POST':
        file.file.delete(save=False)
        file.delete()
        return redirect('dashboard')
    return render(request, 'filemanager/confirm_delete.html', {'file': file})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'filemanager/auth_signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm(request)
    return render(request, 'filemanager/auth_login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
