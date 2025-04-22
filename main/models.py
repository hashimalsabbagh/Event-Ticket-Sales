from django.db import models
from django.contrib.auth.models import User


class Events(models.Model): 
    event_host = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    event_name = models.CharField(max_length=100)
    event_description = models.CharField(max_length=1000)
    max_tickets_no = models.IntegerField(default=500)
    tickets_no = models.IntegerField(blank=True, null=True)
    release_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    price = models.FloatField()

    def save(self, *args, **kwargs):
        if self.tickets_no is None: 
            self.tickets_no = self.max_tickets_no   # starting number of tickets = max tickets
        super().save(*args, **kwargs)

    def __str__(self): 
        return self.event_name

class TicketsPurchased(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"{self.user.username} bought {self.quantity} ticket(s) for {self.event.event_name}"

    
class Wallet(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.FloatField(default=0.00)

    def __str__(self): 
        return f"{self.user.username} has ${self.money}"
    

class CancellationRequest(models.Model):
    reservation = models.ForeignKey(TicketsPurchased, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event_name = models.CharField(max_length=100, blank=True, default="")
    event_description = models.CharField(max_length=1000, blank=True, default="")
    quantity = models.PositiveIntegerField(default=1)
    requested_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(null=True)

    def __str__(self):
        return f"Cancellation request for {self.user} for event {self.event_name} - {'Pending' if self.accepted is None else 'Approved' if self.accepted else 'Rejected'}"
    

class Transactions(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        timestamp = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if self.amount >= 0: 
         return f"Transaction: {self.wallet.user} added {self.amount} at {timestamp}"
        else:
         return f"Transaction: {self.wallet.user} deducted {self.amount} at {timestamp}"
        
class UserProfile(models.Model): 
    USER_TYPES = [
        ('host', 'Event Hoster'),
        ('normal', 'Normal User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=USER_TYPES, default='normal')

    def __str__(self):
        return f"{self.user.username} is account type: {self.type}"
# Create your models here.
