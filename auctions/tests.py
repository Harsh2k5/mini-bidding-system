from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import Auction

class AuctionAPITestCase(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='seller', password='pass')
        self.buyer = User.objects.create_user(username='buyer', password='pass')
        self.auction = Auction.objects.create(
            seller=self.seller,
            item_name='Vintage Clock',
            description='Old but gold',
            starting_price=100.0,
            bid_increment=5.0,
            go_live=now(),
            duration=3600,
            status='live'
        )
        self.client = APIClient()
        self.client.force_login(self.buyer)

    def test_place_valid_bid(self):
        url = f'/api/auctions/{self.auction.id}/place_bid/'
        response = self.client.post(url, {'amount': 105.0}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(float(response.data['amount']), 105.0)

    def test_bid_below_minimum_fails(self):
        url = f'/api/auctions/{self.auction.id}/place_bid/'
        response = self.client.post(url, {'amount': 100.0}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Bid must be at least', str(response.data))

    def test_get_auction_list(self):
        url = '/api/auctions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)