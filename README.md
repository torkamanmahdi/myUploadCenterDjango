## Upload Center

Minimal, modern file upload center built with Django. It provides a clean upload experience, shareable links, a public gallery for files you mark as public, and a simple member dashboard.

### Features

- **Instant uploads**: Upload any supported file and get unique view/download links.
- **Modern minimal UI**: Dark, focused layout with a compact header, hero section, and footer.
- **Public gallery**: Optional gallery listing only the files marked as public.
- **Member dashboard**: Authenticated users can see and manage their own files.
- **Download + view counters**: Each file tracks views and downloads.
- **Configurable upload rules**: Allowed extensions and maximum file size are configurable from the admin.
- **Theme settings**: Basic branding (logo, colors, navigation links) configurable from the admin.
- **Password reset flow**: Built-in "forgot password" via Django auth views (console backend for development).

### Tech stack

- **Backend**: Django 5
- **Database**: SQLite (default, easy to switch)
- **Frontend**: Django templates + Bootstrap 5 + custom minimal styling

### Project structure

Key parts of the project:

- **`uploadcenter/`**
  - `settings.py`: Core Django settings, static/media config, auth redirect URLs.
  - `urls.py`: Root URL configuration, including auth password reset routes.
- **`filemanager/`**
  - `models.py`:
    - `UploadedFile`: Main file model with owner, view/download counts, and `is_public` flag.
    - `SiteThemeSettings`: Simple theme configuration (logo, colors, custom navigation).
    - `UploadCenterSettings`: Upload policy (allowed extensions, max file size in MB).
  - `views.py`:
    - `home`: Minimal main page with upload form, stats, latest public files.
    - `file_detail`, `file_view`, `file_download`: Detail, inline preview, and download with timer + counting.
    - `public_gallery`: Grid-like public gallery for `is_public=True` files.
    - `dashboard`: Member dashboard listing files owned by the logged-in user.
    - `delete_file`: Owner-only deletion of files.
    - `signup_view`, `login_view`, `logout_view`: Simple auth flows.
  - `forms.py`:
    - `UploadFileForm`: Upload form including "show in public gallery".
    - `SignUpForm`, `LoginForm`: Simple member auth forms.
  - `admin.py`:
    - Enhanced `UploadedFileAdmin` with owner, public flag, counters, preview, and size filter.
    - Admin for `SiteThemeSettings` and `UploadCenterSettings`.
  - `templates/filemanager/`:
    - `base.html`: Core layout, header, and footer.
    - `home.html`: Main upload page with hero, stats, and latest public files.
    - `file_detail.html`, `file_view.html`, `download_wait.html`: File detail, preview, and timed download page.
    - `public_gallery.html`: Public gallery view.
    - `dashboard.html`: Member dashboard for managing uploads.
    - `auth_login.html`, `auth_signup.html`: Sign in / sign up screens.
    - `confirm_delete.html`: Delete confirmation for user-owned files.
  - `templates/registration/`:
    - Password reset templates compatible with Django auth views.

### Getting started

#### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd myUploadCenterDjango
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install -r requirements.txt  # or: pip install django
```

> If `requirements.txt` does not exist yet, you can install at least:
>
> ```bash
> pip install "django>=5.0,<6.0"
> ```

#### 2. Apply migrations

```bash
python manage.py migrate
```

#### 3. Create a superuser

```bash
python manage.py createsuperuser
```

Use this account to access the Django admin for configuration.

#### 4. Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser to access the upload center.

### Admin configuration

Log in to `http://127.0.0.1:8000/admin-manager/` with your superuser account.

- **Theme settings (`SiteThemeSettings`)**:
  - Configure brand name, colors, and (optionally) upload a logo.
  - Optionally define custom navigation links, line by line as `Label|/path/`.
- **Upload settings (`UploadCenterSettings`)**:
  - `allowed_extensions`: Comma-separated list like `jpg,jpeg,png,gif,mp4,mp3,pdf`.
  - `max_file_size_mb`: Maximum allowed file size per upload, in megabytes.

You can also manage and inspect uploaded files via the `UploadedFile` model with filters, previews, and counters.

### Authentication and member dashboard

- **Sign up**: `GET /signup/` – create a new account via a simple form.
- **Sign in**: `GET /login/` – log in with username and password.
- **Dashboard**: `GET /dashboard/` – list of files owned by the logged-in user, with:
  - Title and type
  - Public/private badge
  - View and download counts
  - Quick actions (view, download, delete)
- **Logout**: `GET /logout/` – logs the user out and redirects to the home page.

### Public gallery

- **Route**: `GET /gallery/`
- Shows only files where `is_public = True`.
- Each card links to file detail, view, and download, and shows basic stats.

When uploading on the home page, checking **“Show in public gallery”** sets the `is_public` flag for that file.

### Password reset

The project wires Django’s built-in password reset views:

- `accounts/password-reset/` – request reset link.
- `accounts/password-reset/done/` – confirmation page.
- `accounts/reset/<uidb64>/<token>/` – set new password.
- `accounts/reset/done/` – final success page.

For development, the email backend is set to `console`, so reset emails are printed to the terminal where `runserver` is running.

### File size and extension validation

During upload on the home page:

- The uploaded file is checked against `UploadCenterSettings.max_file_size_mb`.
- The file extension is validated against `UploadCenterSettings.allowed_extensions` (comma-separated, no dots).
- If a rule is violated, a simple error message is shown next to the file field.

### Production notes

This project is configured for local development out of the box. For production you should:

- Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `uploadcenter/settings.py`.
- Use a proper database (PostgreSQL, MySQL, etc.) instead of SQLite.
- Configure a real email backend for password reset emails.
- Serve static files (CSS, JS) and media (uploads) via a proper web server or cloud storage.
- Consider adding rate limiting or authentication around uploads if you expect public traffic.

### License

You can choose and add your preferred license (MIT, BSD, etc.) here. By default this template is unlicensed until you specify one.

