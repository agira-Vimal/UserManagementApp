from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from django.core import validators
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
import re


class CustomUserForm(UserCreationForm):
    def validating_username(value):
        if not value.isalpha():
            raise ValidationError("Username Must be Characters Only!")

    def validating_email(value):
        if "@" not in value:
            raise ValidationError("Please Enter a valid Email ID containing '@'")
        email_pattern = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
        if not email_pattern.match(value):
            raise ValidationError("Please Enter a Valid Email ID")

    def validating_password(value):
        special_characters_pattern = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
        if not special_characters_pattern.search(value):
            raise ValidationError(
                "Please Enter a Password Containg atleast 1 special character"
            )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter User Name"}
        ),
        error_messages={"required": "Please Enter Your Username"},
        min_length=3,
        validators=[validating_username],
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Email Address"}
        ),
        error_messages={"required": "Please Enter Your Email"},
        validators=[validating_email],
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Your Password"}
        ),
        error_messages={"required": "Please Enter Your Password"},
        validators=[validating_password],
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Your Password"}
        ),
        error_messages={"required": "Please Enter Your Confirm Password"},
        validators=[validating_password],
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserProfileForm(forms.ModelForm):
    def validating_phone_number(value):
        if value:
            if len(str(value)) < 10:
                raise ValidationError("Phone Number must Contain 10 digits")
            if not value.is_valid():
                raise ValidationError("Please enter a valid phone number.")
        else:
            raise ValidationError("Phone Number is Mandatory")

    
    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Your Last Name"}
        ),
        required=False,
    )

    phone_number = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Phone Number (E.g., +919876543210)",
            }
        ),
        validators=[validating_phone_number],
        required=False,
    )

    address_line_1 = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Address Line 1"}
        ),
        required=False,
    )

    address_line_2 = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Address Line 2"}
        ),
        required=False,
    )

    postcode = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Postcode"}
        ),
        required=False,
    )

    state = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter State"}
        ),
        required=False,
    )

    country = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Country"}
        ),
        required=False,
    )

    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}), required=False
    )

    class Meta:
        model = UserProfile
        fields = [
            "surname",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "postcode",
            "state",
            "country",
            "profile_picture",
        ]
