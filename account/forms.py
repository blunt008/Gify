from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import get_user_model

from .models import Profile


class LoginForm(AuthenticationForm):
        username = forms.CharField(
                max_length=254,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                })
            )
        password = forms.CharField(
                    label=_('Password'),
                    strip=False,
                    widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
                )
        error_messages = {
                'invalid_login': _(
                        'Invalid credentials'
                    ),
                'inactive': _('This account is inactive'),
            }

class ChangePasswordForm(PasswordChangeForm):
        new_password1 = forms.CharField(
                label=_('New password'),
                widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
                strip=False
            )
        new_password2 = forms.CharField(
                label=_('New password confirmation'),
                strip=False,
                widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
            )
        old_password = forms.CharField(
                label=_('Old password'),
                strip=False,
                widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
            )

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={
                                   "class": "form-control"
                               }))
    password2 = forms.CharField(label="Repeat Password",
                                widget=forms.PasswordInput(attrs={
                                    "class": "form-control"
                                }))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={"class": "form-control-file"}
    ))

    class Meta:
        model = get_user_model()
        fields = ("username", )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }

        help_texts = {
            "username": ""
        }



    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        if len(password) < 8:
            msg = "Password is too short. Min. 8 characters."

            self.add_error("password", msg)

class EditUserForm(forms.ModelForm):
    avatar = forms.ImageField(label="Upload new avatar", required=False, widget=forms.FileInput(
        attrs={"class": "form-control-file"}
    ))
    
    class Meta:
        model = Profile
        fields = ("about",)
        widgets = {
            "about": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
