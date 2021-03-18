from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('', include('calendarapp.urls')),
	path('', include('accounts.urls')),
    path('', include('management.urls')),
    path('admin/', admin.site.urls),

]
