from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django import forms
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RegisterView(CreateView):
    """View for user registration."""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('destinations:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Create user profile
        UserProfile.objects.create(user=self.object)
        
        # Automatically log in the user
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        if user:
            login(self.request, user)
            messages.success(self.request, f'Welcome {user.username}! Your account has been created.')
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Register'
        return context


class LoginView(FormView):
    """View for user login."""
    template_name = 'users/login.html'
    form_class = forms.Form
    success_url = reverse_lazy('destinations:home')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if form_class is None:
            class LoginForm(forms.Form):
                username = forms.CharField(label='Username or Email', max_length=100)
                password = forms.CharField(widget=forms.PasswordInput, label='Password')
                remember_me = forms.BooleanField(required=False, label='Remember me')
            
            return LoginForm()
        return form
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        # Try to authenticate with username or email
        user = User.objects.filter(username=username).first()
        if not user:
            user = User.objects.filter(email=username).first()
        
        if user:
            user = authenticate(username=user.username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Remember me functionality
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            
            next_page = request.GET.get('next', 'destinations:home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Login'
        return context


class LogoutView(LoginRequiredMixin, View):
    """View for user logout."""
    login_url = 'users:login'
    
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('destinations:home')


class UserProfileView(LoginRequiredMixin, DetailView):
    """View to display user profile."""
    model = UserProfile
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    login_url = 'users:login'
    
    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View to update user profile."""
    model = UserProfile
    template_name = 'users/profile_update.html'
    fields = ['phone', 'address', 'city', 'country', 'postal_code', 'bio', 'profile_picture', 'date_of_birth']
    success_url = reverse_lazy('users:profile')
    login_url = 'users:login'
    
    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
