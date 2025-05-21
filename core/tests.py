# ✅ 6. TESTING (Unit + Integration)

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Company, Watchlist

class CompanyModelTest(TestCase):
    def test_company_creation(self):
        company = Company.objects.create(
            company_name="Test Co",
            symbol="TST",
            scripcode="123456"
        )
        self.assertEqual(company.symbol, "TST")

class WatchlistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.company = Company.objects.create(company_name="W Co", symbol="WC", scripcode="654321")

    def test_watchlist_creation(self):
        watchlist = Watchlist.objects.create(user=self.user, company=self.company)
        self.assertEqual(watchlist.user.username, "testuser")

class CompanyAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='pass123')
        self.company = Company.objects.create(company_name="API Co", symbol="API", scripcode="111111")

    def test_company_list_api(self):
        response = self.client.get('/api/companies/')
        self.assertEqual(response.status_code, 200)

    def test_watchlist_add_api(self):
        self.client.login(username='apiuser', password='pass123')
        response = self.client.post('/api/watchlist/', {'company_id': self.company.id})
        self.assertEqual(response.status_code, 201)

