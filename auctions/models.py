from django.db import models
from django.contrib.auth.models import User

class Auction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('live', 'Live'),
        ('ended', 'Ended'),
        ('closed', 'Closed'),
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_increment = models.DecimalField(max_digits=10, decimal_places=2)
    go_live = models.DateTimeField()
    duration = models.PositiveIntegerField()  # in seconds
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

class CounterOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counteroffers_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counteroffers_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices_bought')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices_sold')
    pdf_file = models.FileField(upload_to='invoices/')
    created = models.DateTimeField(auto_now_add=True)
