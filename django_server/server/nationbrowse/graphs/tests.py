# coding=utf-8
"""
Unit tests for Graphs.
"""

from django.test import TestCase

# Make HTTP requests inside tests never time out.
import socket
socket.setdefaulttimeout(1000)

class GraphsTest(TestCase):
    def test_dummy(self):
        """
        TODO
        """
        self.assert_(True)
