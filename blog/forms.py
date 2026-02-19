from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from email_validator import validate_email, EmailNotValidError 


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip()
        
        try:
            valid = validate_email(email, check_deliverability=True)
            email = valid.email
        except EmailNotValidError:
            raise forms.ValidationError("This email domain does not exist. Please use a real email.")
        
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Please register using a valid Gmail account only.")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
            
        return email
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile', 'address']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']