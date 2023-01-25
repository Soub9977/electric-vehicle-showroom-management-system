from.import views
from django.conf.urls import url



urlpatterns=[

    url(r'^index/$', views.index, name="load index page"),
    url(r'^adminhome/$', views.adminhome, name="load admin page"),
    url(r'^customerhome/$', views.customerhome, name="load customer page"),
    url(r'^customersignupform/$', views.customersignupform, name="customersignupform html"),
    url(r'^customersignup/$', views.customersignup, name="signupcode"),
    url(r'^adminsigninform/$', views.adminsigninform, name="adminsigninform html"),
    url(r'^adminsignin/$', views.adminsignin, name="adminsignincode"),
    url(r'^customersigninform/$', views.customersigninform, name="customersigninform html"),
    url(r'^customersignin/$', views.customersignin, name="customersignincode"),
    url(r'^adminchangepasswordform/$', views.adminchangepasswordform, name="changepasswordform"),
    url(r'^adminchangepassword/$', views.adminchangepassword, name="changepassword code"),
    url(r'^customerchangepasswordform/$', views.customerchangepasswordform, name="changepasswordform"),
    url(r'^customerchangepassword/$', views.customerchangepassword, name="changepassword code"),
    url(r'^addvehicleform/$', views.addvehicleform, name="addvehcileform html"),
    url(r'^addvehicle/$', views.addvehicle, name="add vehicle code"),
    url(r'^viewvehicle/$', views.viewvehicle, name="view vehicles"),
    url(r'^addmodelform/$', views.viewvehicle, name="add model form"),
    url(r'^addmodelforminfo/([\w-]+)/$', views.addmodelforminfo, name="add model form"),

    url(r'^addmodel/$', views.addmodel, name="add model code"),
    url(r'^viewmodel/$', views.viewvehicle, name="view models"),
    url(r'^viewmodeldetails/([\w-]+)/$', views.viewmodeldetails, name="view models"),

    url(r'^addcolorform/([\w-]+)/(\d+)/$', views.addcolorform, name="add model form"),
    url(r'^addcolor/$', views.addcolor, name="add model code"),
    url(r'^viewcolor/$', views.viewcolor, name="view color"),
    url(r'^browsevehicle/$', views.browsevehicle, name="browse vehicle code"),
    url(r'^browsemodel/([\w-]+)/$', views.browsemodel, name="browse model code"),
    url(r'^browsecolor/([\w-]+)/(\d+)/(\d+)/$', views.browsecolor, name="browse color code"),
    url(r'^quotationform/([\w-]+)/([\w-]+)/$', views.quotationform, name=" quotation form"),
    url(r'^quotation/$', views.quotation, name=" quotation code"),
    url(r'^viewquotationform/([\w-]+)/([\w-]+)/([\w-]+)/([\w-]+)/([\w-]+)/$', views.viewquotationform, name=" view quotation form"),
    url(r'^viewallquotationform/$', views.viewallquotationform, name=" view all quotation"),
    url(r'^bookingform/(\d+)/([0-9]+\.?[0-9]+)/$', views.bookingform, name="booking form"),
    url(r'^bookings/$', views.bookings, name="booking code"),
    url(r'^viewbookings/$', views.viewbookings, name="view booking"),
    url(r'^viewbookingforpayment/$', views.viewbookingforpayment, name="view booking payment"),
    url(r'^paymentform/(\d+)/([0-9]+\.?[0-9]+)/$', views.paymentform, name="payment code"),
    url(r'^payment/$', views.payment, name="payment process"),
    url(r'^viewpayment/$', views.viewpayment, name="view payment"),
    url(r'^customerpayment/$', views.customerpayment, name="view customer payment"),
    url(r'^admindeliveryform/(\d+)/$', views.admindeliveryform, name="Admin Delivery Form"),
    url(r'^admindelivery/$', views.admindelivery, name="Admin Delivery Process"),
    url(r'^chatbot/$', views.chatbot, name="ChatBot Process"),
    url(r'^adminlogout/$', views.adminlogout, name="admin logout"),
    url(r'^customerlogout/$', views.customerlogout, name="customer logout"),
    url(r'^forgotpasswordform/$', views.forgotpasswordform, name="forgot password form"),
    url(r'^forgotpassword/$', views.forgotpassword, name="Forgot password code"),
    url(r'^billmail/$', views.forgotpassword, name="Forgot password code"),
    url(r'^contactus/$', views.contactus, name="Contact Us"),
    url(r'^salesreportform/$', views.salesreportform, name="sales report form"),
    url(r'^salesreport/$', views.salesreport, name="sales report process"),









]
