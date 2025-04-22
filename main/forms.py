from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    type = forms.ChoiceField(choices=[('', '---')] + list(UserProfile.USER_TYPES))
    class Meta: 
        model = User
        fields = ['username', 'email', 'password']
    def clean_username(self): 
        username = self.cleaned_data.get('username')
        if User.objects.filter(username = username).exists():
            raise ValidationError("Username is taken")
        return username 

    def clean_email(self): 
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise ValidationError("Email is taken")
        return email 
        
    def save(self, commit=True): 
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit: 
            user.save()
        return user
    
    
class LoginForm(forms.Form): 
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username not found.")
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # We can only check password if username is already entered and valid
        if username and password and User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Incorrect password.")
        return password
    
class EventForm(ModelForm):
    class Meta: 
        model = Events
        fields = ['event_name', 'event_description', 'max_tickets_no', 'end_date', 'price']
        widgets = {
            'event_name' : forms.Textarea(attrs={'rows' : 1, 'placeholder' : 'Write your event name here...',  'class' : 'form-control'}),
            'event_description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your event description here...', 'class': 'form-control'}), 
            'max_tickets_no':forms.NumberInput(attrs={'class' : 'form-control'}),
            'end_date' :forms.DateInput(attrs={'type' : 'date', 'class' : 'form-control'}),
            'price' : forms.NumberInput(attrs={'class' : 'form-control'}),
        }
    

    