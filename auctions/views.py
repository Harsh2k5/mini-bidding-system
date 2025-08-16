from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from datetime import timedelta
from .models import Auction, Bid
from .serializers import AuctionSerializer, BidSerializer

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def place_bid(self, request, pk=None):
        auction = self.get_object()
        bid_amount = request.data.get('amount')

        if bid_amount is None:
            return Response({'error': 'Bid amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bid_amount = float(bid_amount)
        except ValueError:
            return Response({'error': 'Invalid bid amount.'}, status=status.HTTP_400_BAD_REQUEST)

        if auction.status != 'live':
            return Response({'error': 'Auction is not live.'}, status=status.HTTP_400_BAD_REQUEST)

        if not (auction.go_live <= now() <= auction.go_live + timedelta(seconds=auction.duration)):
            return Response({'error': 'Auction is not accepting bids at this time.'}, status=status.HTTP_400_BAD_REQUEST)

        highest_bid = auction.bids.order_by('-amount').first()
        if highest_bid is None:
            min_bid = auction.starting_price + auction.bid_increment
        else:
            min_bid = highest_bid.amount + auction.bid_increment

        if bid_amount < float(min_bid):
            return Response({'error': f'Bid must be at least {min_bid}'}, status=status.HTTP_400_BAD_REQUEST)

        new_bid = Bid.objects.create(auction=auction, bidder=request.user, amount=bid_amount)
        serializer = BidSerializer(new_bid)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BidViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]