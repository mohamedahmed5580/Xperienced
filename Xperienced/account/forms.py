from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    csrfmiddlewaretoken = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','phone']

    def clean_password(self):
        # This method ensures that the password is cleaned properly
        return self.cleaned_data['password']
class EditAboutForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['description']
class EditImageProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']

# class ApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Application
#         fields = ['firstName', 'lastName', 'email', 'phoneNumber', 'lastCompany', 'dateOfBirth', 'Address', 'ZipCode', 'City', 'ApplicationLetter', 'CV']

# class SignUpUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'password',
#             'password1', 
#             'companyCheck', 
#             'companyName',
#             'is_admin',
#         )