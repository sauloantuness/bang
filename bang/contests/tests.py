from django.test import TestCase
from datetime import datetime, timedelta
from home.models import *

# Create your tests here.
class ContestMethodTests(TestCase):
	def test_status_contest_ended(self):
		c = Contest()
		c.date = datetime.now() - timedelta(minutes=30) 
		c.duration = 15
		self.assertEqual(c.getStatus(), 'ended')

	def test_status_contest_running(self):
		c = Contest()
		c.date = datetime.now()
		c.duration = 15
		self.assertEqual(c.getStatus(), 'running')

	def test_status_contest_waiting(self):
		c = Contest()
		c.date = datetime.now() + timedelta(minutes=30)
		c.duration = 15
		self.assertEqual(c.getStatus(), 'waiting')