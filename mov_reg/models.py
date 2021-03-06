from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Vehicle_Detail(models.Model):
    VehicleNo = models.CharField(max_length=10,default=None)
    Amount = models.DecimalField(null=True,blank=True,max_digits=19, decimal_places=2)
    Reason = models.CharField(max_length=100,default=None)
    Reason_Id = models.IntegerField(default=0)
    Date = models.CharField(max_length=10)
    def save(self,*args,**kwargs):
        char_fields = [f.name for f in Vehicle_Detail._meta.fields if isinstance(f, models.CharField)]
        if getattr(self,'Reason',False) != 'InvoiceNo':
                setattr(self,'Amount',-getattr(self,'Amount',False))
        for f in char_fields:
            val = getattr(self,f,False)
            if val:
                setattr(self,f,val.upper())
        super(Vehicle_Detail,self).save(*args,**kwargs)
class Movement(models.Model):
    Party =	models.CharField(max_length=100,null=True,blank=True)
    ACofParty = models.CharField(max_length=100,null=True,blank=True)
    Movement = models.CharField(max_length=100,null=True,blank=True)
    Size = models.IntegerField(null=True,blank=True)
    PartyRef = models.CharField(max_length=100,null=True,blank=True)
    ContainerNo =	models.CharField(max_length=100,null=True,blank=True)
    From =	models.CharField(max_length=100,null=True,blank=True)
    To1 =	models.CharField(max_length=100,null=True,blank=True)
    To2 =	models.CharField(max_length=100,null=True,blank=True)
    VehicleNo = models.CharField(max_length=100,null=True,blank=True)
    TransporterName = models.CharField(max_length=100,null=True,blank=True)
    InvoiceNo	= models.IntegerField(null=True,blank=True)
    InvoiceDate =	models.CharField(max_length=100,null=True,blank=True)
    InvoiceAmount =	models.IntegerField(null=True,blank=True)
    TripSheetNo = models.IntegerField(null=True,blank=True)
    TripSheetAmount =	models.IntegerField(null=True,blank=True)
    TripSheetDate	= models.CharField(max_length=100,null=True,blank=True)
    CashAdvance =	models.IntegerField(null=True,blank=True)
    ChequeAdvance =	models.IntegerField(null=True,blank=True)
    Fixed_Advance =	models.IntegerField(null=True,blank=True)
    Diesel =	models.IntegerField(null=True,blank=True)
    Alloted_Diesel = models.DecimalField(null=True,blank=True,max_digits=19, decimal_places=2)
    Diesel_Advance	= models.DecimalField(null=True,blank=True,max_digits=19, decimal_places=2)
    Status	= models.CharField(max_length=100,null=True,blank=True)
    Driver_Name = models.CharField(max_length=100,null=True,blank=True)
    def get_absolute_url(self):
        return reverse('mov_details', args=[str(self.id)])
    def save(self,*args,**kwargs):
        char_fields = [f.name for f in Movement._meta.fields if isinstance(f, models.CharField)]
        for f in char_fields:
            val = getattr(self,f,False)
            if val:
                setattr(self,f,val.upper())
        super(Movement,self).save(*args,**kwargs)
