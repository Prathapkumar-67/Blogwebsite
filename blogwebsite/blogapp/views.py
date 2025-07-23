from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CustomUser, Post
from rest_framework_simplejwt.tokens import RefreshToken

# JWT token helper
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Changed from username to email
        password = request.POST.get('password')
        
        # Get the user by email first
        try:
            user_obj = CustomUser.objects.get(email=email)
            username = user_obj.username
            # Authenticate with the username
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                tokens = get_tokens_for_user(user)
                response = redirect('home')
                response.set_cookie('access_token', tokens['access'], max_age=172800, httponly=True)
                response.set_cookie('refresh_token', tokens['refresh'], max_age=172800, httponly=True)
                auth_login(request, user)
                return response
            else:
                error_message = "Invalid email or password"
                return render(request, 'blogapp/login.html', {'error': error_message})
        except CustomUser.DoesNotExist:
            error_message = "Invalid email or password"
            return render(request, 'blogapp/login.html', {'error': error_message})
    
    return render(request, 'blogapp/login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if password == re_password:
            if CustomUser.objects.filter(email=email).exists():
                error_message = "Email already exists"
                return render(request, 'blogapp/signup.html', {'error': error_message})
            if CustomUser.objects.filter(mobile=phone).exists():
                error_message = "Phone number already exists"
                return render(request, 'blogapp/signup.html', {'error': error_message})
            if CustomUser.objects.filter(username=name).exists():
                error_message = "Username already exists"
                return render(request, 'blogapp/signup.html', {'error': error_message})
            user = CustomUser.objects.create_user(username=name, email=email, password=password, mobile=phone)
            user.save()
            return render(request, 'blogapp/signup.html', {'success': "Account created successfully"})
        else:
            error_message = "Passwords do not match"
            return render(request, 'blogapp/signup.html', {'error': error_message})
    return render(request, 'blogapp/signup.html')

@login_required(login_url='/login/')
def aboutus(request):
    return render(request, 'blogapp/aboutus.html')

@login_required(login_url='/login/')
def home(request):
    # Get featured blogs (latest 6 posts from all users)
    featured_blogs = Post.objects.all().order_by('-created_at')[:6]

    # Get unique categories for the filter dropdown
    categories = Post.objects.values_list('category', flat=True).distinct().order_by('category')

    context = {
        'featured_blogs': featured_blogs,
        'categories': categories,
    }
    return render(request, 'blogapp/home.html', context)

@login_required(login_url='/login/')
def search_results(request):
    search_query = request.GET.get('search', '').strip()
    search_type = request.GET.get('search_type', 'all')
    category_filter = request.GET.get('category', '')

    results = Post.objects.all()

    # Apply search filters
    if search_query:
        if search_type == 'title':
            results = results.filter(title__icontains=search_query)
        elif search_type == 'author':
            results = results.filter(
                Q(author__username__icontains=search_query) |
                Q(author__first_name__icontains=search_query) |
                Q(author__last_name__icontains=search_query)
            )
        elif search_type == 'category':
            results = results.filter(category__icontains=search_query)
        else:  # search_type == 'all'
            results = results.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query) |
                Q(author__first_name__icontains=search_query) |
                Q(author__last_name__icontains=search_query) |
                Q(category__icontains=search_query)
            )

    # Apply category filter
    if category_filter:
        results = results.filter(category=category_filter)

    results = results.order_by('-created_at')

    # Get unique categories for the filter dropdown
    categories = Post.objects.values_list('category', flat=True).distinct().order_by('category')

    context = {
        'results': results,
        'search_query': search_query,
        'search_type': search_type,
        'category_filter': category_filter,
        'categories': categories,
        'total_results': results.count(),
    }
    return render(request, 'blogapp/search_results.html', context)

@login_required(login_url='/login/')
def settings(request):
    return render(request, 'blogapp/settings.html')

@login_required(login_url='/login/')
def my_blogs(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        content = request.POST.get('content')
        images = request.FILES.get('images')

        if title and category and content:
            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user,
                category=category,
                images=images
            )
            return redirect('my_blogs')

    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blogapp/my_blogs.html', {'posts': user_posts})

@login_required(login_url='/login/')
def blog_detail(request, blog_id):
    post = get_object_or_404(Post, Post_id=blog_id)
    return render(request, 'blogapp/blog_detail.html', {'post': post})

@login_required(login_url='/login/')
def blog_edit(request, blog_id):
    post = get_object_or_404(Post, Post_id=blog_id, author=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        content = request.POST.get('content')
        images = request.FILES.get('images')

        if title and category and content:
            post.title = title
            post.category = category
            post.content = content
            if images:
                post.images = images
            post.save()
            return redirect('blog_detail', blog_id=post.Post_id)

    return render(request, 'blogapp/blog_edit.html', {'post': post})

@login_required(login_url='/login/')
def blog_delete(request, blog_id):
    post = get_object_or_404(Post, Post_id=blog_id, author=request.user)
    post.delete()
    return redirect('my_blogs')

@login_required(login_url='/login/')
@require_POST
def update_profile(request):
    user = request.user
    field = request.POST.get('field')
    value = request.POST.get('value')
    
    if not field or not value:
        return JsonResponse({'success': False, 'message': 'Missing required fields'})
    
    try:
        if field == 'name':
            # Check if username already exists
            user.username = value
            message = 'Name updated successfully'
        elif field == 'email':
            # Check if email already exists
            if CustomUser.objects.filter(email=value).exclude(id=user.id).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists'})
            user.email = value
            message = 'Email updated successfully'
        elif field == 'phone':
            # Check if phone already exists
            if CustomUser.objects.filter(mobile=value).exclude(id=user.id).exists():
                return JsonResponse({'success': False, 'message': 'Phone number already exists'})
            user.mobile = value
            message = 'Phone number updated successfully'
        elif field == 'password':
            user.set_password(value)
            message = 'Password updated successfully'
        else:
            return JsonResponse({'success': False, 'message': 'Invalid field'})
        
        user.save()
        return JsonResponse({'success': True, 'message': message})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required(login_url='/login/')
@require_POST
def delete_account(request):
    try:
        user = request.user
        user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def logout(request):
    auth_logout(request)
    response = redirect('login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response
