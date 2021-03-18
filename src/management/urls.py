from django.urls import path
from .views import (
	SettingsView, 
	UserManagementView, 
	DashboardView,
	SaveSettings,
	CreateUser,
	DeleteUser,
	UpdateUser
)

app_name="management"
urlpatterns = [
	path('settings', SettingsView.as_view(), name="settings"),
	path('users', UserManagementView.as_view(), name="users"),
	path('dashboard', DashboardView.as_view(), name='dashboard'),

	path('settings/save/', SaveSettings.as_view(), name="save-settings"),
	path('users/create/', CreateUser.as_view(), name="create-user"),
	path('users/delete/', DeleteUser.as_view(), name="delete-user"),
	path('users/update/', UpdateUser.as_view(), name="update-user")
]
