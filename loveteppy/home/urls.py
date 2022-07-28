from django.urls import path
from . import views

urlpatterns = [
	
]


################### NOTE
'''
This is not functional for I imported the views on src/urls.py directly. 
There's this error not displaying the homepage when I put "include('home.urls')" on the urlpatterns so,
I did a workaround.
'''
