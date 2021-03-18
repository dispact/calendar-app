from calendarapp.models import EventColors, EventStatus, EventTypes

EventColors.objects.bulk_create([
	EventColors(color_code='#37D872', name='Green'),
	EventColors(color_code='#9437D8', name='Purple'),
	EventColors(color_code='#D83737', name='Red'),
	EventColors(color_code='#3788d8', name='Blue')
])

EventStatus.objects.bulk_create([
	EventStatus(name='Pending', color='Blue'),
	EventStatus(name='Approved', color='Green'),
	EventStatus(name='Denied', color='Red')
])

EventTypes.objects.bulk_create([
	EventTypes(name='Personal', color=EventColors.objects.filter(name='Blue').first()),
	EventTypes(name='Sick', color=EventColors.objects.filter(name='Red').first()),
	EventTypes(name='Vacation', color=EventColors.objects.filter(name='Purple').first())
])