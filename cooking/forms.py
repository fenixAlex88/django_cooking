from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class PostAddForm(forms.ModelForm):
    """Форма добавления новой статьи от пользователя"""

    class Meta:
        model = Post
        fields = ('title', 'content', 'photo', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    """Форма аунтификации пользователя"""
    username = forms.CharField(label="Имя пользователя", 
                               max_length=150, 
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль",
                               min_length=4,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control'}))

class RegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    username = forms.CharField(label="Имя пользователя",
                            max_length=150,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control',
                                        'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label="Электронная почта",
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control',
                                        'placeholder': 'Электронная почта'}))
    password1 = forms.CharField(label="Пароль",
                            widget=forms.PasswordInput(
                                attrs={'class': 'form-control',
                                        'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Подтвердить пароль",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                        'placeholder': 'Подтвердить пароль'}))

class CommentForm(forms.ModelForm):
    """Форма созлания комментария"""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст вашего комментария'})}