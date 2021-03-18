from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms

from .forms import LoginForm, RegisterForm

User = get_user_model()

def register_view(request):
	if (request.user.is_authenticated):
		return redirect("/")
	template_name = "accounts/register.html"
	default_avatar = 'avatars/default.png'
	form = RegisterForm(request.POST or None)
	context = { "form": form }
	if form.is_valid():
		email 		= form.cleaned_data.get("email")
		password1 	= form.cleaned_data.get("password1")
		password2 	= form.cleaned_data.get("password2")
		first_name 	= form.cleaned_data.get("first_name")
		last_name 	= form.cleaned_data.get('last_name')
		try:
			user = User.objects.create_user(email=email, password=password1, first_name=first_name, last_name=last_name)
		except:
			user = None
		if user != None:
			login(request, user)
			return redirect("/")
		else:
			request.session["registration_error"] = 1
	return render(request, template_name, context)
		
def login_view(request):
	if (request.user.is_authenticated):
		return redirect("/")
	template_name = "accounts/login.html"
	form = LoginForm(request.POST or None)
	context = { "form": form }
	if form.is_valid():
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		user = authenticate(request, email=email, password=password)
		if user != None:
			login(request, user)
			return redirect('/')
		#else:
			# attempt = request.session.get("attempt") or 0
			# request.session['attempt'] = attempt + 1
			#request.session['invalid_user'] = 1
	return render(request, template_name, context)

@login_required
def logout_view(request):
	logout(request)
	return redirect("/login")

