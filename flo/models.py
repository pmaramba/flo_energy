from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Company(models.Model):    
    FUEL_TYPE_CHOICES = [
        ('unleaded_petrol', 'Unleaded Petrol'),
        ('blended_petrol', 'Blended Petrol'),
        ('diesel_50', 'Diesel 50'),
        ('regular_diesel', 'Regular Diesel'),
        ]
    
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.TextField()
    fuel_type = models.CharField(max_length=100, choices=FUEL_TYPE_CHOICES)    
    fuel_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fuel_allocation = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    init_fuel = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    notification_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=0.1)
    notification_sent = models.BooleanField(default=False)
    
def calculate_fuel_allocation(self):  
    if self.fuel_price > 0:  
        self.fuel_allocation = self.amount_paid / self.fuel_price  
        self.save()  
    else:  
        raise ValueError("Fuel price must be greater than zero.")  


def deduct_fuel(self, amount):
    if amount > self.fuel_allocation:
        raise ValueError("Not enough fuel allocation")

    # Deduct the fuel
    self.fuel_allocation -= amount
    self.save()
    # Check if the fuel allocation is below the notification threshold
    if self.fuel_allocation <= (self.notification_threshold * self.amount_paid):
        self.send_notification()
            
def send_notification(self):
    # Create a notification for the company
    Notification.objects.create(
        client=self,
        message=f"Fuel level is below the threshold for {self.company_name}. Current allocation: {self.fuel_allocation}L"
    )
        
     # Send an email notification
    send_mail(
        'Fuel Level Alert',
        f"Dear {self.contact_person},\n\nYour fuel level has dropped below the threshold. Current allocation: {self.fuel_allocation}L",
        'luckybeni@gmail.com',
        [self.email],
        fail_silently=False,
    )
    print('email sent succesfully')

def __str__(self):
    return self.company_name

class FuelTransaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount_withdrawn = models.DecimalField(max_digits=10, decimal_places=0)
    transaction_date = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f'{self.amount_withdrawn} withdrawn by {self.company.company_name} on {self.transaction_date}'

    
class Notification(models.Model):
    client = models.ForeignKey(Company, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
def __str__(self):
    return f'Notification for  {self.client.company_name}: {self.message}'
    

@receiver(post_save, sender=FuelTransaction)
def update_fuel_allocation(sender, instance, created, **kwargs):
    if created:
        # Deduct fuel when a new transaction is created
        company = instance.company
        try:
            company.deduct_fuel(instance.amount_withdrawn)
        except ValueError as e:
            # Handle the error (e.g., log it, notify someone, etc.) 
            print(f"Error deducting fuel: {e} ") 
            
def save(self, *args, **kwargs):  
    # Calculate fuel allocation before saving  
    self.calculate_fuel_allocation()  
    super().save(*args, **kwargs)  
