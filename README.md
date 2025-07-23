# BlogWebsite - Modern Blogging Platform

A full-featured blogging platform built with Django, featuring user authentication, blog management, advanced search, and a modern responsive design.

## 🚀 Features

- **User Authentication**: Secure login/signup with custom user model
- **Blog Management**: Full CRUD operations for blog posts
- **Advanced Search**: Search by title, author, category, or content
- **Category Filtering**: Dynamic filtering by blog categories
- **Image Support**: Upload and display images in blog posts
- **Responsive Design**: Modern UI with gradient themes and animations
- **Admin Panel**: Django admin interface for site management

## 📋 Table of Contents

1. [Backend Architecture](#backend-architecture)
2. [Frontend Design](#frontend-design)
3. [Database Schema](#database-schema)
4. [Installation & Setup](#installation--setup)
5. [User Credentials](#user-credentials)

---

## 🔧 Backend Architecture

### Folder Structure

```
blogwebsite/
├── blogwebsite/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py             # Django settings and configuration
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py                 # WSGI configuration for deployment
│   └── asgi.py                 # ASGI configuration for async support
├── blogapp/                    # Main application directory
│   ├── migrations/             # Database migration files
│   ├── templates/              # HTML templates
│   │   └── blogapp/           # App-specific templates
│   ├── __init__.py
│   ├── admin.py               # Admin panel configuration
│   ├── apps.py                # App configuration
│   ├── models.py              # Database models
│   ├── views.py               # View functions and business logic
│   ├── urls.py                # App-specific URL routing
│   └── tests.py               # Unit tests
├── media/                     # User uploaded files (images)
├── static/                    # Static files (CSS, JS, images)
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── user_credentials.txt       # User account details
```

### Key Files Explanation

#### `settings.py`
- **Database Configuration**: SQLite database setup
- **Media Files**: Configuration for image uploads (`MEDIA_URL`, `MEDIA_ROOT`)
- **Custom User Model**: `AUTH_USER_MODEL = 'blogapp.CustomUser'`
- **Security Settings**: Debug mode, allowed hosts, secret key
- **Installed Apps**: Django apps and custom blogapp

#### `urls.py` (Main)
- **URL Routing**: Maps URLs to views
- **Media Files**: Serves uploaded images in development
- **Admin Panel**: `/admin/` route for Django admin

#### `urls.py` (App)
- **Home Page**: `/` - Main dashboard with featured blogs
- **Authentication**: `/login/`, `/signup/`, `/logout/`
- **Blog Management**: `/my-blogs/`, `/blog/<id>/`, `/blog/edit/<id>/`, `/blog/delete/<id>/`
- **Search**: `/search/` - Advanced search functionality
- **User Settings**: `/settings/`, `/aboutus/`

### Models (`models.py`)

#### `CustomUser` Model
```python
class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15)
    # Inherits: username, email, first_name, last_name, password, is_active, date_joined
```
- **Purpose**: Extended user model with mobile number
- **Authentication**: Supports login with username or email
- **Relationships**: One-to-many with Post model

#### `Post` Model
```python
class Post(models.Model):
    Post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    images = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
- **Purpose**: Stores blog post data
- **Features**: Title, content, author, category, images, timestamps
- **Relationships**: Many-to-one with CustomUser

### Views (`views.py`)

#### Authentication Views

**`login(request)`**
- **Purpose**: Handles user authentication
- **Method**: POST for login, GET for form display
- **Features**:
  - Supports login with username or email
  - Password validation using Django's authenticate()
  - Session management with login()
  - Error handling for invalid credentials
- **Redirect**: Home page on success, login page with error on failure

**`signup(request)`**
- **Purpose**: User registration and account creation
- **Method**: POST for registration, GET for form display
- **Validation**:
  - Password confirmation matching
  - Email uniqueness check
  - Username availability validation
  - Mobile number format validation
- **Features**: Auto-login after successful registration

**`logout(request)`**
- **Purpose**: Secure user logout
- **Method**: POST only (CSRF protection)
- **Features**: Session cleanup, redirect to home page

#### Blog Management Views

**`home(request)`**
- **Purpose**: Main dashboard with featured blogs
- **Method**: GET
- **Features**:
  - Displays all blog posts in grid layout
  - Category filtering functionality
  - Search bar integration
  - Responsive design with pagination
- **Context**: All posts, categories list, user authentication status

**`my_blogs(request)`**
- **Purpose**: Personal blog management interface
- **Method**: GET for display, POST for blog creation
- **Features**:
  - User's blog list with edit/delete options
  - Inline blog creation form
  - Image upload handling
  - Real-time form validation
- **Security**: Login required, user can only see own blogs

**`blog_detail(request, blog_id)`**
- **Purpose**: Individual blog post viewing
- **Method**: GET
- **Features**:
  - Full blog content display
  - Author information
  - Creation/update timestamps
  - Image display if available
- **Error Handling**: 404 for non-existent blogs

**`blog_edit(request, blog_id)`**
- **Purpose**: Edit existing blog posts
- **Method**: GET for form, POST for updates
- **Features**:
  - Pre-populated form with current data
  - Image replacement functionality
  - Auto-resize textarea
  - Form validation and error handling
- **Security**: Only blog author can edit

**`blog_delete(request, blog_id)`**
- **Purpose**: Delete blog posts
- **Method**: POST only (security)
- **Features**:
  - Confirmation modal
  - Cascade deletion of associated images
  - Success/error messaging
- **Security**: Only blog author can delete

#### Search and Navigation

**`search_results(request)`**
- **Purpose**: Advanced search functionality
- **Method**: GET with query parameters
- **Features**:
  - Multi-field search (title, content, author, category)
  - Search type filtering (All, Title, Author, Category)
  - Category-based filtering
  - Combined search and filter functionality
- **Query Optimization**: Uses Django Q objects for complex queries

**`aboutus(request)`**
- **Purpose**: Platform information page
- **Method**: GET
- **Features**:
  - Company information
  - Team member profiles
  - Platform statistics
  - Feature highlights

**`settings(request)`**
- **Purpose**: User profile management
- **Method**: GET for display, handles AJAX updates
- **Features**:
  - Profile information display
  - Inline editing capabilities
  - Real-time updates via AJAX
  - Account deletion option

#### Utility Views

**`update_profile(request)`**
- **Purpose**: AJAX profile updates
- **Method**: POST
- **Features**:
  - Field-specific updates (first_name, last_name, email, mobile)
  - JSON response format
  - Validation and error handling
  - No page refresh required

**`delete_account(request)`**
- **Purpose**: Account deletion
- **Method**: POST
- **Features**:
  - Confirmation required
  - Cascade deletion of user's blogs
  - Session cleanup
  - Redirect to home page

---

## 🎨 Frontend Design

### HTML Templates

#### `base.html`
- **Purpose**: Master template with common layout
- **Features**: Navigation header, logout modal, responsive design
- **Styling**: Purple gradient theme, glass morphism effects
- **Navigation**: Home, My Blogs, About Us, Settings, Logout

#### `home.html`
- **Purpose**: Main dashboard and featured blogs
- **Features**: Search bar, category filtering, blog grid
- **Components**: Featured blogs section, search functionality
- **Responsive**: Grid layout adapts to screen size

#### `my_blogs.html`
- **Purpose**: Personal blog management interface
- **Features**: Create, edit, delete blogs with modals
- **Components**: Blog list, create form modal, delete confirmation
- **Interactions**: CRUD operations with JavaScript

#### `search_results.html`
- **Purpose**: Advanced search results display
- **Features**: Search filters, result cards, pagination
- **Components**: Search form, category filters, result grid
- **Functionality**: Multi-field search (title, author, category, content)

#### `blog_detail.html`
- **Purpose**: Individual blog post viewing
- **Features**: Full blog content, author info, metadata
- **Components**: Blog content, author section, navigation
- **Design**: Clean reading experience with typography focus

#### `blog_edit.html`
- **Purpose**: Blog post editing interface
- **Features**: Editable form, image upload, auto-resize textarea
- **Components**: Form fields, save/cancel buttons, current image display
- **Functionality**: Real-time form validation and preview

#### `login.html` & `signup.html`
- **Purpose**: User authentication interfaces
- **Features**: Modern form design, validation, error handling
- **Components**: Input fields, submit buttons, navigation links
- **Design**: Gradient background, glass morphism forms

#### `settings.html`
- **Purpose**: User profile management
- **Features**: Inline editing, real-time updates, account deletion
- **Components**: Profile form, action buttons, confirmation modals
- **Functionality**: AJAX updates without page refresh

#### `aboutus.html`
- **Purpose**: Platform information and team details
- **Features**: Hero section, feature cards, team profiles
- **Components**: Mission statement, statistics, team grid
- **Design**: Engaging layout with animations and gradients

### Design System

#### Color Palette
- **Primary Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Success**: `linear-gradient(135deg, #10b981, #059669)`
- **Danger**: `linear-gradient(135deg, #ef4444, #dc2626)`
- **Text**: `#1f2937` (dark), `#6b7280` (medium), `#9ca3af` (light)

#### Typography
- **Font Family**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **Headings**: Gradient text effects with background-clip
- **Body**: Clean, readable fonts with proper line-height

#### Components
- **Buttons**: Gradient backgrounds, hover animations, shadow effects
- **Cards**: Glass morphism with backdrop-blur and transparency
- **Forms**: Modern inputs with focus states and validation
- **Modals**: Centered overlays with blur backgrounds

---

## 💾 Database Schema

### Database Configuration
- **Type**: SQLite (default Django database)
- **Location**: `db.sqlite3` in project root
- **Encoding**: UTF-8
- **Migrations**: Managed by Django ORM

### Database Credentials
- **Development**: No credentials required (SQLite)
- **Admin Panel**: 
  - URL: `http://127.0.0.1:8000/admin/`
  - Username: `admin`
  - Password: `Blogwebsite@12`

### Schema Details

#### Users Table (`blogapp_customuser`)
```sql
CREATE TABLE blogapp_customuser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    mobile VARCHAR(15),
    password VARCHAR(128) NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    is_staff BOOLEAN DEFAULT 0,
    is_superuser BOOLEAN DEFAULT 0,
    date_joined DATETIME NOT NULL,
    last_login DATETIME
);
```

#### Posts Table (`blogapp_post`)
```sql
CREATE TABLE blogapp_post (
    Post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    images VARCHAR(100),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES blogapp_customuser(id)
);
```

### Data Population
- **Users**: 12 total (1 admin + 11 regular users)
- **Posts**: 65 total across 5 categories
  - Business: 15 posts
  - Technology: 15 posts  
  - Travel: 15 posts
  - Health: 10 posts
  - Food: 10 posts

---

## 🛠 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd blogwebsite
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   cd blogwebsite
   python manage.py migrate
   ```

4. **Start development server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   - Main site: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

### Dependencies
- **Django 5.2.3**: Web framework
- **Pillow 11.2.1**: Image processing
- **asgiref 3.8.1**: ASGI utilities
- **sqlparse 0.5.3**: SQL parsing
- **tzdata 2025.2**: Timezone data

---

## 👥 User Credentials

### Administrator Account
- **Username**: `admin`
- **Email**: `admin@blogwebsite.com`
- **Password**: `Blogwebsite@12`
- **Access**: Full admin panel access

### Regular User Accounts
All regular users have the password: `BlogUser@123`

1. **john_doe** - john.doe@email.com
2. **jane_smith** - jane.smith@email.com
3. **mike_johnson** - mike.johnson@email.com
4. **sarah_wilson** - sarah.wilson@email.com
5. **david_brown** - david.brown@email.com
6. **emily_davis** - emily.davis@email.com
7. **alex_miller** - alex.miller@email.com
8. **lisa_garcia** - lisa.garcia@email.com
9. **tom_anderson** - tom.anderson@email.com
10. **anna_taylor** - anna.taylor@email.com

*Complete credentials available in `user_credentials.txt`*

---

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. For educational use and learning purposes.

---

**Created**: June 20, 2025  
**Version**: 1.0  
**Framework**: Django 5.2.3  
**Database**: SQLite
