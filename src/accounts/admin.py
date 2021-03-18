from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User

class UserCreationForm(forms.ModelForm):
	first_name = forms.CharField(label='First Name', widget=forms.TextInput())
	last_name = forms.CharField(label='Last Name', widget=forms.TextInput())
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Verify Password', widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise ValidationError('Passwords do not match!')
		return password2

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'password', 'first_name', 'last_name', 'active')

	def clean_password(self):
		return self.initial['password']

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'first_name', 'last_name', 'active', 'staff', 'admin')
	list_filter = ('active', 'staff', 'admin')
	fieldsets = (
		(None, {'fields': ('email', 'password', 'active')}),
		('Personal Info', {'fields': ('first_name', 'last_name')}),
		('Leave Time', {'fields': ('personal_days', 'vacation_days', 'sick_days')}),
		('Permissions', {'fields': ('staff', 'admin')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
		}),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)