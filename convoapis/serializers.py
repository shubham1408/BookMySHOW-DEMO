from django.contrib.auth.models import User, Group
from .models import UserProfile, Movie, Cinema, Shows, Ticket
from rest_framework import serializers
from django.core.validators import (MinLengthValidator, 
    MaxLengthValidator, validate_integer)
from .choices import GENDER_CHOICES, STATUS_CHOICES, INACTIVE, ACTIVE


class UserSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return super().to_internal_value(data)
    
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'name', 'password',
                  'is_superuser', 'phone_no', 'gender', 
                  'is_staff']


class GroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = ['url', 'name']


class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ['name', 'genre', 'released_date', 'status']
        # exclude= ['added_on', 'updated_on']


class CinemaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cinema
        fields = ['name', 'no_of_seats', 'no_of_screens', 
            'opening_time', 'closing_time', 'status', 
            'city', 'address']


class ShowCreateListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shows
        fields = '__all__'


class ShowSerializer(serializers.ModelSerializer):
    cinema_name = serializers.CharField(source='cinema.name')
    cinema_no_of_seats = serializers.IntegerField(source='cinema.no_of_seats')
    cinema_no_of_screens = serializers.CharField(source='cinema.no_of_screens')
    cinema_opening_time = serializers.DateTimeField(source='cinema.opening_time')
    cinema_closing_time = serializers.DateTimeField(source='cinema.closing_time')
    city = serializers.CharField(source='cinema.city')
    address = serializers.CharField(source='cinema.address')
    
    class Meta:
        model = Shows
        fields = ['cinema_name', 'cinema_no_of_seats', 
        'cinema_no_of_screens', 'cinema_opening_time', 
        'cinema_closing_time', 'city', 'address', 'show_time']


class ShowTimeSeatAvailaibileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shows
        fields = ['show_time', 'ticket_left']


class TicketSerializer(serializers.ModelSerializer):

    Movie_Name = serializers.ChoiceField(choices=list(
        Movie.objects.all().values_list('name', flat=True)))
    Ticket_Price = serializers.ChoiceField(choices=list(
        Shows.objects.all().values_list('ticket_cost', flat=True)))
    User_Name = serializers.ChoiceField(choices=list(
        UserProfile.objects.all().values_list('username', flat=True)))
    Show_Time = serializers.ChoiceField(choices=list(
        Shows.objects.all().values_list('show_time', flat=True)))


    def create(self, validated_data):
        data = {
            'ticket_user': UserProfile.objects.get(
                username=validated_data.get('User_Name')),
            'show': Shows.objects.get(
                show_time=validated_data.get('Show_Time')),
            'qr_code': 'gdgfgf',
            'sold_at': validated_data.get('Ticket_Price'),
            'status': ACTIVE
        }
        return Ticket.objects.create(**data)

    
    class Meta:
        model=Ticket
        field = ['Movie_Name', 'Ticket_Price', 'User_Name', 'Show_Time']
        exclude = ['ticket_user', 'show', 'qr_code', 'sold_at', 'status']


class TicketViewSerializer(serializers.ModelSerializer):

    class Meta:
        model=Ticket
        fields = '__all__'
