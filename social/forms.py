from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'O que está a pensar?',
            'rows': 3,
            'class': 'post-textarea',
        }),
        max_length=500,
        label='',
    )

    class Meta:
        model = Post
        fields = ['content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Escreva um comentário...',
            'rows': 2,
            'class': 'comment-textarea',
        }),
        max_length=300,
        label='',
    )

    class Meta:
        model = Comment
        fields = ['content']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'auth-input'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'auth-input', 'placeholder': 'Fale sobre si...'}),
        }