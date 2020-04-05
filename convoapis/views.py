import pytz
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import (status, permissions, 
                            authentication, generics, 
                            renderers)
from .serializers import (UserSerializer, GroupSerializer, 
                          MovieSerializer, CinemaSerializer, 
                          ShowCreateListSerializer, ShowSerializer, 
                          ShowTimeSeatAvailaibileSerializer, TicketSerializer,
                          TicketViewSerializer)
from .models import (UserProfile, Movie, Cinema, Shows, Ticket)
from dateutil import parser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CinemaAPI(generics.ListCreateAPIView):
    serializer_class = CinemaSerializer
    
    def get_queryset(self):
        cinema = Cinema.objects.all()
        return cinema


class ShowCreateListAPI(generics.ListCreateAPIView):
    serializer_class = ShowCreateListSerializer

    def get_queryset(self):
        cinema = Shows.objects.all()
        return cinema 


class TicketListAPI(generics.ListAPIView):

    queryset = Ticket.objects.all()
    serializer_class = TicketViewSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserListAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()



class MoviesByCity(generics.ListCreateAPIView):
    """
    API to retrieve all movies by city

    To search movie by city one has to append the url 
    with ?city=city_name
    """
    serializer_class = MovieSerializer
    
    def get_queryset(self):
        movie_ids = list(Shows.objects.filter(
            cinema__city=self.request.query_params.get(
                'city')).values_list(
            'movie_id', flat=True))
        movies = Movie.objects.filter(id__in=movie_ids)
        return movies


class CinemasByMovie(generics.ListCreateAPIView):
    """
    API to retrieve all cinemas by movie name

    To search cinemas by movie one has to append the url 
    with ?movie=movie_name
    """

    serializer_class = CinemaSerializer
    
    def get_queryset(self):
        cinema_ids = list(Shows.objects.filter(
            cinema__city=self.request.query_params.get(
                'movie')).values_list(
            'cinema_id', flat=True))
        cinemas = Cinema.objects.all()
        return cinemas


class ShowTimeSeatAvailaibility(generics.ListCreateAPIView):
    """
    API to retrieve all tickets left according to show time

    To search shows by show_time one has to append the url 
    with ?show_time=query_time

    QUERY TIME SHOULD BE IN ISO FORMAT

    for example:- "2020-04-03T09:38:10.438740Z"
    """
    serializer_class = ShowTimeSeatAvailaibileSerializer

    def get_queryset(self):
        shows = Shows.objects.filter(
                    show_time=parser.parse(
                    self.request.query_params.get(
                    'show_time')).replace(tzinfo=pytz.UTC))
        return shows


class UserProfileCreateView(generics.CreateAPIView):
    """
    API for signup and creating user in db

    AFter creating user one has to login with login
    api provided by rest framework

    Either one can login through django admin
    or through restframework's url
    '/api-auth/login/'

    Make sure that user should exist before you can logged in.
    """
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = dict(self.request.data.copy())
        del data['csrfmiddlewaretoken']
        copy_data = data.copy()    
        for key, value in copy_data.items():
            if key in ['username', 'email', 'name', 'password', 'phone_no']:
                data[key] = str(data[key][0])
            elif key == 'gender':
                data[key] = int(data[key][0])
            else:
                data[key] = True if data['is_staff'][0] == 'true' else False
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.validated_data)
        return Response(serializer.validated_data, 
            status=status.HTTP_201_CREATED, headers=headers)


class BookTicketAPI(generics.CreateAPIView):
    """
    API to book a ticket by choosing from list
    of movies and cinemas
    """
    serializer_class = TicketSerializer
    authentication_classes = (
        authentication.SessionAuthentication,
    )
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['Show_Time'] = parser.parse(
            request.data['Show_Time']).replace(tzinfo=pytz.UTC)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.validated_data)
        return Response(serializer.validated_data, 
            status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        ticket = Ticket.objects.all()
        return ticket
