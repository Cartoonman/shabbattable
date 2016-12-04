'''Unittests for the frijay app'''
from django.test import TestCase
from .models import Event
from .models import User


# Create your tests here.
class EventModelTest(TestCase):
    '''Testing the Event Model'''

    def test_string_representation(self):
        '''Test __str__ method for Event'''
        event = Event(title="My title")
        self.assertEqual(str(event), event.title)


class UserProfileModelTest(TestCase):
    '''Testing the User Model'''

    def test_string_representation(self):
        '''Test __str__ method for User'''
        userprofile = User(first_name='Abraham', last_name='Lincoln', username='mrpresident')
        self.assertEqual(str(userprofile), userprofile.username)


# class ViewsTest(TestCase):
#     '''Test the index.html page'''
#
#     def test_indexPage(self):
#         """Tests the landing page"""
#         response = self.client.get("/frijay/")
#         self.assertEqual(response.status_code, 200)
#
#     '''Test the reservation.html page'''
#
#     def test_reservationPage(self):
#         """Tests the reservations page """
#         response = self.client.get("/frijay/reservations/")
#         self.assertEqual(response.status_code, 200)
#
#     '''Test the events.html page'''
#
#     def test_eventsPage(self):
#         """Tests the events page"""
#         response = self.client.get("/frijay/events/")
#         self.assertEqual(response.status_code, 200)
#
#     '''Test the about.html page'''
#
#     def test_aboutPage(self):
#         """Tests the about page"""
#         response = self.client.get("/frijay/about/")
#         self.assertEqual(response.status_code, 200)
#
#     '''Test the login.html page'''
#
#     def test_loginPage(self):
#         """Tests the login page"""
#         response = self.client.get("/frijay/login")
#         self.assertEqual(response.status_code, 200)
#
#     '''Test the signup.html'''
#
#     def test_signUpPage(self):
#         """Tests the signup page"""
#         response = self.client.get("/frijay/signup/")
#         self.assertEqual(response.status_code, 200)
