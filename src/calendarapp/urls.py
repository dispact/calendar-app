from django.urls import path
from .views import (
	CalendarView,
	AddEvent,
	DeleteEvent,
	UpdateEvent,
	ApproveEvent,
	DenyEvent,
	UserEventView
)

app_name="calendarapp"
urlpatterns = [
	path('', CalendarView.as_view(), name="calendar"),
	path('events', UserEventView.as_view(), name='events'),
	path('event/add/', AddEvent.as_view(), name="add-event"),
	path('event/delete/', DeleteEvent.as_view(), name="delete-event"),
	path('event/update/', UpdateEvent.as_view(), name="update-event"),
	path('event/approve/', ApproveEvent.as_view(), name="approve-event"),
	path('event/deny/', DenyEvent.as_view(), name="deny-event")

]