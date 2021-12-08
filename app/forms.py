"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _


#Импорт моделей
from .models import News

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class BootstrapRegistrationForm(UserCreationForm):
    """Registration form which uses boostrap CSS."""
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2')
        widgets = { 
                'username' :  forms.TextInput({
                                        'class': 'form-control',
                                        'placeholder': 'Имя пользователя'}),
                'password1' :    forms.PasswordInput({
                                        'class': 'form-control',
                                        'placeholder':'Пароль'}),
                'password2' : forms.PasswordInput({
                                        'class': 'form-control',
                                        'placeholder':'Повторите пароль'}),
                }




class AddNews(forms.ModelForm):
    """AddNews form which uses boostrap CSS."""
    class Meta:
        model = News
        fields = ('title', 'description', 'content', 'image')
        labels = {'title': 'Заголовок', 'description' : 'Краткое содержание', 'content' : 'Полное содержание', 'image' : 'Картинка'}
        widgets = { 
            'title' :  forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Заголовок'}),
            'description' :    forms.Textarea({
                                      'class' : 'form-control',
                                      'placeholder' : 'Краткое содержание'}),
            'content' : forms.Textarea({
                                      'class' : 'form-control',
                                      'placeholder' : 'Текст статьи'}),
            'image' : forms.FileInput({
                                       'class' : 'form-control',
                                      'placeholder' : 'Текст статьи' })
            }



