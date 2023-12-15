from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from evproject import settings

from .models import Admin
from .models import Vehicle
from .models import Customer
from .models import EVModel
from .models import Colors
from .models import Quotation
from .models import Booking
from .models import Payment
from .models import Delivery



from datetime import date, datetime
from django.core.mail import send_mail, EmailMultiAlternatives


# Create your views here

def index(request):
    return render(request, 'evapp/index.html')


def adminhome(request):
    return render(request, 'evapp/adminhome.html')


def customerhome(request):
    return render(request, 'evapp/customerhome.html')


# admin signin form
def adminsigninform(request):
    return render(request, 'evapp/adminsigninform.html')


def customersignupform(request):
    return render(request, 'evapp/customersignupform.html')


# load customersignupform
def adminsignin(request):
    # get the input
    vemailid = request.POST.get("textemail")
    vpassword = request.POST.get("textpassword")
    request.session["session_emailid"] = vemailid
    request.session["session_password"] = vpassword

    # check if input matches with admin table row
    try:
        adminobj = Admin.Objects.get(emailid=vemailid, password=vpassword)
        return render(request, 'evapp/adminhome.html')
    except:
        messages = "Invalid login"
        return render(request, 'evapp/loginmessages.html', {"messages": messages})


def customersignup(request):
    vname = request.POST.get("textname")
    vemailid = request.POST.get("textemail")
    vpassword = request.POST.get("textpassword")
    vphone = request.POST.get("textphone")
    vaddress = request.POST.get("textaddress")
    vcity = request.POST.get("textcity")
    vpincode = request.POST.get("textpincode")

    # save in database table
    # create onject for customer class
    customerobj = Customer(name=vname, emailid=vemailid, password=vpassword, phone=vphone, address=vaddress, city=vcity,
                           pincode=vpincode)
    customerobj.save()
    request.session["messages"] = "registration successful"
    return render(request, 'evapp/loginmessages.html')



# customer signin form
def customersigninform(request):
    return render(request, 'evapp/customersigninform.html')


def customersignin(request):
    # get the input
    vemailid = request.POST.get("textemail")
    vpassword = request.POST.get("textpassword")
    try:
        customerobj = Customer.Objects.get(emailid=vemailid, password=vpassword)
        request.session["session_emailid"] = vemailid
        request.session["session_password"] = vpassword
        request.session["session_customercode"] = customerobj.customercode
        request.session["session_name"] = customerobj.name

        request.session["session_phone"] = customerobj.phone
        request.session["session_address"] = customerobj.address


        return render(request, 'evapp/customerhome.html')
    except:
        request.session["messages"] = "Invalid Login"
        return render(request, 'evapp/loginmessages.html')




def adminchangepasswordform(request):
    return render(request, 'evapp/adminchangepasswordform.html')


def adminchangepassword(request):
    # from session
    vemailid = request.session["session_emailid"]
    vpassword = request.session["session_password"]

    # get the input from form
    vcurrentpassword = request.POST.get("textcurrentpassword")
    vnewpassword = request.POST.get("textnewpassword")
    vconfirmpassword = request.POST.get("textconfirmpassword")

    if vnewpassword == vconfirmpassword:
        if vpassword == vcurrentpassword:
            adminobj = Admin.Objects.get(emailid=vemailid)
            adminobj.password = vnewpassword
            adminobj.save()
            request.session["session_password"] = vnewpassword
            messages = "Password Changed"
            return render(request, 'evapp/adminmessages.html', {"messages": messages})


        else:
            messages = "Invalid Current Password"
            return render(request, 'evapp/adminmessages.html', {"messages": messages})


    else:
        messages = "New and Confirm Password do not exist"
        return render(request, 'evapp/adminmessages.html', {"messages": messages})




def customerchangepasswordform(request):
    return render(request, 'evapp/customerchangepasswordform.html')


def customerchangepassword(request):
    # from session
    vemailid = request.session["session_emailid"]
    vpassword = request.session["session_password"]

    # get the input from form
    vcurrentpassword = request.POST.get("textcurrentpassword")
    vnewpassword = request.POST.get("textnewpassword")
    vconfirmpassword = request.POST.get("textconfirmpassword")

    if vnewpassword == vconfirmpassword:
        if vpassword == vcurrentpassword:
            customerobj = Customer.Objects.get(emailid=vemailid)
            customerobj.password = vnewpassword
            customerobj.save()
            request.session["session_password"] = vnewpassword
            messages = "Password Changed"
            return render(request, 'evapp/messages.html', {"messages": messages})


        else:
            messages = "Invalid Current Password"
            return render(request, 'evapp/messages.html', {"messages": messages})


    else:
        messages = "New and Cofirm Password do not exist"
        return render(request, 'evapp/messages.html', {"messages": messages})




def addvehicleform(request):
    return render(request, 'evapp/addvehicleform.html')


def addvehicle(request):
    vmodelname = request.POST.get("textmodelname")
    vbrand = request.POST.get("textbrand")

    # insert row into vehicle table

    vehicleobj = Vehicle(brand=vbrand, modelname=vmodelname)
    vehicleobj.save()
    messages = "Vehicle Saved"
    return render(request, 'evapp/adminmessages.html', {"messages": messages})




def viewvehicle(request):
    vehicleobj = Vehicle.Objects.all()
    c=len(vehicleobj)
    return render(request, 'evapp/viewvehicle.html', {'vehicleobj': vehicleobj, 'count':c})


def addmodelforminfo(request, s):
    return render(request, 'evapp/addmodelform.html', {'modelname': s})


def viewmodeldetails(request, s):
    evmodelobj = EVModel.Objects.filter(modelname=s)
    c = len(evmodelobj)
    return render(request, 'evapp/viewmodel.html', {'evmodelobj': evmodelobj, 'count': c})




def addcolorform(request, x, y):
    return render(request, 'evapp/addcolorform.html', {'modelname': x, 'modelid': y})


def addcolor(request):
    # all the formfields ara available as dict items
    formfields = dict(request.POST.items())

    # get image upload
    image = request.FILES["photo"]

    # get other input values
    for k, v in formfields.items():
        if k == "textmodelname":
            vmodelname = v
        elif k == "textmodelid":
            vmodelid = v
        elif k == "textcolor":
            vcolor = v
        elif k == "textstock":
            vstock = v

    # upload image to server
    fs = FileSystemStorage()
    vimagefilename = fs.save(image.name, image)

    # insert row into product table
    vehicleobj = Vehicle.Objects.get(modelname=vmodelname)
    evmodelobj = EVModel.Objects.get(modelid=vmodelid)
    colorsobj = Colors(modelid=evmodelobj, modelname=vehicleobj, color=vcolor, image=vimagefilename, stock=vstock)
    colorsobj.save()
    messages = "Color Saved"
    return render(request, 'evapp/adminmessages.html', {"messages": messages})


def viewcolor(request):
    colorsobj = Colors.Objects.all()
    return render(request, 'evapp/viewcolor.html', {'colorsobj': colorsobj})




def browsevehicle(request):
    # fetch all vehicle from table and display in browsevehicle.html
    # select * from vehicle
    vehicleobj = Vehicle.Objects.all()
    c = len(vehicleobj)
    return render(request, 'evapp/browsevehicle.html', {'vehicleobj': vehicleobj, 'count':c})


def browsemodel(request, x):
    # fetch all vehicle from table and display in browsevehicle.html
    # select * from vehicle
    evmodelobj = EVModel.Objects.filter(modelname=x)
    c = len(evmodelobj)
    return render(request, 'evapp/browsemodel.html', {'evmodelobj': evmodelobj, 'count':c})


def quotationform(request, a, b):
    request.session["colorid"] = b
    request.session["color"] = a
    return render(request, 'evapp/quotationform.html')


def browsecolor(request, x, y, z):
    # fetch all vehicle from table and display in browsevehicle.html
    # select * from vehicle

    # store modelname, modelid, mrp in session

    request.session["modelid"] = y
    request.session["modelname"] = x
    request.session["mrp"] = z
    colorsobj = Colors.Objects.filter(modelname=x, modelid=y)
    c = len(colorsobj)
    return render(request, 'evapp/browsecolor.html', {'colorsobj': colorsobj,'count':c})


def addmodel(request):
    vmodelname = request.POST.get("textmodelname")
    vgear = request.POST.get("textgear")
    vdimension = request.POST.get("textdimension")
    vbatterycapacity = request.POST.get("textbatterycapacity")
    vwheel = request.POST.get("textwheel")
    vbrake = request.POST.get("textbrake")
    vspeed = request.POST.get("textspeed")
    vemission = request.POST.get("textemission")
    vusb = request.POST.get("textusb")
    vchargingtime = request.POST.get("textchargingtime")
    vmrp = request.POST.get("textmrp")
    vwarranty = request.POST.get("textwarranty")
    vdescription = request.POST.get("textdescription")

    # insert row into vehicle table
    vehicleobj = Vehicle.Objects.get(modelname=vmodelname)
    evmodelobj = EVModel(modelname=vehicleobj, gear=vgear, dimension=vdimension, batterycapacity=vbatterycapacity,
                         wheel=vwheel,
                         brake=vbrake, speed=vspeed, emission=vemission, usb=vusb, chargingtime=vchargingtime, mrp=vmrp,
                         warranty=vwarranty,
                         description=vdescription)
    evmodelobj.save()
    messages = "EV Model Saved"
    return render(request, 'evapp/adminmessages.html', {"messages": messages})

def quotation(request):
    vavailfinance = request.POST.get("textavailfinance")
    vquotationdate = date.today()
    vcustomercode = request.session["session_customercode"]
    customerobj = Customer.Objects.get(customercode=vcustomercode)
    mrp = request.session["mrp"]
    mrp = int(mrp)
    vtax = mrp*.05
    vtotalamount = mrp+vtax
    colorsobj = Colors.Objects.get(colorid=request.session["colorid"])
    quotationobj = Quotation(customercode=customerobj, colorid=colorsobj,quotationdate=vquotationdate, availfinance=vavailfinance,
                             price=mrp,tax=vtax, totalamount=vtotalamount)
    quotationobj.save()
    qn = Quotation.Objects.latest("quotationnumber").quotationnumber
    quotationobjget = Quotation.Objects.get(quotationnumber=qn)

    return render(request, 'evapp/viewquotationform.html',{'quotationobjget': quotationobjget})


def viewquotationform(request, x, y, a, b, c):

    request.session["session_name"] = a
    request.session["session_phone"] = b
    request.session["session_address"] = c
    request.session["modelname"] = x
    request.session["color"] = y
    colorsobj = Colors.Objects.all()
    customerobj = Customer.Objects.get(name=a, phone=b, address=c)
    quotationobj = Quotation.Objects.all()

    return render(request, 'evapp/viewquotationform.html', {'quotationobj': quotationobj, 'colorsobj': colorsobj,
                                                            'customerobj': customerobj})

def viewallquotationform(request):

    vcustomercode = request.session["session_customercode"]
    query1="select quotationnumber, quotationdate, availfinance, tax, price, totalamount, quotation.colorid," \
           " colors.color, colors.modelname, colors.modelid" \
           " from quotation inner join colors on quotation.colorid=colors.colorid where customercode=%s"
    quotationobject = Quotation.Objects.raw(query1,[vcustomercode])
    return render(request, 'evapp/viewallquotationform.html',{'quotationobjget': quotationobject})

def bookingform(request, quotationnumber, totalamount):

    return render(request, 'evapp/bookingform.html', {'quotationnumber': quotationnumber, 'totalamount': totalamount})



def bookings(request):
    vquotationnumber = request.POST.get("textquotationnumber")

    vdeliverytype = request.POST.get("deliverytype")
    vbookingdate = date.today()
    vdeliverydate = request.POST.get("textdeliverydate")
    vadvancepaid = request.POST.get("textadvancepaid")
    vbalance = request.POST.get("textbalance")
    quotationobj =Quotation.Objects.get(quotationnumber=vquotationnumber)
    bookingobj = Booking(quotationnumber=quotationobj,deliverytype=vdeliverytype,
                             bookingdate=vbookingdate,deliverydate=vdeliverydate, advancepaid=vadvancepaid, balance=vbalance)
    bookingobj.save()
    messages = "Booking successful"
    return render(request, 'evapp/messages.html', {"messages": messages})





def viewbookings(request):

    query1 = " select bookingid, booking.quotationnumber,quotation.customercode,name,advancepaid," \
             " deliverytype,deliverydate,quotation.colorid,color,balance from booking inner join quotation on" \
             " booking.quotationnumber=quotation.quotationnumber inner join customer on " \
             "quotation.customercode=customer.customercode inner join colors on quotation.colorid=colors.colorid "
    bookingobj = list(Booking.Objects.raw(query1))
    c = len(bookingobj)
    return render(request, 'evapp/viewbookings.html', {'bookingobj': bookingobj, 'count':c})


def viewbookingforpayment(request):
    query1 = " select bookingid, booking.quotationnumber,quotation.customercode,name,advancepaid," \
             " deliverytype,deliverydate,quotation.colorid,color,balance from booking inner join quotation on" \
             " booking.quotationnumber=quotation.quotationnumber inner join customer on " \
             "quotation.customercode=customer.customercode inner join colors on " \
             "quotation.colorid=colors.colorid where balance>0 "
    bookingobj = list(Booking.Objects.raw(query1))
    count = len(bookingobj)
    return render(request, 'evapp/viewbookingforpayment.html', {'bookingobj': bookingobj,'count':count})

def paymentform(request, x, y):
    request.session["bookingid"] = x
    request.session["balance"] = y
    return render(request, 'evapp/paymentform.html', {'x': x, 'y': y})

#customer
def payment(request):
    vamountpaid = request.POST.get("textamountpaid")
    vpaiddate = request.POST.get("textpaiddate")
    vtransactionid = request.POST.get("texttransactionid")
    x = request.session["bookingid"]
    y = request.session["balance"]
    query2 = "select name, emailid, customercode, phone from customer where customercode in (select customercode from quotation where " \
             " quotationnumber in(select quotationnumber from booking where bookingid=%s))"
    customerobj = list(Customer.Objects.raw(query2,[x]))
    name = customerobj[0].name
    phone = customerobj[0].phone
    vemailid = customerobj[0].emailid


    #
    query1 = "select * from vehicle where modelname in (select modelname from colors where colorid in " \
              "(select colorid from quotation where quotationnumber in(select quotationnumber from booking where bookingid =%s)));"
    vehicleobj = list(Vehicle.Objects.raw(query1, [x]))
    brand = vehicleobj[0].brand
    modelname = vehicleobj[0].modelname

    #
    bookingobj = Booking.Objects.get(bookingid=x)
    paymentobj = Payment(amountpaid=vamountpaid, paiddate=vpaiddate, transactionid=vtransactionid, bookingid=bookingobj)
    paymentobj.save()

    bookingobj.balance = bookingobj.balance-int(vamountpaid)
    bookingobj.save()
    vbalance = bookingobj.balance
    deliveryobj = Delivery.Objects.get(bookingid=x)
    vservice1 = deliveryobj.service1
    vservice2 = deliveryobj.service2
    vservice3 = deliveryobj.service3

    #

    #
    subject = 'Bill'
    subject, from_email, to = 'Bill', 'evappa7@gmail.com', vemailid
    html_content = render_to_string('evapp/billmail.html',
                                    {
                                        'name':name,
                                    'phone':phone,
                                     'brand': brand,
                                     'modelname': modelname,
                                     'amountpaid': vamountpaid,
                                     'paiddate': vpaiddate,
                                     'balance': vbalance,
                                        'service1': vservice1,
                                        'service2': vservice2,
                                        'service3': vservice3,

                                      })
    text_content = strip_tags(html_content)
    #strip  the html tag. So people can see the pure text at least

    #create the email, and attach the HTML version as well
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # message="Customer Name :"+name+"\n"
    # message+="Phone :"+phone+"\n"
    # message+= "Brand :"+brand+"\n"
    # message+="Model name : "+modelname+"\n"
    # message+= "Amount Paid :"+str(vamountpaid)+"\n"
    # message+= "Paid on :"+vpaiddate+"\n"
    # message+="Balance :"+str(vbalance)+"\n"
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [vemailid, ]
    #res = send_mail(subject, message, email_from, recipient_list, fail_silently=True)
    messages = "Payment successful and mail sent to customer"
    return render(request, 'evapp/adminmessages.html', {"messages": messages})



def viewpayment(request):
    query1 = " select transactionid, payment.bookingid, amountpaid, paiddate, booking.balance from booking inner join payment " \
             "on payment.bookingid=booking.bookingid"
    paymentobj = list(Payment.Objects.raw(query1))
    c = len(paymentobj)

    return render(request, 'evapp/viewpayment.html', {'paymentobj': paymentobj, 'count':c})

def customerpayment(request):
    query1 = " select payment.bookingid,amountpaid,paiddate,transactionid, balance from payment inner join booking on payment.bookingid=booking.bookingid" \
             " where booking.bookingid in (select bookingid from booking where" \
             " quotationnumber in(select quotationnumber from quotation where customercode=%s )) "
    x = request.session["session_customercode"]
    paymentobj = list(Payment.Objects.raw(query1,[x]))

    return render(request, 'evapp/customerpayment.html', {'paymentobj': paymentobj})


def admindeliveryform(request, x):
    request.session["bookingid"] = x
    return render(request, 'evapp/admindeliveryform.html', {'x': x})


def admindelivery(request):
    x = request.session["bookingid"]
    vchassisnumber = request.POST.get("textchassisnumber")
    vservice1 = request.POST.get("textservicedate1")
    vservice2 = request.POST.get("textservicedate2")
    vservice3 = request.POST.get("textservicedate3")
    bookingobj = Booking.Objects.get(bookingid=x)
    deliveryobj = Delivery(bookingid=bookingobj.bookingid, chassisnumber=vchassisnumber, service1=vservice1,service2=vservice2,service3=vservice3 )
    deliveryobj.save()
    messages = "Delivery successful"
    return render(request, 'evapp/adminmessages.html', {"messages": messages})



def chatbot(request):
    return render(request, 'evapp/chatbot.html')

def adminlogout(request):
    request.session["session_emailid"] = None
    request.session["session_password"] = None
    request.session["selected_emailid"] = None
    request.session["messages"] = None
    return render(request, 'evapp/adminsigninform.html')

def customerlogout(request):
    request.session["session_emailid"] = None
    request.session["session_password"] = None
    request.session["session_password"] = None
    request.session["selected_emailid"] = None
    request.session["messages"] = None
    return render(request, 'evapp/customersigninform.html')

def forgotpasswordform(request):
    return render(request, 'evapp/forgotpasswordform.html')

def forgotpassword(request):
    emailid = request.POST.get("textemailid")
    customerobj = Customer.Objects.get(emailid=emailid)
    password = customerobj.password
    name = customerobj.name

    subject = 'Password Forgot Request'
    message = 'Hi  ' + name + ',Your Password is' + password
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [emailid, ]
    res = send_mail(subject, message, email_from, recipient_list,fail_silently=True)
    request.session["messages"] = 'Hi ' + name + ", Please Check Your Mail for Password."
    return render(request,'evapp/loginmessages.html')

def contactus(request):
    return render(request, 'evapp/contactus.html')

def salesreportform(request):
    return render(request, 'evapp/salesreportform.html')

def salesreport(request):
    vfromdate = request.POST.get("textfromdate")
    vtodate = request.POST.get("texttodate")
    query1 = " select booking.bookingid, quotation.colorid,count(*) as 'soldvehicles', sum(totalamount) as" \
             " 'totalamount',colors.modelname from quotation inner join booking on" \
             " quotation.quotationnumber=booking.quotationnumber inner join colors on colors.colorid=quotation.colorid " \
             " where bookingdate between %s and %s group by modelname "
    bookingobj = Booking.Objects.raw((query1),[vfromdate, vtodate])
    return render(request, 'evapp/viewsales.html',{'bookingobj':bookingobj, 'fromdate': vfromdate, 'todate':vtodate})

















