from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django.contrib.auth import password_validation

class UserRegisterForm(UserCreationForm):
    ACADEMIC_YEAR_CHOICES = (
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year')
    )
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control shadow-none", "placeholder": "Name", "autofocus":"true"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control shadow-none", "placeholder": "Description", "style":"height:100px"}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control shadow-none", "placeholder": "Age"}))
    academicYear = forms.ChoiceField(choices=ACADEMIC_YEAR_CHOICES,
                                     widget=forms.Select(attrs={"class": "form-control shadow-none"}))
    major = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control shadow-none", "placeholder": "Major"}))
    phoneNum = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control shadow-none", "placeholder": "Phone Number"}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control shadow-none", "placeholder": "Image"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control shadow-none", "placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control shadow-none", "placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control shadow-none", "placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control shadow-none", "placeholder": "Confirm Password"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove default password validators
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
        self.fields['description'].required = False 

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Remove email similarity validation
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            if password1 and email:
                if password1.lower() == email.lower():
                    raise forms.ValidationError("The password cannot be too similar to the email.")
        # Custom validation for minimum length and commonality
        try:
            password_validation.validate_password(password1)
        except forms.ValidationError as error:
            # This will raise a validation error with messages from all validators
            raise forms.ValidationError(list(error.messages))
        return password1

    class Meta:
        model = User
        fields = ['name', 'description', 'age', 'academicYear', 'major', 'phoneNum', 'image', 'username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Name"}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Age"}))
    phoneNum = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Phone Number"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"placeholder": "Image"}))

    class Meta:
        model = User
        fields = ["name", 'image', 'age', 'academicYear', 'phoneNum']