from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'display_name', 'user_type', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})


    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})



class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfileModel
        fields = '__all__'
        exclude = ['recruiter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})




class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfileModel
        fields = '__all__'
        exclude = ['seeker']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})



class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPostModel
        fields = '__all__'
        exclude = ['posted_by']

        widgets = {
            'deadline': forms.DateInput(attrs={'type':'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})




class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = ApplyJobModel
        fields = '__all__'
        exclude = ['applied_by', 'apply_to']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})
