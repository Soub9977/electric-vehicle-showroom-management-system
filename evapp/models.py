from django.db import models


# Create your models here.

class Admin(models.Model):
    emailid = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=10, blank=True, null=True)
    Objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'admin'


class Vehicle(models.Model):
    brand = models.CharField(max_length=20, blank=True, null=True)
    modelname = models.CharField(primary_key=True, max_length=10, blank=True, null=False)
    Objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'vehicle'


class EVModel(models.Model):
    modelid = models.AutoField(primary_key=True)
    modelname = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='modelname', max_length=50, blank=True, null=True)
    gear = models.CharField(max_length=50, blank=True, null=True)
    dimension = models.CharField(max_length=50, blank=True, null=True)
    batterycapacity = models.CharField(max_length=50, blank=True, null=True)
    wheel = models.CharField(max_length=50, blank=True, null=True)
    brake = models.CharField(max_length=50, blank=True, null=True)
    speed = models.CharField(max_length=50, blank=True, null=True)
    emission = models.CharField(max_length=50, blank=True, null=True)
    usb = models.CharField(max_length=50, blank=True, null=True)
    chargingtime = models.CharField(max_length=50, blank=True, null=True)
    mrp = models.IntegerField(blank=True, null=True)
    warranty = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    Objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'evmodel'


class Colors(models.Model):
    colorid = models.AutoField(primary_key=True, blank=True, null=False)
    modelid = models.ForeignKey(EVModel, models.DO_NOTHING, db_column='modelid', max_length=50, blank=True,
                                  null=True)
    modelname = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='modelname', max_length=50, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    image = models.CharField(max_length=50, blank=True, null=True)
    imageback = models.CharField(max_length=50, blank=True, null=True)
    imageside = models.CharField(max_length=50, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    Objects = models.Manager()


    class Meta:
        managed = True
        db_table = 'colors'


class Customer(models.Model):
    customercode = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=10,blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    emailid = models.CharField(unique=True, max_length=50, blank=True, null=True)
    password = models.CharField(max_length=10, blank=True, null=True)
    Objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'customer'


class Quotation(models.Model):
    quotationnumber = models.AutoField(primary_key=True, blank=True, null=False)
    customercode = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customercode', blank=True, null=True)
    quotationdate = models.DateField(blank=True, null=True)
    colorid = models.ForeignKey(Colors, models.DO_NOTHING, db_column='colorid', blank=True, null=True)
    availfinance = models.CharField(max_length=3, blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    totalamount = models.FloatField(blank=True, null=True)
    Objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'quotation'


class Booking(models.Model):
    quotationnumber = models.ForeignKey(Quotation, models.DO_NOTHING, db_column='quotationnumber', blank=True,
                                        null=True)
    bookingid = models.AutoField(primary_key=True, blank=True, null=False)
    bookingdate = models.DateField(blank=True, null=True)
    deliverytype = models.CharField(max_length=20, blank=True, null=True)
    deliverydate = models.DateField(blank=True, null=True)
    advancepaid = models.FloatField(blank=True, null=True)
    balance = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, default='New', null=True)
    Objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'booking'


class Payment(models.Model):
    bookingid = models.ForeignKey(Booking, models.DO_NOTHING, db_column='bookingid', blank=True, null=True)
    amountpaid = models.FloatField(blank=True, null=True)
    paiddate = models.DateField(blank=True, null=True)
    transactionid = models.CharField(primary_key=True, max_length=20, blank=True, null=False)
    #balance = models.FloatField(blank=True, null=True)
    Objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'payment'


class Delivery(models.Model):
    bookingid = models.IntegerField(primary_key=True, blank=True, null=False)
    chassisnumber = models.CharField(max_length=20, blank=True, null=True)
    service1 = models.DateField(blank=True, null=True)
    service2 = models.DateField(blank=True, null=True)
    service3 = models.DateField(blank=True, null=True)
    Objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'delivery'

