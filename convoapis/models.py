from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser,
    BaseUserManager, PermissionsMixin)
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password)
from django.core.validators import (MinLengthValidator, 
    MaxLengthValidator, validate_integer)
from django.utils.translation import ugettext_lazy as _
from .choices import GENDER_CHOICES, STATUS_CHOICES, INACTIVE, ACTIVE


class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, name, password=None):
        user = self.model(
            username=username,
            name=name,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password):
        user = self.create_user(email=email,
                                password=password,
                                username=username,
                                name=name
                                )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=250, default='')
    name = models.CharField(max_length=255)
    phone_no = models.CharField(
        max_length=255, validators=[MaxLengthValidator(14),
        MinLengthValidator(10), validate_integer],
        null=False, unique=True)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, null=True)
    wallet = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        if self.email:
            return self.email
        else:
            return self.name

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(UserProfile, self).save(*args, **kwargs)

    class Meta(AbstractBaseUser.Meta):
        db_table = 'userprofile'


class Cinema(models.Model):
    
    name = models.CharField(max_length=255)
    no_of_seats = models.IntegerField(null=False)
    no_of_screens = models.IntegerField(default=1)
    opening_time = models.TimeField(null=False)
    closing_time = models.TimeField(null=False)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, null=False)
    city = models.CharField(null=False, max_length=255)
    address = models.CharField(null=False, max_length=255)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cinema'


class Movie(models.Model):
    
    name = models.CharField(max_length=255, null=False)
    genre = models.TextField()
    released_date = models.DateField(null=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, null=False)

    class Meta:
        db_table = 'movie'


class Shows(models.Model):

    movie = models.ForeignKey(Movie, 
        on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, 
        on_delete=models.CASCADE)
    show_time = models.DateTimeField(null=False)
    ticket_left = models.IntegerField(null=False)
    ticket_cost = models.FloatField(null=False)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=ACTIVE, 
        null=False)  # Show running check
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        return super(Shows, self).save(*args, **kwargs) 

    class Meta:
        db_table = 'shows'

    

class Ticket(models.Model):
    
    ticket_user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE)
    show = models.ForeignKey('Shows', 
        on_delete=models.CASCADE)
    qr_code = models.CharField(max_length=255)
    sold_at = models.FloatField(null=False)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=ACTIVE, 
        null=False) # Ticket cancellation check

    def save(self, *args, **kwargs):
        return super(Ticket, self).save(*args, **kwargs)    

    class Meta:
        db_table = 'ticket'



