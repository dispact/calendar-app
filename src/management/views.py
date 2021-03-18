import re
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseNotFound
from django.views import View
from calendarapp.models import EventStatus, Event

User = get_user_model()

# User Settings
class SettingsView(LoginRequiredMixin, View):
	template_name = 'management/settings.html'

	def get(self, request, *args, **kwargs):
		context = {"first_name": self.request.user.first_name or '', "last_name": self.request.user.last_name or ''}
		return render(self.request, self.template_name, context)

# Admin User Management
class UserManagementView(LoginRequiredMixin, UserPassesTestMixin, View):
	def test_func(self):
		return self.request.user.is_staff

	template_name = 'management/user_management.html'

	def get(self, request, *args, **kwargs):
		user_list = User.objects.all()
		context = {"user_list": user_list}
		return render(self.request, self.template_name, context)

# Supervisor Board
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
	def test_func(self):
		return self.request.user.is_staff

	template_name 	= "management/dashboard.html"

	def get(self, request, *args, **kwargs):
		print(User.objects.get(pk=self.request.user.id).last_login)
		status_id 	= EventStatus.objects.filter(name='Pending').first()
		event_list 	= Event.objects.filter(status=status_id).all()
		context 	= {"event_list": event_list}
		return render(self.request, self.template_name, context)

class SaveSettings(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		first_name 		= request.GET.get("first_name", None)
		last_name 		= request.GET.get("last_name", None)
		if (first_name == '' or None) or (last_name == '' or None):
			return HttpResponseNotFound(JsonResponse({"msg": "Fields cannot be empty!"}))
		if (first_name == request.user.first_name) and (last_name == request.user.last_name):
			return JsonResponse({"msg": "Settings have successfully been saved!"})
		obj 			= User.objects.filter(email=request.user.email).first()
		obj.first_name 	= first_name
		obj.last_name 	= last_name
		try:
			obj.save()
			print('Updating user: ', request.user)
			data = {"msg": "Settings have successfully been saved!"}
		except Exception as e:
			print('Error updating user: ',e)
			data = {"msg": "An error occurred while trying to save settings."}
			return HttpResponseNotFound(JsonResponse(data))
		return JsonResponse(data)


class CreateUser(LoginRequiredMixin, UserPassesTestMixin, View):
	def test_func(self):
		return self.request.user.is_staff

	def get(self, request, *args, **kwargs):
		first_name	= request.GET.get("first_name", None)
		last_name 	= request.GET.get("last_name", None)
		email 		= request.GET.get("email", None)
		password 	= request.GET.get("password", None)
		staff 		= request.GET.get("staff", False)

		print(request.GET)

		if None not in (first_name, last_name, email, password):
			pass
		else:
			return HttpResponseNotFound(JsonResponse({"msg": "Please fix the empty fields!"}))

		if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			return HttpResponseNotFound(JsonResponse({"msg": "Please enter a valid email address!"}))

		if User.objects.filter(email=email).count() >= 1:
			return HttpResponseNotFound(JsonResponse({"msg": "An account with that email address already exists!"}))
		
		try:
			new_user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name)
			new_user.set_password(password)
			print('staff: ',staff)
			if (staff == 'true'):
				new_user.staff = True
				new_user.save()
			print('User "',email,'" created by '+self.request.user.email)
			data = {"msg": "User successfully created!", "id": new_user.id, "name": new_user.get_name(), "email": new_user.email, "staff": new_user.is_staff}
		except Exception as e:
			print('Error creating user: ',e)
			return HttpResponseNotFound(JsonResponse({"msg": "An unexpected error occurred."}))
		return JsonResponse(data)

class DeleteUser(LoginRequiredMixin, UserPassesTestMixin, View):
	def test_func(self):
		return self.request.user.is_staff

	def get(self, request, *args, **kwargs):
		user_id = request.GET.get('id', None)
		if user_id is None: 
			return HttpResponseNotFound(JsonResponse({"msg": "Invalid user"}))
		try:
			user = User.objects.filter(pk=user_id).first()
			user.delete()
			data = {"msg": "User successfully deleted!"}
		except Exception as e:
			print('Error deleting user: ',e)
			return HttpResponseNotFound(JsonResponse({"msg": "An unexpected error occured."}))
		return JsonResponse(data)

class UpdateUser(LoginRequiredMixin, UserPassesTestMixin, View):
	def test_func(self):
		return self.request.user.is_staff

	def get(self, request, *args, **kwargs):
		user_id = request.GET.get('id', None)
		if user_id is None:
			return HttpResponseNotFound(JsonResponse({'msg': 'Invalid user'}))

		first_name 	= request.GET.get('first_name', None)
		last_name 	= request.GET.get('last_name', None)
		email 		= request.GET.get('email', None)

		if None not in (first_name, last_name, email):
			pass
		else:
			return HttpResponseNotFound(JsonResponse({'msg': 'Please fill out all the fields!'}))

		try: 
			user = User.objects.filter(pk=user_id).first()
			if user is None:
				return HttpResponseNotFound(JsonResponse({'msg': 'User does not exist!'}))
			user.first_name = first_name
			user.last_name 	= last_name
			user.email 		= email
			user.save()
			data = {'msg': 'User successfully updated!'}
			print('User ', user_id, ' updated by ',request.user)
		except Exception as e:
			print('Error updating user ',user_id,' -> ',e)
			return HttpResponseNotFound(JsonResponse({'msg': 'An unexpected error occured'}))
		return JsonResponse(data)
