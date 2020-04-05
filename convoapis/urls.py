from django.urls import include, path
from rest_framework import routers
from .views import *

app_name="convoapis"


urlpatterns = [
    
    path('user/list/', UserListAPI.as_view(), name="user_list"),
    path('cinema/list/', CinemaAPI.as_view(), name='cinema_api'), 
    path('shows/list/', ShowCreateListAPI.as_view(), name='show_create_list_api'),
    path('all/tickets/', TicketListAPI.as_view(), name='ticket_list_api'),
    # BELOW API URLS ARE ASSIGNMENT BASED APIS

    path('movie/city/', MoviesByCity.as_view(), name="movie_by_city"),
    path('cinema/movie/', CinemasByMovie.as_view(), name="cinema_by_movie"),
    path('seats/by/show_time/', ShowTimeSeatAvailaibility.as_view(), name="seat_by_showtime"),
    path('user/signup/', UserProfileCreateView.as_view(), name='signup_api'),
    path('book/ticket/', BookTicketAPI.as_view(), name="book_ticket")
   

]