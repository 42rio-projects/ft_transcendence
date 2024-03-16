from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User

class ChangePasswordForm(forms.Form):
	current_password = forms.CharField(label="Current password", widget=forms.PasswordInput)
	new_password = forms.CharField(label="New password", widget=forms.PasswordInput, validators=[validate_password])
	new_password_confirm = forms.CharField(label="Confirm new password", widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super().clean()
		new_password = cleaned_data.get('new_password')
		new_password_confirm = cleaned_data.get('new_password_confirm')

		if new_password != new_password_confirm:
			raise forms.ValidationError("Passwords do not match")

		return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']
