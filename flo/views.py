from django.http import HttpResponseRedirect               
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import F
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Company
from .forms import CompanyForm

def login(request):
    return render(request, 'flo/login.html', 
    )
def index(request):
    return render(request, 'flo/index.html', {
        'companies': Company.objects.all()
    })

from django.shortcuts import render


def send_notification(company):
    # Create a notification for the company
    
    # Notification.objects.create(
    #     client=company,
    #     message=f"Fuel level is below the threshold for {company.company_name}. Current allocation: {company.fuel_allocation}L"
    # )
        
     # Send an email notification
    send_mail(
        'Fuel Level Alert',
        f"Dear {company.contact_person},\n\nYour fuel level has dropped below the threshold. Current allocation: {company.fuel_allocation}L",
        'luckybeni@gmail.com',
        [company.email],
        fail_silently=False,
    )
    print('email sent succesfully')



def owing(request):
    # Fetch all companies first
    companies = Company.objects.all()
    companies = Company.objects.filter(notification_sent=False)

    # Create an empty list to store companies that are owing
    owing_companies = []

    # Iterate over each company and calculate the remaining fuel percentage
    for company in companies:
        # Ensure init_fuel is not zero to avoid division by zero
        if company.init_fuel > 0:
            send_notification(company)
            # Calculate the remaining fuel percentage
            remaining_percentage = (company.fuel_allocation / company.init_fuel) * 100  # Remaining fuel percentage

            # Check if the remaining fuel is below 10%
            if remaining_percentage < 10:
                # Calculate amount owing based on the amount of fuel used
                fuel_used = company.init_fuel - company.fuel_allocation  # Total fuel used
                amount_owing = fuel_used * company.fuel_price  # Calculate amount owing
                owing_companies.append({
                    'company': company,
                    'amount_owing': amount_owing
                })
                
        else:
            # Optionally handle cases where init_fuel is zero
            print(f"Company {company.company_name} has an initial fuel of zero. Cannot calculate owing.")

    # Pass the owing companies to the template
    return render(request, 'flo/owing.html', {
        'owing_companies': owing_companies
    })

def view_company(request, id):
    company = Company.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

def dashboard_view(request):  
    companies = Company.objects.all()  
    return render(request, 'dashboard.html', {'companies': companies})  

def add(request):
    print("Request method:", request.method)
    
    
    if request.method == 'POST':
        print("Handling POST request")                       
        form = CompanyForm(request.POST)
        
     
        if form.is_valid():
           print('form is valid')
           new_company_name = form.cleaned_data['company_name']
           new_contact_person = form.cleaned_data['contact_person']
           new_email = form.cleaned_data['email']
           new_phone = form.cleaned_data['phone']
           new_address = form.cleaned_data['address']
           new_fuel_type = form.cleaned_data['fuel_type']
           new_amount_paid = form.cleaned_data['amount_paid']
           new_fuel_price = form.cleaned_data['fuel_price']
           new_fuel_allocation = form.cleaned_data['fuel_allocation']
           new_init_fuel = form.cleaned_data['init_fuel']


           new_company = Company(
               company_name = new_company_name,
               contact_person = new_contact_person,
               email = new_email,
               phone = new_phone,
               address = new_address,
               fuel_type = new_fuel_type,
               amount_paid = new_amount_paid,
               fuel_price = new_fuel_price,
               fuel_allocation = new_fuel_allocation,
               init_fuel = new_init_fuel
           )
           new_company.save()
           return render(request, 'flo/add.html', {
               'form': CompanyForm(),
               'success': True
               
           })           
        else:
            print("Form is not valid")
            # Form validation failed
            return render(request, 'flo/add.html', {
                'form': form,  # Return form with validation errors
                'success': False
            })   
    else:
            form = CompanyForm()          
       
    return render(request, 'flo/add.html', {
            'form': form
            })
            
def edit(request, id):
    # Fetch the company to edit or raise a 404 error if it doesn't exist
    company = get_object_or_404(Company, id=id)
    

    if request.method == 'POST':
       # company =Company.objects.filter(pk=id)
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save() 
            return redirect('index')
           
    else:
        #company = Company.objects.get(pk=id)
        form = CompanyForm(instance=company)
    return render(request, 'flo/edit.html', {
        'form': form,
        'company': company
    })
            
def delete(request, id): 
    if request.method == 'POST':
        company = Company.objects.get(pk=id)
        company.delete()
        return HttpResponseRedirect(reverse('index'))
          