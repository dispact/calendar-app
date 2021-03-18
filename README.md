# Calendar App

## Features
- User/Staff Auth System
- Users can select date(s) on the calendar to request time off
- Every time off request has to be approved the supervisor
- In the event that an already approved time off request needs to be changed, the user who requested the time off can adjust the request on the calendar. It will need to go through supervisor approval again.
- CRUD User Management System


## Requirements
- django==3.1.5
- django-tailwind==1.1.2
- [SweetAlerts2](https://sweetalert2.github.io/)
- [Dark Theme for SweetAlerts2](https://github.com/sweetalert2/sweetalert2-themes/tree/master/dark)
- [Fullcalendar](https://fullcalendar.io/)

## Notes
#### Initializing the database
1. python manage.py migrate
2. python manage.py shell
3. Paste this into shell: `from calendarapp.models_initial_data import *`
4. Ctrl + Z and then Enter to exit Shell
5. Create super user: `python manage.py createsuperuser`