from django.contrib import admin
from .models import Event, EventTypes, EventColors, EventStatus

def make_pending(modeladmin, request, queryset):
	pending = EventStatus.objects.filter(name='Pending').first()
	queryset.update(status=pending)
make_pending.short_description = "Mark selected events as pending"

class EventAdmin(admin.ModelAdmin):
	list_display = ('owner', 'typeOf', 'status', 'start', 'end')
	actions = [make_pending]

class EventTypesAdmin(admin.ModelAdmin):
	list_display = ('name', 'color')

class EventColorsAdmin(admin.ModelAdmin):
	list_display = ('color_code', 'name')

class EventStatusAdmin(admin.ModelAdmin):
	list_display = ('name', 'color')

admin.site.register(Event, EventAdmin)
admin.site.register(EventTypes, EventTypesAdmin)
admin.site.register(EventColors, EventColorsAdmin)
admin.site.register(EventStatus, EventStatusAdmin)