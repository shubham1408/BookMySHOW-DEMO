MALE = 1
FEMALE = 2
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female')
)


INACTIVE = 0
ACTIVE = 1
STATUS_CHOICES = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'Inactive')
)

from rest_framework.exceptions import ErrorDetail
BOoK_TICKET_SERIALIZER_ERROR = {
	'Movie_Name': [ErrorDetail(string='"Tarzan" is not a valid choice.',
		code='invalid_choice')],
	'Ticket_Price': [ErrorDetail(string='"45.0" is not a valid choice.',
		code='invalid_choice')], 
	'User_Name': [ErrorDetail(string='"shubh13434" is not a valid choice.', 
		code='invalid_choice')],
	'Show_Time': [ErrorDetail(string='"2020-04-03 03:00:00+00:00" is not a valid choice.',
		code='invalid_choice')]
}

CSRF_TOKEN = 'Uze4e00xm3hgCLzHZXGeUjDWTcU2R3WMBXva7NUfjCBFL0UcNPUSx9RAGxAAg3Hc'