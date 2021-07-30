from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
# Create your models here.
class Vehicle_Detail(models.Model):
    VehicleNo = models.CharField(max_length=10,default=None)
    Amount = models.IntegerField()
    Reason = models.CharField(max_length=100,default=None)
    Reason_Id = models.IntegerField(default=0)
    Date = models.CharField(max_length=10,default=date.today().strftime("%d-%m-%Y"))
    def save(self,*args,**kwargs):
        char_fields = [f.name for f in Vehicle_Detail._meta.fields if isinstance(f, models.CharField)]
        if getattr(self,'Reason',False) != 'InvoiceNo':
                setattr(self,'Amount',-getattr(self,'Amount',False))
        for f in char_fields:
            val = getattr(self,f,False)
            if val:
                setattr(self,f,val.upper())
        super(Vehicle_Detail,self).save(*args,**kwargs)
class File(models.Model):
    file = models.FileField(upload_to='')
class Movement(models.Model):
    Party =	models.CharField(max_length=50,null=True,blank=True)
    ACofParty = models.CharField(max_length=50,null=True,blank=True)
    Movement = models.CharField(max_length=10,null=True,blank=True)
    Size = models.IntegerField(null=True,blank=True)
    PartyRef = models.CharField(max_length=50,null=True,blank=True)
    ContainerNo =	models.CharField(max_length=11,null=True,blank=True)
    From =	models.CharField(max_length=30,null=True,blank=True)
    To1 =	models.CharField(max_length=30,null=True,blank=True)
    To2 =	models.CharField(max_length=30,null=True,blank=True)
    VehicleNo = models.CharField(max_length=10,null=True,blank=True)
    TransporterName = models.CharField(max_length=25,null=True,blank=True)
    InvoiceNo	= models.IntegerField(null=True,blank=True)
    InvoiceDate =	models.CharField(max_length=10,null=True,blank=True)
    InvoiceAmount =	models.IntegerField(null=True,blank=True)
    TripSheetNo = models.IntegerField(null=True,blank=True)
    TripSheetAmount =	models.IntegerField(null=True,blank=True)
    TripSheetDate	= models.CharField(max_length=10,null=True,blank=True,default=date.today().strftime("%d-%m-%Y"))
    CashAdvance =	models.IntegerField(null=True,blank=True)
    ChequeAdvance =	models.IntegerField(null=True,blank=True)
    Fixed_Advance =	models.IntegerField(null=True,blank=True)
    Diesel =	models.IntegerField(null=True,blank=True)
    Alloted_Diesel =	models.IntegerField(null=True,blank=True)
    Diesel_Advance	= models.IntegerField(null=True,blank=True)
    Fixed_Diesel_Advance =	models.IntegerField(null=True,blank=True)
    Status	= models.CharField(max_length=10,null=True,blank=True)
    Driver_Name = models.CharField(max_length=10,null=True,blank=True)
    def get_absolute_url(self):
        return reverse('mov_details', args=[str(self.id)])
    def save(self,*args,**kwargs):
        char_fields = [f.name for f in Movement._meta.fields if isinstance(f, models.CharField)]
        for f in char_fields:
            val = getattr(self,f,False)
            if val:
                setattr(self,f,val.upper())
        super(Movement,self).save(*args,**kwargs)