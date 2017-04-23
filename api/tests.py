from django.test import TestCase
from django.test import Client
from datetime import datetime, timedelta
from home.models import Solution

class ApiTests(TestCase):
    def test_historic_should_return_none(self):
        response = self.client.get('/api/historic/week/')
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'xAxis': [
                    (datetime.now() - timedelta(days=6)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=5)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=4)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=3)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=2)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=1)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=0)).strftime('%d/%m')
                ],
                'series': [0, 0, 0, 0, 0, 0, 0]
            }
        )

    def test_historic_should_return_one_item_at_last_day(self):
        Solution.objects.create(date=datetime.now(), problem_id=0, profile_id=0)

        response = self.client.get('/api/historic/week/')
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'xAxis': [
                    (datetime.now() - timedelta(days=6)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=5)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=4)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=3)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=2)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=1)).strftime('%d/%m'),
                    (datetime.now() - timedelta(days=0)).strftime('%d/%m')
                ],
                'series': [0, 0, 0, 0, 0, 0, 1]
            }
        )        
