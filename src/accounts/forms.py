from django.contrib.auth import get_user_model
from django import forms
from django.contrib import messages

User = get_user_model()

class RegisterForm(forms.Form):
	first_name = forms.CharField(
		label='First Name',
		widget=forms.TextInput(
			attrs={
				"class": "appearance-none rounded-none bg-gray-700 relative block w-full px-3 py-2 border border-gray-500 placeholder-gray-300 text-gray-200 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm",
				"required": True,
				"placeholder": "First Name",
			}
		)
	)
	last_name = forms.CharField(
		label='Last Name',
		widget=forms.TextInput(
			attrs={
				"class": "appearance-none rounded-none bg-gray-700 relative block w-full px-3 py-2 border border-gray-500 placeholder-gray-300 text-gray-200 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm",
				"required": True,
				"placeholder": "Last Name",
			}
		)
	)
	email = forms.EmailField(
		widget=forms.EmailInput(
			attrs={
				"class": "appearance-none rounded-none bg-gray-700 relative block w-full px-3 py-2 border border-gray-500 placeholder-gray-300 text-gray-200 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm",
				"autofocus": True,
				"required": True,
				"placeholder": "Email",
			}
		)
	)
	password1 = forms.CharField(
		label='Password',
		widget=forms.PasswordInput(
			attrs={
				"class": "appearance-none rounded-none bg-gray-700 relative block w-full px-3 py-2 border border-gray-500 placeholder-gray-300 text-gray-200 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm",
				"required": True,
				"placeholder": "Password",
			}
		)
	)
	password2 = forms.CharField(
		label='Confirm Password',
		widget=forms.PasswordInput(
			attrs={
				"class": "appearance-none rounded-none bg-gray-700 relative block w-full px-3 py-2 border border-gray-500 placeholder-gray-300 text-gray-200 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm",
				"required": True,
				"placeholder": "Verify password",
			}
		)
	)

	def clean_email(self):
		email = self.cleaned_data.get("email")
		qs = User.objects.filter(email__iexact=email)
		if qs.exists():
			raise forms.ValidationError("That email is already in use")
		return email

	def clean_password2(self):
		password2 = self.cleaned_data.get('password2')
		if password2 != self.cleaned_data['password1']:
			raise forms.ValidationError('Passwords do not match!')
		return password2


class LoginForm(forms.Form):
	email = forms.EmailField(
		widget=forms.EmailInput(
			attrs={
				"class": "appearance-none rounded-none bg-gray-700 relative block w-full px-3 py-2 border border-gray-500 placeholder-gray-300 text-gray-200 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm",
				"autofocus": True,
				"required": True,
				"placeholder": "Email",
			}
		)
	)
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				"class": "appearance-none rounded-none bg-gray-700 relative block w-full px-3 py-2 border border-gray-500 placeholder-gray-300 text-gray-200 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm",
				"required": True,
				"placeholder": "Password",
			}
		)
	)

	def clean_email(self):
		email = self.cleaned_data.get("email")
		qs = User.objects.filter(email__iexact=email)
		if not qs.exists():
			return messages.add_message(request, messages.ERROR, 'This email already exists!')
		return email