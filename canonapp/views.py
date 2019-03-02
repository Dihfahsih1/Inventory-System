from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *
from datetime import datetime as dt
from datetime import datetime,timezone
from .resources import *
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.db.models import Count, F, Value,Sum
from django.db.models.functions import Length, Upper, datetime

from django.http import HttpResponse

from django.views.generic import View
from django.utils import timezone
from .pdf_render import Render

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import *
from django.shortcuts import redirect, HttpResponseRedirect

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


# Create your views here.

#########################
# operations manager viewing cars
###########################

def operations_view_cars(request):
    items = Car.objects.all()
    context = {'items': items, }
    return render(request, "operationsapp/operations_view_cars.html", context)

#################################
# receptionist viewing cars
#################################

def receptionist_view_cars(request):
    items = Car.objects.all()
    context = {'items': items, }
    return render(request, "receptionistapp/receptionist_view_cars.html", context)

################################
# operations manager adding car
#############################

def operations_add_car(request):
    if request.method=="POST":
        form=CarForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('operations_view_cars')
    else:
        form=CarForm()
        return render(request, 'operationsapp/operations_add_car.html', {'form':form})

##########################
#  Receptionist_home page
#########################
def receptionist_home(request):


    return render(request,"receptionistapp/receptionist_home.html")




def operations_delete_car(request,pk):
    Car.objects.filter(id=pk).delete()
    items=Car.objects.all()
    context={'items':items}
    return render(request, 'operationsapp/operations_view_cars.html', context)

def receptionist_add_complaint(request):
    if request.method=="POST":
        form=ComplaintsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receptionist_view_complaints')
    else:
        form=ComplaintsForm()
        return render(request, 'receptionistapp/receptionist_add_complaint.html', {'form':form})

def operations_add_driver(request):
    if request.method=="POST":
        form=DriverForm(request.POST,request.FILES)
        if form.is_valid():

            car = get_object_or_404(Car, car_registration_no=form.cleaned_data['attached_car'].car_registration_no)

            if car.availability=='TAKEN':
                info='The selected car has already been assigned to a driver'
                form = DriverForm()
                return render(request,'operationsapp/operations_add_driver.html',{'info':info,'form':form})

            else:

                # updating the car status
                Car.objects.filter(car_name=form.cleaned_data['attached_car'].car_name) \
                    .update(availability='TAKEN')

                form.save()

                info='The driver successfully registered'
                items = Driver.objects.all()

                return render(request,'operationsapp/operations_view_drivers.html',{'info':info,'items': items})
    else:
        form=DriverForm()
        return render(request, 'operationsapp/operations_add_driver.html', {'form':form})

def receptionist_view_complaints(request):
    items = Complaints.objects.all()
    context = {'items': items, }
    return render(request, "receptionistapp/receptionist_view_complaints.html", context)

def receptionist_view_drivers(request):
    items = Driver.objects.all()
    context = {'items': items, }
    return render(request, "receptionistapp/receptionist_view_drivers.html", context)

def operations_view_drivers(request):
    items = Driver.objects.all()
    context = {'items': items, }
    return render(request, "operationsapp/operations_view_drivers.html", context)

def operations_edit_car(request,pk):
    item=get_object_or_404(Car,pk=pk)

    if request.method=="POST":
        form=CarForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            car = form.cleaned_data['attached_car']
            Car.objects.filter(car_registration_no=car).update(car_status='TAKEN')
            form.save()
            return redirect('operations_view_cars')


    else:
        form=CarForm(instance=item)
    return render(request, 'operationsapp/operations_edit_item.html', {'form':form, 'header': 'Car'})

def receptionist_edit_complaint(request,pk):
    item=get_object_or_404(Complaints,pk=pk)
    if request.method=="POST":
        form=ComplaintsForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('receptionist_view_complaints')
    else:
        form=ComplaintsForm(instance=item)
    return render(request, 'receptionistapp/receptionist_edit_item.html', {'form':form, 'header': 'Complaint'})

def operations_edit_driver(request,pk):
    item=get_object_or_404(Driver,pk=pk)

    if request.method=="POST":
        form=DriverForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect('operations_view_drivers')

    else:
        form=DriverForm(instance=item)
    return render(request, 'operationsapp/operations_edit_item.html', {'form':form, 'header': 'Driver'})

def operations_delete_car(request,pk):
    Car.objects.filter(id=pk).delete()
    items=Car.objects.all()
    context={'items':items}
    return render(request, 'operationsapp/operations_view_cars.html', context)

def receptionist_delete_complaint(request,pk):
    Complaints.objects.filter(id=pk).delete()
    items=Complaints.objects.all()
    context={'items':items}
    return render(request, 'receptionistapp/receptionist_view_complaints.html', context)

def operations_delete_driver(request,pk):
    driver=Driver.objects.filter(id=pk)
    #search for all driver associated data
    DriverPayment.objects.filter(driver_name=driver.id).delete()
    Driver_Payment_Report.objects.filter(driver_name=driver.driver_name).delete()
    DriverPayments_Archive.objects.filter(driver_name=driver.id).delete()
    Driver_payment_Reports_Archive.objects.filter(driver_name=driver.driver_name).delete()
    driver.delete()
    items=Driver.objects.all()
    context={'items':items}
    return render(request, 'operationsapp/operations_view_drivers.html', context)

def receptionist_forward_complaint(request,pk):
    complaint=Complaints.objects.filter(id=pk)
    complaint.update(forwarded_status='FORWARDED')
    items=Complaints.objects.all()
    context={'items':items}
    return render(request, 'receptionistapp/receptionist_view_complaints.html', context)

def operations_home(request):
    return render(request, 'operationsapp/operations_home.html')

def operations_view_complaints(request):
    items = Complaints.objects.filter(forwarded_status='FORWARDED')
    context = {'items': items, }
    return render(request, "operationsapp/operations_view_complaints.html", context)

def operations_export_cars(request):
    car_resource = CarResource()
    dataset = car_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cars.csv"'
    return response

def operations_export_drivers(request):
    driver_resource = DriverResource()
    dataset = driver_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="drivers.csv"'
    return response

def operations_view_driver_payments(request):

    all_drivers = Driver.objects.all()
    # loop through all drivers available
    for driver in all_drivers:

        driver_name = driver.driver_name
        driver_id = driver.id
        driver_car = driver.attached_car
        driver_balance = driver.driver_monthly_payment

        # calculating total paid so far
        total = DriverPayment.objects.filter(driver_name=driver_id).aggregate(
            total_amount_paid=models.Sum("paid_amount"))
        total_paid = total["total_amount_paid"]
        report_item = Driver_Payment_Report()
        report_item.driver_name = driver_name
        report_item.amount_paid = total_paid
        report_item.balance = driver_balance
        report_item.driver_car = driver_car

        # first check for availability of an object(filtering)
        if Driver_Payment_Report.objects.filter(driver_name=driver_name):
            Driver_Payment_Report.objects.filter(driver_name=driver_name).update(amount_paid=total_paid,
                                                                                 balance=driver_balance)

        else:
            report_item.save()

    items = Driver_Payment_Report.objects.all()
    item_number = items.count()

    # calculating the total balance
    total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
    driver_total_balance = total_bal["total_bal"]

    # calculating the total payments
    total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
    driver_total_paid = total_pai["total_pai"]


    # when sending SMS to a driver
    if request.method == 'POST':
        message = request.POST['sms_message']
        driv_name=request.POST['driver_name']
        contact=get_object_or_404(Driver,driver_name=driv_name).driver_contact

        # Your Account Sid and Auth Token from twilio.com/console
        account_sid = 'ACe9595ff028274b8621fb538ae4b10c8b'
        auth_token = 'a331bb0cbf2ef5bf8a650aabc48d8c82'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body="Dear" + driv_name +"    "+
                 message,
            from_='+12013406675',
            to='+256' + contact
        )


        redirect('operations_view_driver_payments')


    context = {
        'driver_total_balance': driver_total_balance,
        'driver_total_paid': driver_total_paid,
        'items': items,
        'item_number': item_number
    }
    return render(request, "operationsapp/operations_view_driver_payments.html", context)






def accountant_home(request):
    return render(request, 'accountantapp/accountant_home.html')

def accountant_view_driver_payments(request):
    items = Driver.objects.all()
    context = {'items': items, }
    return render(request, 'accountantapp/accountant_view_driver_payments.html', context)

###########################################
# this handles driver payments
#######################################

def accountant_make_driver_payments(request):
    if request.method=="POST":
        form=DriverPaymentForm(request.POST)
        if form.is_valid():
            #updating the driver balance
            Driver.objects.filter(driver_name=form.cleaned_data['driver_name'].driver_name)\
               .update(driver_monthly_payment=F('driver_monthly_payment')-form.cleaned_data['paid_amount'])

            #saving payment data
            form.save()
            return redirect('accountant_make_driver_payments')
    else:
        #the payment form
        form=DriverPaymentForm()

        # looking for all available payments
        items = DriverPayment.objects.all()
        context = {'items': items,'form':form, }

    return render(request, 'accountantapp/accountant_make_driver_payments.html',context)




#class handling pdf generation of the driver receipt
class generate_driver_payment_receipt(View):

    def get(self, request,pk):
        payment_item = get_object_or_404(DriverPayment, pk=pk)
        today = timezone.now()
        params = {
            'payment_item':payment_item,
            'today': today,
            'request': request
        }
        return Render.render('accountantapp/driver_receipt.html', params)

# class handling pdf generation of the driver receipt
class accountant_generate_driver_financial_report(View):
    def get(self, request, driver_name):
        #first get the driver name
       # driver =Driver.objects.filter(pk=pk).values_list('')

        #driver id to match drivers in payment table
        driver = get_object_or_404(Driver, driver_name=driver_name).id


        #driver name to appear on the report
        driver_name = driver_name


        #passing on the driver attached car
        attached_car=get_object_or_404(Driver, driver_name=driver_name).attached_car

        #Total balance to be paid by driver
        driver_balance=get_object_or_404(Driver, driver_name=driver_name).driver_monthly_payment

        #all payments made by a specific driver
        payments=DriverPayment.objects.filter(driver_name=driver)

        #getting today's date
        today = timezone.now()


        #calculating total paid so far
        total= DriverPayment.objects.filter(driver_name=driver).aggregate(total_amount_paid=models.Sum("paid_amount"))
        total_paid=total["total_amount_paid"]


        #parameters sent to the pdf for display
        params = {
            'attached_car':attached_car,
            'total_paid':total_paid,
            'driver_balance':driver_balance,
            'driver_name':driver_name,
            'request': request,
            'payments': payments,
            'today': today,
        }
        return Render.render('accountantapp/accountant_driver_financial_report.html', params)




###############################################
#  THis enables printing of the archived reports
#
###################################################



class accountant_driver_payment_archive_print(View):
        def get(self, request):
            if request.method=='POST':
                report_year = request.POST['report_year'] 
                report_month=request.POST['report_month']
                
                #all the reports got after printing
                archived_reports=Driver_payment_Reports_Archive.objects.filter(month=report_month, year=report_year)
                
                #getting the current time zone
                today = timezone.now()
 
                #number of records got
                item_number = archived_reports.count()
        
                # calculating the total balance
                total_bal = Driver_payment_Reports_Archive.objects.aggregate(total_bal=models.Sum("balance"))
                driver_total_balance = total_bal["total_bal"]
        
                # calculating the total payments
                total_pai = Driver_payment_Reports_Archive.objects.aggregate(total_pai=models.Sum("amount_paid"))
                driver_total_paid = total_pai["total_pai"]
                


        #parameters sent to the pdf for display
        params = {
            'item_number':item_number, 
            'request': request,
            'archived_reports': archived_reports,
            'driver_total_paid':driver_total_paid
            'driver_total_balance':driver_total_balance
            'today': today,
        }
        return Render.render('accountantapp/accountant_driver_payment_archive_print.html', params)



















#########################################
# display_driver_financial statement
##########################################

# class handling pdf generation of the driver receipt

def accountant_display_driver_financial_statement(request, driver_name):
#first get the driver name
# driver =Driver.objects.filter(pk=pk).values_list('')

#driver id to match drivers in payment table
    driver = get_object_or_404(Driver, driver_name=driver_name).id


    #driver name to appear on the report
    driver_name = driver_name


    #passing on the driver attached car
    attached_car=get_object_or_404(Driver, driver_name=driver_name).attached_car

    #Total balance to be paid by driver
    driver_balance=get_object_or_404(Driver, driver_name=driver_name).driver_monthly_payment

    #all payments made by a specific driver
    payments=DriverPayment.objects.filter(driver_name=driver)

    #getting today's date
    today = timezone.now()


    #calculating total paid so far
    total= DriverPayment.objects.filter(driver_name=driver).aggregate(total_amount_paid=models.Sum("paid_amount"))
    total_paid=total["total_amount_paid"]


    #parameters sent to the pdf for display
    params = {
        'attached_car':attached_car,
        'total_paid':total_paid,
        'driver_balance':driver_balance,
        'driver_name':driver_name,
        'request': request,
        'payments': payments,
        'today': today,
    }
    return render(request,'accountantapp/accountant_display_driver_financial_statement.html', params)




def operations_display_driver_financial_statement(request, driver_name):
#first get the driver name
# driver =Driver.objects.filter(pk=pk).values_list('')

#driver id to match drivers in payment table
    driver = get_object_or_404(Driver, driver_name=driver_name).id


    #driver name to appear on the report
    driver_name = driver_name


    #passing on the driver attached car
    attached_car=get_object_or_404(Driver, driver_name=driver_name).attached_car

    #Total balance to be paid by driver
    driver_balance=get_object_or_404(Driver, driver_name=driver_name).driver_monthly_payment

    #all payments made by a specific driver
    payments=DriverPayment.objects.filter(driver_name=driver)

    #getting today's date
    today = timezone.now()


    #calculating total paid so far
    total= DriverPayment.objects.filter(driver_name=driver).aggregate(total_amount_paid=models.Sum("paid_amount"))
    total_paid=total["total_amount_paid"]


    #parameters sent to the pdf for display
    params = {
        'attached_car':attached_car,
        'total_paid':total_paid,
        'driver_balance':driver_balance,
        'driver_name':driver_name,
        'request': request,
        'payments': payments,
        'today': today,
    }
    return render(request,'operationsapp/operations_display_driver_financial_statement.html', params)




 ##################################
 # This produces the general financial report for all drivers
 ##################################       


def driver_general_financial_report(request):
    
    #when some one submits the financial report
    if request.method == 'POST':
        archived_year = request.POST['archived_year']
        archived_month=request.POST['archived_month']
            
            #getting all the driver_payments
        all_payment_reports=Driver_Payment_Report.objects.all()
        for payment_report in all_payment_reports:
            driver_name=payment_report.driver_name
            driver_car=payment_report.driver_car
            balance=payment_report.balance
            amount_paid=payment_report.amount_paid
            date=payment_report.date
    
            #getting the archives object to creation
            payment_report_archive_object=Driver_payment_Reports_Archive()
    
            payment_report_archive_object.driver_name=driver_name
            payment_report_archive_object.amount_paid=amount_paid
            payment_report_archive_object.driver_car=driver_car
            payment_report_archive_object.balance=balance
            payment_report_archive_object.date=date
            payment_report_archive_object.month=archived_month
            payment_report_archive_object.year=archived_year


            #getting the specific driver object and updating its current balance
            Driver.objects.filter(driver_name=driver_name).update(
                driver_monthly_payment=F('driver_monthly_payment_ref')+balance
            )
    
            payment_report_archive_object.save()
    
        #This deletes all the current report data after creation of a monthly archive.
        all_payment_reports.delete()
    
        driver_receipts=DriverPayment.objects.all()
        for receipt in driver_receipts:
            date=receipt.date
            driver_name=receipt.driver_name
            paid_amount=receipt.paid_amount
            paid_by=receipt.paid_by
            received_by=receipt.received_by
    
            #get the receipt archive object
            payment_receipt_archive=DriverPayments_Archive()
            payment_receipt_archive.date=date
            payment_receipt_archive.driver_name=driver_name
            payment_receipt_archive.paid_amount=paid_amount
            payment_receipt_archive.paid_by=paid_by
            payment_receipt_archive.received_by=received_by
            payment_receipt_archive.month=archived_month
            payment_receipt_archive.year=archived_year
            
            payment_receipt_archive.save()
    
        driver_receipts.delete()
        message="you have successfully archived the payment report and all payment receipts for"+archived_month+" "+archived_year
        context={'message':message}
    
        return  render(request, "accountantapp/driver_general_financial_report.html",context)
    
    
    all_drivers = Driver.objects.all()
    #loop through all drivers available
    for driver in all_drivers:

        driver_name=driver.driver_name
        driver_id=driver.id
        driver_car=driver.attached_car
        driver_balance=driver.driver_monthly_payment

        # calculating total paid so far
        total = DriverPayment.objects.filter(driver_name=driver_id).aggregate(total_amount_paid=models.Sum("paid_amount"))
        total_paid = total["total_amount_paid"]
        report_item=Driver_Payment_Report()
        report_item.driver_name=driver_name
        report_item.amount_paid=total_paid
        report_item.balance=driver_balance
        report_item.driver_car=driver_car

        # first check for availability of an object(filtering)
        if Driver_Payment_Report.objects.filter(driver_name=driver_name):
            Driver_Payment_Report.objects.filter(driver_name=driver_name).update(amount_paid=total_paid,balance=driver_balance)

        else:
         report_item.save()

    items=Driver_Payment_Report.objects.all()
    item_number=items.count()

    #calculating the total balance
    total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
    driver_total_balance = total_bal["total_bal"]

    #calculating the total payments
    total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
    driver_total_paid = total_pai["total_pai"]
    
    months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
    years = [2019,2020,2021,2022,2023,2024]


    context={
        'months':months,
        'years':years,
        'driver_total_balance':driver_total_balance,
        'driver_total_paid':driver_total_paid,
        'items':items,
        'item_number':item_number
    }

    return render(request, "accountantapp/driver_general_financial_report.html",context)

##########################################################
# printing of the general financial report
####################################################


class print_general_financial_report(View):

    def get(self, request):
        today = timezone.now()

        items = Driver_Payment_Report.objects.all()
        item_number = items.count()

        # calculating the total balance
        total_bal = Driver_Payment_Report.objects.aggregate(total_bal=models.Sum("balance"))
        driver_total_balance = total_bal["total_bal"]

        # calculating the total payments
        total_pai = Driver_Payment_Report.objects.aggregate(total_pai=models.Sum("amount_paid"))
        driver_total_paid = total_pai["total_pai"]

        params = {
        'driver_total_balance':driver_total_balance,
        'driver_total_paid':driver_total_paid,
        'items':items,
        'item_number':item_number,
        'today': today,
        }
        return Render.render('accountantapp/print_general_financial_report.html', params)
        
        
        
        

def operations_handle_complaint(request,pk):

    complaint=get_object_or_404(Complaints,pk=pk)
    Complaints.objects.filter(pk=pk).update(forwarded_status='CLEARED')
    Complaints.objects.filter(pk=pk).update(handled_status='HANDLED')


    items = Complaints.objects.filter(forwarded_status='FORWARDED')
    context = {'items': items, }
    return render(request, "operationsapp/operations_view_complaints.html", context)

def operations_view_car_details(request,pk):
    #driver
    driver=get_object_or_404(Driver,pk=pk)

    #attached car
    specific_car=driver.attached_car

    context={'specific_car':specific_car,}

    return render(request, "operationsapp/operations_view_car_details.html",context)
    
def receptionist_view_car_details(request,pk):
    #driver
    driver=get_object_or_404(Driver,pk=pk)

    #attached car
    specific_car=driver.attached_car

    context={'specific_car':specific_car,}

    return render(request, "receptionistapp/receptionist_view_car_details.html",context)    
    
    
    
    
    
    
    
    
    
    
    
    

#generating the financial statement for a particular driver.
class generate_operations_driver_financial_statement(View):
    def get(self, request, driver_name):
        #first get the driver name
       # driver =Driver.objects.filter(pk=pk).values_list('')

        #driver id to match drivers in payment table
        driver = get_object_or_404(Driver, driver_name=driver_name).id


        #driver name to appear on the report
        driver_name = driver_name


        #passing on the driver attached car
        attached_car=get_object_or_404(Driver, driver_name=driver_name).attached_car

        #Total balance to be paid by driver
        driver_balance=get_object_or_404(Driver, driver_name=driver_name).driver_monthly_payment

        #all payments made by a specific driver
        payments=DriverPayment.objects.filter(driver_name=driver)

        #getting today's date
        today = timezone.now()


        #calculating total paid so far
        total= DriverPayment.objects.filter(driver_name=driver).aggregate(total_amount_paid=models.Sum("paid_amount"))
        total_paid=total["total_amount_paid"]


        #parameters sent to the pdf for display
        params = {
            'attached_car':attached_car,
            'total_paid':total_paid,
            'driver_balance':driver_balance,
            'driver_name':driver_name,
            'request': request,
            'payments': payments,
            'today': today,}

        return Render.render('operationsapp/operations_driver_financial_statement.html', params)




##################################
# viewing of monthly archives
#################################

def view_archives(request):


    return render(request, 'operationsapp/view_archives.html')




def accountant_edit_driver_receipts(request,pk):

    item=get_object_or_404(DriverPayment,pk=pk)
    if request.method=="POST":
        form=DriverPaymentForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('accountant_make_driver_payments')
    else:
        form=DriverPaymentForm(instance=item)
        context={
        'form':form
        }

    return render(request,'accountantapp/accountant_edit_item.html',context)


def operations_view_driver_details(request,pk):
    
    specific_driver=get_object_or_404(Driver,pk=pk)
    
    context={
        'specific_driver':specific_driver
    }
    
    
    return render(request,'operationsapp/operations_view_driver_details.html',context)


def receptionist_view_driver_details(request,pk):
    
    specific_driver=get_object_or_404(Driver,pk=pk)
    
    context={
        'specific_driver':specific_driver
    }
    
    
    return render(request,'receptionistapp/receptionist_view_driver_details.html',context)
  
    
######################################
# Searching for archived report
#############################################
    
    

def accountant_driver_payment_archive(request):
    # when we search for monthly archived reports
    if request.method == 'POST':
        report_year = request.POST['report_year'] 
        report_month=request.POST['report_month']
        archived_reports=Driver_payment_Reports_Archive.objects.filter(month=report_month, year=report_year)
        months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
        years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
        drivers=Driver.objects.all()
    
        context={'archived_reports':archived_reports,'months':months,'years':years,'drivers':drivers}
        return render(request,"accountantapp/accountant_driver_payment_archive.html",context)

    months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
    years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
    drivers=Driver.objects.all()
    context={'months':months,'years':years,'drivers':drivers}
    return render(request,"accountantapp/accountant_driver_payment_archive.html",context)


##########################################
# Searching for the payment receipts
####################################################

def accountant_driver_payment_archived_receipt(request):
           # when we search for monthly archived receipts for customers
    if request.method == 'POST':
        receipt_year = request.POST['receipt_year'] 
        receipt_month=request.POST['receipt_month']
        receipt_driver=request.POST['receipt_driver']
        
        driver_id=get_object_or_404(Driver, driver_name=receipt_driver).id
    
        archived_receipts=DriverPayments_Archive.objects.filter(month=receipt_month, year=receipt_year,driver_name=driver_id)
        months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November',
                'December']
        years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
        drivers=Driver.objects.all()
        context={'archived_receipts':archived_receipts,'months':months,'years':years,'drivers':drivers}
        return render(request,"accountantapp/accountant_driver_payment_archived_receipt.html",context)
            
    months=   ['January','February','March', 'April', 'May', 'June', 'July','August', 'August','September','October','November', 'November', 'December']
    years = [2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035]
    drivers=Driver.objects.all()
    context={'months':months,'years':years,'drivers':drivers}
    return render(request,"accountantapp/accountant_driver_payment_archived_receipt.html",context)









################################

 #   ACCOUNTANT DEFS  #
#############################

def accountantindex(request):
    return render(request,'accountantapp/Accprofile.html')

def accountant_profile(request):
    return render(request, 'accountantapp/Accprofile.html')

    ####################################################
    #        ENTERING RECORDS INTO THE DATABASE        #
    ####################################################

 # payment of salaries
def pay_salary(request):
    if request.method=="POST":
        form=SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salaryreport')
    else:
        form=SalaryForm()
        return render(request, 'accountantapp/add_new.html',{'form':form})


# recording the major expenditures
def enter_expenditure(request):
    if request.method=="POST":
        form=SpendForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('expenditurereport')
    else:
        form=SpendForm()
        return render(request, 'accountantapp/add_new.html',{'form':form})



  #recording small expenses
def enter_sundryexpense(request):
    if request.method=="POST":
        form=SundryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('sundryreport')
    else:
        form=SundryForm()
        return render(request, 'accountantapp/add_new.html',{'form':form})

#############################################################        
# EDITTING THE FIELDS THE ENTRIES THAT HAVE BEEN RECORDED   #
#############################################################
def edit_payment(request, pk):
    item = get_object_or_404(Spend, pk=pk)
    if request.method == "POST":
        form = SpendForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('expenditurereport')
    else:
        form = SpendForm(instance=item)
    return render(request, 'accountantapp/add_new.html', {'form': form, })

def edit_salary(request, pk):
    item = get_object_or_404(Salary, pk=pk)
    if request.method == "POST":
        form = SalaryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('salaryreport')
    else:
        form = SalaryForm(instance=item)
    return render(request, 'accountantapp/add_new.html', {'form': form, })

def edit_sundry(request, pk):
    item = get_object_or_404(Sundry, pk=pk)
    if request.method == "POST":
        form = SundryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('sundryreport')
    else:
        form = SundryForm(instance=item)
    return render(request, 'accountantapp/add_new.html', {'form': form, })

        ####################################################
        #                VIEWING  THE REPORTS              #
        ####################################################

def display_viewstaff(request):
    all_staff = StaffDetails.objects.all()
    return render(request,'accountantapp/accountantindex.html',{'Staffs': all_staff})

       ####################################################
      #        CALCULATING TOTALS IN THE REPORTS         #
      ####################################################

def salaryreport(request):
  timezone.now()
  current_month = datetime.datetime.now().month
  queryset = Salary.objects.all().filter(Date__month=current_month).order_by('-Date')
  today = timezone.now()
  month = today.strftime('%B')
  total = 0
  for instance in queryset:
      total += instance.Amount
  context = {
      'month': month,
      'queryset': queryset,
      'total': total,
  }
  return render(request, 'accountantapp/salaryindex.html', context)

# def expenditurereport(request):
def expenditurereport(request):
  current_month = datetime.datetime.now().month
  queryset = Spend.objects.all().filter(Date__month=current_month).order_by('-Date')
  today = timezone.now()
  month = today.strftime('%B')
  total = 0
  for instance in queryset:
      total += instance.Amount
  context = {
      'month': month,
      'queryset': queryset,
      'total': total,
  }
  return render(request, 'accountantapp/expenditureindex.html', context)

# calculating totals in sundryexpense report
def sundryreport(request):
  current_month = datetime.datetime.now().month
  queryset = Sundry.objects.filter(Date__month=current_month).order_by('-Date')
  today = timezone.now()
  month = today.strftime('%B')
  total = 0
  for instance in queryset:
      total += instance.Amount
  context = {
      'month': month,
      'queryset': queryset,
      'total': total,
  }
  return render(request, 'accountantapp/sundryindex.html', context)


      ####################################################
      #        GENERATING REPORTS IN FORM OF PDFS         #
      ####################################################

# Printing Expenditure Report
class expenditurepdf(View):
  def get(self, request):
      current_month = datetime.datetime.now().month
      expense = Spend.objects.filter(Date__month=current_month).order_by('-Date')

      today = timezone.now()
      month = today.strftime('%B')
      totalexpense = 0
      for instance in expense:
          totalexpense += instance.Amount
      expensecontext = {

          'month': month,
          'today': today,
          'expense': expense,
          'request': request,
          'totalexpense': totalexpense,
      }
      return Render.render('accountantapp/expenditurepdf.html', expensecontext)

# Printing Salaries Report
class salariespdf(View):
  def get(self, request):
      current_month = datetime.datetime.now().month
      salaries = Salary.objects.filter(Date__month=current_month).order_by('-Date')
      today = timezone.now()
      month = today.strftime('%B')
      totalsalary = 0
      for instance in salaries:
          totalsalary += instance.Amount
      salarycontext = {
          'month': month,
          'today': today,
          'salaries': salaries,
          'request': request,
          'totalsalary': totalsalary,
      }
      return Render.render('accountantapp/pdf.html', salarycontext)

# Printing Sundry Expenses Report
class sundrypdf(View):
  def get(self, request):
      current_month = datetime.datetime.now().month
      sundry = Sundry.objects.filter(Date__month=current_month).order_by('-Date')
      today = timezone.now()
      month = today.strftime('%B')
      totalsundry = 0
      for instance in sundry:
          totalsundry += instance.Amount
      sundrycontext = {
          ''
          'month': month,
          'today': today,
          'sundry': sundry,
          'request': request,
          'totalsundry': totalsundry,
      }
      return Render.render('accountantapp/sundrypdf.html', sundrycontext)




      ####################################################
      #       PRINTING THE RECEIPTS                      #
      ####################################################

class expensereceipt(View):
    def get(self, request, pk):
      expense = get_object_or_404(Spend,pk=pk)
      today = timezone.now()
      expensecontext = {
          'today': today,
          'expense': expense,
          'request': request,
      }
      return Render.render('accountantapp/expensereceipt.html', expensecontext)

class salaryreceipt(View):
  def get(self, request, pk):
      salary = get_object_or_404(Salary,pk=pk)
      today = timezone.now()
      salarycontext = {
          'today': today,
          'salary': salary,
          'request': request,
      }
      return Render.render('accountantapp/salaryreceipt.html', salarycontext)

class sundryreceipt(View):
  def get(self, request,pk):
      sundry = get_object_or_404(Sundry, pk=pk)
      today = timezone.now()
      sundrycontext = {
          'today': today,
          'sundry': sundry,
          'request': request,
      }
      return Render.render('accountantapp/sundryreceipt.html', sundrycontext)

  ####################################################
  #        ARCHIVING OF THE MONTHLY REPORTS          #
  ####################################################

def salaryarchive(request):
  queryset = Salary.objects.all().order_by('-Date')
  total = 0
  for instance in queryset:
      total += instance.Amount
  context = {
      'queryset': queryset,
      'total': total,
  }
  return render(request, 'accountantapp/salaryarchive.html', context)

def expenditurearchive(request):
  queryset = Spend.objects.all().order_by('-Date')
  total = 0
  for instance in queryset:
      total += instance.Amount
  context = {
      'queryset': queryset,
      'total': total,
  }
  return render(request, 'accountantapp/expenditurearchive.html', context)

# calculating totals in sundryexpense report
def sundryarchive(request):
  queryset = Sundry.objects.all().order_by('-Date')
  total = 0
  for instance in queryset:
      total += instance.Amount
  context = {
      'queryset': queryset,
      'total': total,
  }
  return render(request, 'accountantapp/sundryarchive.html', context)



    ####################################################
    #        GENERATING REPORTS IN FORM OF ANNUAL PDFS #
    ####################################################


# Printing Expenditure archived Report
class expenditurearchivepdf(View):
    def get(self, request):
        expense = Spend.objects.all().order_by('-Date')
        today = timezone.now()
        month = today.strftime('%B')
        totalexpense = 0
        for instance in expense:
            totalexpense += instance.Amount
        expensecontext = {
            'today': today,
            'expense': expense,
            'request': request,
            'totalexpense': totalexpense,
        }
        return Render.render('accountantapp/expenditurearchivepdf.html', expensecontext)


# Printing Salaries archived Report
class salaryarchivepdf(View):
    def get(self, request):
        salaries = Salary.objects.all().order_by('-Date')
        today = timezone.now()
        totalsalary = 0
        for instance in salaries:
            totalsalary += instance.Amount
        salarycontext = {
            'today': today,
            'salaries': salaries,
            'request': request,
            'totalsalary': totalsalary,
        }
        return Render.render('accountantapp/salaryarchivepdf.html', salarycontext)


# Printing Sundry Expenses archived Report
class sundryarchivepdf(View):
    def get(self, request):
        sundry = Sundry.objects.all().order_by('-Date')
        today = timezone.now()
        totalsundry = 0
        for instance in sundry:
            totalsundry += instance.Amount
        sundrycontext = {
            'today': today,
            'sundry': sundry,
            'request': request,
            'totalsundry': totalsundry,
        }
        return Render.render('accountantapp/sundryarchivepdf.html', sundrycontext)




####################################################################
# The manager views start
######################################################################





































