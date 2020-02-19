from django.urls import path  # allows to create paths within our app

from . import views

app_name = 'user'  # part of the url reverse loopkup functionality

urlpatterns = [
    # the path will be user/create and will be wired to the CreateUserView
    # The app_name and the below name='create' helps with the url reverse
    # lookup done in the test functions.
    # Finally we want to include this url on the app main urls in app/urls.py
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
 ]
