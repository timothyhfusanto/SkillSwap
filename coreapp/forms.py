from django import forms
from .models import *
from accounts.models import User
from django.core.validators import DecimalValidator


class ServiceListingForm(forms.ModelForm):
    relatedskilltag = forms.ModelMultipleChoiceField(queryset=skilltag.objects.all())

    class Meta:
        model = ServiceListing
        fields = ['nameofservice', 'image', 'details', 'relatedskilltag', 'hourlyCharge', 'skill']
        widgets = {
            'nameofservice': forms.TextInput(attrs={'class': 'form-control shadow-none', 'placeholder': 'Please state directly the service you will provide EG. I will help/create/do...', "autofocus":"true"}),
            'hourlyCharge': forms.NumberInput(attrs={'class': 'form-control shadow-none', 'placeholder': 'Hourly Charge', 'step': '0.01'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description here'}),
            'skill': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Skill Offered'}),
            'image': forms.FileInput(attrs={'onchange': "loadFile(event)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False  # Make the image field optional


class SkillSwapListingForm(forms.ModelForm):
    new_skill_name = forms.CharField(max_length=255, required=False, label='New Skill Name')
    new_skill_name_wanted = forms.CharField(max_length=255, required=False, label='New Skill Name Wanted')

    class Meta:
        model = SkillSwapListing
        fields = ['nameofservice', 'image', 'details', 'skill_offered', 'optional_skill_wanted']
        widgets = {
            'nameofservice': forms.TextInput(attrs={'class': 'form-control shadow-none',
                                                    'placeholder': 'Please state directly the skill you are offering (e.g Offering Python Coding)'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description here (e.g I am looking for..)'}),
            'skill_offered': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Skill Offered'}),
            'optional_skill_wanted': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Skill Wanted'}),
            'image': forms.FileInput(attrs={'onchange': "loadFile(event)"}),
        }
        
class EditServiceForm(forms.ModelForm):
    relatedskilltag = forms.ModelMultipleChoiceField(queryset=skilltag.objects.all())
    class Meta:
        model = ServiceListing
        fields = ['nameofservice', 'details', 'image', 'relatedskilltag', 'hourlyCharge', 'skill']
        placeholders = {
            'nameofservice': 'Enter the name of the service',
            'details': 'Enter the details',
            'hourlyCharge': 'Enter the hourly charge',
            'relatedskilltag': 'Enter related skill tags',
            'image': 'Choose an image',
            'skill': 'Select a skill',
        }
        widgets = {
            'nameofservice': forms.TextInput(
                attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['nameofservice']}),
            'details': forms.Textarea(
                attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['details']}),
            'hourlyCharge': forms.NumberInput(
                attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['hourlyCharge']}),
            'image': forms.FileInput(attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['image']}),
            'skill': forms.TextInput(
                attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['skill']}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                placeholder = self.Meta.placeholders.get(field_name)
                if placeholder:
                    field.widget.attrs['placeholder'] = placeholder

class EditSkillSwapForm(forms.ModelForm):
    class Meta:
        model = SkillSwapListing
        fields = ['nameofservice', 'details', 'image', 'relatedskilltag', 'skill_offered', 'optional_skill_wanted']
        placeholders = {
            'nameofservice': 'Enter the name of the service',
            'details': 'Enter the details',
            'skill_offered': 'Enter the skill offered',
            'optional_skill_wanted': 'Enter optional skill wanted',
            'image': 'Choose an image',
        }
        widgets = {
            'nameofservice': forms.TextInput(attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['nameofservice']}),
            'details': forms.Textarea(attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['details']}),
            'skill_offered': forms.TextInput(attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['skill_offered']}),
            'optional_skill_wanted': forms.TextInput(attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['optional_skill_wanted']}),
            'image': forms.FileInput(attrs={'class': 'form-control shadow-none', 'placeholder': placeholders['image']}),
            'relatedskilltag': forms.SelectMultiple(attrs={'class': 'form-control shadow-none'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            placeholder = self.Meta.placeholders.get(field_name)
            if placeholder:
                field.widget.attrs['placeholder'] = placeholder

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'description', 'age', 'academicYear', 'phoneNum', 'image', 'email', 'username', 'major']  # Add all relevant fields here
        placeholders = {
            'name': 'Enter your name',  # Default placeholder value
            'email': 'Enter your email',
            'description': 'Enter your description',
            'age': 'Enter your age',
            'academicYear': 'Enter your academic year',
            'major': 'Enter your major',
            'phoneNum': 'Enter your phone number',
            'username': 'Enter your username'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control shadow-none', "autofocus":"true"}),
            'description': forms.Textarea(attrs={'class': 'form-control shadow-none', "style":"height:100px"}),
            'email': forms.EmailInput(attrs={'class': 'form-control shadow-none'}),
            'age': forms.NumberInput(attrs={'class': 'form-control shadow-none'}),
            'academicYear': forms.Select(attrs={'class': 'form-control shadow-none'}),
            'phoneNum': forms.NumberInput(attrs={'class': 'form-control shadow-none'}),
            'username': forms.TextInput(attrs={'class': 'form-control shadow-none'}),
            'major' : forms.TextInput(attrs={'class': 'form-control shadow-none'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            # You can add more widgets for image field if needed
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            placeholder = self.Meta.placeholders.get(field_name)
            if placeholder:
                field.widget.attrs['placeholder'] = placeholder
                
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', "placeholder": "comment", "style": "height:100px", "name":"text"}),
        }

        
class ServiceListingPurchaseForm(forms.ModelForm):
    class Meta:
        model = ServiceListingPurchase
        fields = ['message']


class SkillSwapOfferForm(forms.ModelForm):
    class Meta:
        model = SkillSwapOffer
        fields = ['skill_offered', 'message']
        


