import datetime
from dateutil import parser
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from convoapis.models import Movie
from .models import Movie, Cinema, Shows, UserProfile
from .choices import BOoK_TICKET_SERIALIZER_ERROR, CSRF_TOKEN


class ApiTestCases(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'password': 'shubh@9028', 'last_login': None, 
            'is_superuser': True, 'username': 'shubh123', 
            'email': 'dwivedishubham953@gmail.com', 'name': 'Shubham Dwivedi', 
            'phone_no': '09540359028', 'gender': 1, 'wallet': 0, 
            'added_on': datetime.datetime(2020, 4, 3, 13, 6, 43, 402926),
            'updated_on': datetime.datetime(2020, 4, 5, 9, 58, 34, 508798),
            'is_staff': True, 'is_active': True}
        self.user = UserProfile.objects.create(**self.user_data)
        self.movie_data = {
                'name': 'Tarzan', 'genre': 'Action', 'status': 1,
                'released_date': datetime.datetime(2020, 4, 1, 0, 0)}
        self.movie = Movie.objects.create(**self.movie_data)
        self.cinema_data = {
                'name': 'Pvr Dharm', 'no_of_seats': 100,
                'no_of_screens': 2, 'city': 'Gurugram',
                'opening_time': datetime.datetime.now(),
                'closing_time': datetime.datetime.now(),
                'status': 1, 'address': 'Mg road'}
        self.cinema = Cinema.objects.create(**self.cinema_data)
        self.show_data = {
                'movie': self.movie, 'cinema': self.cinema,
                'show_time': datetime.datetime(2020, 4, 3, 9, 38, 10, 438740),
                'ticket_left': 100, 'ticket_cost': 45.0, 'status': 1}
        self.show = Shows.objects.create(**self.show_data)


    def test_movie_by_city_api(self):
        """
        Test for searching movies in db by city
        query params
        """
        response = self.client.get(reverse(
            'movieapis:movie_by_city'), {'city': 'Gurugram'})
        response_data_dict = dict(dict(
            response.data).get('results')[0])
        response_data_dict['released_date'] = parser.parse(
            response_data_dict['released_date'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data_dict, self.movie_data)

    def test_cinema_by_movie_api(self):
        """
        Test for seraching alll cinemas in db by movie 
        """
        response = self.client.get(reverse(
            'movieapis:cinema_by_movie'), {'movie': 'Tarzan'})
        response_data_dict = dict(dict(
            response.data).get('results')[0])
        response_data_dict['opening_time'] = parser.parse(
            response_data_dict['opening_time'])
        response_data_dict['closing_time'] = parser.parse(
            response_data_dict['closing_time'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data_dict, self.cinema_data)

    def test_to_return_all_shows_by_showtime_api(self):
        """
        Test for seraching all shows by show_time 
        """
        response = self.client.get(
            reverse('movieapis:seat_by_showtime'), {
                    'show_time': "2020-04-03T09:38:10.438740Z"})
        response_data_dict = dict(dict(
            response.data).get('results')[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data_dict.get('ticket_left'), 
            self.show_data.get('ticket_left'))

    def test_to_book_ticket_api_fail_with_serializer_validation_error(self):
        """
        Test for seraching all shows by show_time 
        """
        self.client.login(username='shubh123', password='shubh@9028')
        session = self.client.session
        session.save()
        payload = {
            'csrfmiddlewaretoken': [CSRF_TOKEN], 
            'Movie_Name': ['Tarzan'], 'Ticket_Price': ['45.0'], 
            'User_Name': ['shubh13434'], 
            'Show_Time': ['April 3, 2020, 3 a.m.']}
        response = self.client.post(
            reverse('movieapis:book_ticket'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data, BOoK_TICKET_SERIALIZER_ERROR)
