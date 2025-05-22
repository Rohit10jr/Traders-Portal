from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Company, WatchList
from django.test import override_settings



# --------------- Company crud tests --------------------
@override_settings(REST_FRAMEWORK={'DEFAULT_PAGINATION_CLASS': None})
class CompanyViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='test@pass1234')
        self.login_url = reverse('token_obtain_pair') 
        self.company_list_url = reverse('company-list-create')
        self.register_url = reverse('register')
        
        # delete models 
        Company.objects.all().delete()
        # User.objects.all().delete()
        
        # Authenticate
        response = self.client.post(self.login_url, {"username": "testuser", "password": "test@pass1234"})
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        
        # Create test data
        self.company1 = Company.objects.create(company_name="Infosys", symbol="INFY", scripcode="500209")
        self.company2 = Company.objects.create(company_name="Tata Consultancy", symbol="TCS", scripcode="532540")

    # Test User Registration
    def test_user_registration_success(self):
        payload = {
            "username": "newuser",
            "password": "newpass@1234"
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("data", response.data)

    def test_user_registration_invalid(self):
        response = self.client.post(self.register_url, {})  # Empty data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)


    # Test Create / Retrieve / Update / Delete Company
    def test_create_company(self):
        payload = {
            "company_name": "Wipro",
            "symbol": "WIPRO",
            "scripcode": "507685"
        }
        response = self.client.post(self.company_list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 3)

    def test_get_single_company(self):
        url = reverse('company-detail', kwargs={'pk': self.company1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], "INFY")

    def test_update_company(self):
        url = reverse('company-detail', kwargs={'pk': self.company1.pk})
        payload = {"company_name": "Infosys Ltd", "symbol": "INFY", "scripcode": "500209"}
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company1.refresh_from_db()
        self.assertEqual(self.company1.company_name, "Infosys Ltd")

    def test_delete_company(self):
        url = reverse('company-detail', kwargs={'pk': self.company1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(pk=self.company1.pk).exists())



# --------------- WatchList crud tests --------------------
@override_settings(REST_FRAMEWORK={'DEFAULT_PAGINATION_CLASS': None})
class WatchlistCRUDTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        Company.objects.all().delete()
        WatchList.objects.all().delete()

        self.company1 = Company.objects.create(company_name="Apple", symbol="AAPL", scripcode="123")
        self.company2 = Company.objects.create(company_name="Amazon", symbol="AMZN", scripcode="456")

        self.watchlist_item = WatchList.objects.create(user=self.user, company=self.company1)

    def test_create_watchlist_item(self):
        url = reverse('watchlist-list-create')
        data = {'company_id': self.company2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['company']['id'], self.company2.id)
        
    def test_prevent_duplicate_watchlist(self):
        url = reverse('watchlist-list-create')
        data = {'company_id': self.company1.id}  # Already added in setUp
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_watchlist_items(self):
        url = reverse('watchlist-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_watchlist_item(self):
        url = reverse('watchlist-detail', args=[self.watchlist_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company']['id'], self.company1.id)
        
    def test_delete_watchlist_item(self):
        url = reverse('watchlist-detail', args=[self.watchlist_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WatchList.objects.count(), 0)
