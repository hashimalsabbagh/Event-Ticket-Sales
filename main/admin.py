from django.contrib import admin
from .models import *

admin.site.register(Events)
admin.site.register(TicketsPurchased)
admin.site.register(Wallet)
admin.site.register(CancellationRequest)
# Register your models here.
