# coding=utf-8
"""
Unit tests for Places.
"""

from django.test import TestCase
from django.conf import settings

# Make HTTP requests inside tests never time out.
import socket
socket.setdefaulttimeout(1000)

class PlacesTest(TestCase):
    def test_dummy(self):
        """
        TODO
        """
        self.assert_(True)
