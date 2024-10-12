from django.contrib import admin
from .models import Company, FuelTransaction, Notification

# Register your models here.
admin.site.register(Company)
admin.site.register(FuelTransaction)
admin.site.register(Notification)