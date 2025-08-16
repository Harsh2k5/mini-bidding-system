from rest_framework import serializers
from .models import Auction, Bid
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)
    class Meta:
        model = Bid
        fields = ['id', 'auction', 'bidder', 'amount', 'timestamp']

class AuctionSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    bids = BidSerializer(many=True, read_only=True)
    class Meta:
        model = Auction
        fields = ['id', 'item_name', 'description', 'starting_price', 'bid_increment', 'go_live', 'duration', 'status', 'seller', 'bids']