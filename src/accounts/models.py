from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MinValueValidator

class UserManager(BaseUserManager):

	def create_user(self, email, password=None, first_name=None, last_name=None):
		if not email:
			raise ValueError('Users must have an email address!')
		user = self.model(
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name,
		)
		user.set_password(password)
		user.save()
		return user

	def create_staffuser(self, email, password, first_name=None, last_name=None):
		user = self.create_user(
			email=email,
			password=password,
			first_name=first_name,
			last_name=last_name,
		)
		user.staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password, first_name=None, last_name=None):
		user = self.create_user(
			email=email,
			password=password,
			first_name=first_name,
			last_name=last_name,
		)
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email 			= models.EmailField(max_length=255, unique=True)
	first_name 		= models.CharField(verbose_name='First Name', max_length=126, null=True)
	last_name 		= models.CharField(verbose_name='Last Name', max_length=126, null=True)
	sick_days 		= models.FloatField(verbose_name='Sick Days', default=0.0, validators=[MinValueValidator(0.0)])
	personal_days 	= models.FloatField(verbose_name='Personal Days', default=0.0, validators=[MinValueValidator(0.0)])
	vacation_days 	= models.FloatField(verbose_name='Vacation Days', default=0.0, validators=[MinValueValidator(0.0)])
	active 			= models.BooleanField(default=True)
	staff 			= models.BooleanField(default=False)
	admin 			= models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	def __str__(self):
		return self.email

	def get_name(self):
		if None not in (self.first_name, self.last_name):
			return self.first_name + ' ' + self.last_name
		else:
			return ''

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin
	
	@property
	def is_active(self):
		return self.active