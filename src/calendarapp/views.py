from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse, HttpResponseNotFound

from itertools import chain

from datetime import date, datetime

from .models import Event, EventTypes, EventStatus

class CalendarView(LoginRequiredMixin, View):
	template_name = "calendarapp/calendar.html"

	def get(self, request, *args, **kwargs):
		approved_status = EventStatus.objects.filter(name='Approved').first()
		pending_status 	= EventStatus.objects.filter(name='Pending').first()
		approved_list 	= Event.objects.filter(status=approved_status).all()
		pending_list 	= Event.objects.filter(status=pending_status).filter(owner=request.user).all()
		event_list 		= chain(approved_list, pending_list)
		event_types 	= EventTypes.objects.all()
		context = {
			"event_list": event_list,
			"current_date": date.today(),
			"event_types": event_types
		}
		return render(self.request, self.template_name, context)

class UserEventView(LoginRequiredMixin, View):
	template_name 	= "calendarapp/user_events.html"

	def get(self, request, *args, **kwargs):
		event_list = Event.objects.filter(owner=request.user).all().order_by('-created_at')
		context = { "event_list": event_list }
		return render(self.request, self.template_name, context)

class AddEvent(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		start	= datetime.strptime(self.convert_date(request.GET.get("start", None)), "%b %d %Y")
		end		= datetime.strptime(self.convert_date(request.GET.get("end", None)), "%b %d %Y")
		typeOf 	= EventTypes.objects.filter(name=request.GET.get('typeOf')).first()
		status 	= EventStatus.objects.filter(name='Pending').first()
		if (Event.objects.filter(typeOf=typeOf, start=start, end=end, owner=request.user).first()):
			return HttpResponseNotFound(JsonResponse({"msg": "This event already exists!"}))
		try:
			event 	= Event(typeOf=typeOf, start=start, end=end, owner=request.user, status=status)
			print("Creating event for ",request.user.get_name())
			event.save()
			data = {
				"status": "success", 
				"title": event.get_event_title(), 
				"id": event.id, 
				"color": typeOf.color.color_code,
				"typeOf": typeOf.name,
				"owner": request.user.email,
				"msg": "Event has been submitted for approval!"
			}
		except Exception as e:
			print('error saving event: ',e)
			data = {"msg":"An error occurred while creating this event."}
			return HttpResponseNotFound(JsonResponse(data))
		return JsonResponse(data)

	def convert_date(self, d):
		temp = d.split(" ")
		new_date = temp[1] + " " + temp[2] + " " + temp[3]
		return new_date

class DeleteEvent(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		event_id = request.GET.get('id', None)
		obj = get_object_or_404(Event, id=event_id)
		if obj.owner != request.user:
			return HttpResponseNotFound(JsonResponse({"msg": "You are not the owner of this event!"}))
		try:
			obj.delete()
			print('Deleting event: ', event_id)
			data = {"msg": "This event has been deleted!"}
		except:
			data = {"msg": "An error occurred while trying to delete this event."}
			return HttpResponseNotFound(JsonResponse(data))
		return JsonResponse(data)

class UpdateEvent(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		event_id	= request.GET.get('id', None)
		obj 		= get_object_or_404(Event, id=event_id)

		if obj.owner != request.user:
			return HttpResponseNotFound(JsonResponse({"msg": "You are not the owner of this event!"}))

		start		= datetime.strptime(self.convert_date(request.GET.get("start", None)), "%b %d %Y")
		end 		= datetime.strptime(self.convert_date(request.GET.get("end", None)), "%b %d %Y")

		if (request.GET.get('typeOf', None)):
			typeOf 		= EventTypes.objects.filter(name=request.GET.get('typeOf')).first()
			obj.typeOf 	= typeOf
		else:
			typeOf = obj.typeOf

		pending_status 	= EventStatus.objects.filter(name='Pending').first()
		obj.status 		= pending_status
		obj.start 		= start
		obj.end 		= end
		try:
			obj.save()
			print('Updating event: ',event_id)
			data = {"msg": 'This has been submitted for approval!'}
		except Exception as e:
			print('Error updating event: ',e)
			data = {"msg": "An error occurred while trying to update this event."}
			return HttpResponseNotFound(JsonResponse(data))
		return JsonResponse(data)

	def convert_date(self, d):
		temp = d.split(" ")
		new_date = temp[1] + " " + temp[2] + " " + temp[3]
		return new_date
		
class ApproveEvent(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		event_id 		= request.GET.get('id', None)
		obj 			= get_object_or_404(Event, id=event_id)
		# if obj.owner == request.user:
		# 	return JsonResponse({"status": "error", "msg": "You can't approve your own status!"}, status=406)
		approved_status = EventStatus.objects.filter(name='Approved').first()
		obj.status 		= approved_status
		try:
			obj.save()
			print('Event #',event_id,' approved by ',request.user)
			data = {"status": "success", "msg": "Event approved!"}
		except Exception as e:
			print('Error approving event #',event_id,': ',e)
			data = {"status": "error", "msg": "An error occurred while approving event."}
			return HttpResponseNotFound(JsonResponse(data));
		return JsonResponse(data)

class DenyEvent(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		event_id 		= request.GET.get('id', None)
		obj 			= get_object_or_404(Event, id=event_id)
		denied_status 	= EventStatus.objects.filter(name='Denied').first()
		obj.status 		= denied_status
		try:
			obj.save()
			print('Event #',event_id,' denied by ',request.user)
			data = {"status": "success", "msg": "Event denied!"}
		except Exception as e:
			print('Error denying event #',event_id,': ',e)
			data = {"status": "error", "msg": "An error occurred while denying event."}
			return HttpResponseNotFound(JsonResponse(data));
		return JsonResponse(data)
