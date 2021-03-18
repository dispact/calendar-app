from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class EventStatus(models.Model):
	name 	= models.CharField(max_length=24, unique=True)
	color 	= models.CharField(max_length=10, unique=True)

	def __str__(self):
		return self.name

class EventColors(models.Model):
	color_code 		= models.CharField(max_length=10, null=False, unique=True)
	name 			= models.CharField(max_length=24, null=True, unique=True)
	
	def __str__(self):
		return self.name

class EventTypes(models.Model):
	name 	= models.CharField(max_length=24, unique=True)
	color 	= models.ForeignKey(EventColors, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.name

class Event(models.Model):
	owner		= models.ForeignKey(User, null=False, on_delete=models.CASCADE)
	typeOf		= models.ForeignKey(EventTypes, on_delete=models.CASCADE)
	status 		= models.ForeignKey(EventStatus, on_delete=models.CASCADE) 
	start 		= models.DateField()
	end			= models.DateField(null = True, blank = True)
	created_at 	= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.owner.get_name()

	def get_event_title(self):
		return self.owner.get_name() + ' ' + self.typeOf.name + ' ' + 'Time'