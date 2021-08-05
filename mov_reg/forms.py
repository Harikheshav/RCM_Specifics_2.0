from django import forms
from .models import Movement,Vehicle_Detail
import os
import floppyforms
class Vehicle_Detail_Form(forms.ModelForm):
    class Meta:
        model = Vehicle_Detail
        fields = '__all__'
        exclude = ['Reason_Id']
        widgets={
        'VehicleNo':floppyforms.TextInput(
        attrs={'class':'form-control','autocomplete': 'off'}), 
        'Amount':floppyforms.TextInput(
        attrs={'class':'form-control','placeholder':'If amount is a expense add(-) sign','autocomplete': 'off'}),
        'Reason':floppyforms.TextInput(
        attrs={'class':'form-control','autocomplete': 'off'}),
        'Date':floppyforms.TextInput(
        attrs={'class':'form-control','autocomplete': 'off'})}
class MovementForm(forms.ModelForm):
    class Meta:
        model=Movement
        fields='__all__'
        exclude=['Alloted_Diesel','Fixed_Advance','Fixed_Diesel_Advance']
        widgets={
        'Party':floppyforms.TextInput(
        attrs={'class':'form-control','autocomplete': 'off'}), 
        'ACofParty': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
        'Movement': floppyforms.TextInput(datalist=['Import','Export','Offload','Empty'],attrs={'class':'form-control','autocomplete':'off'}),
        'PartyRef': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
		'InvoiceNo': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
		'InvoiceDate': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),        
        'Size': floppyforms.TextInput(datalist=[20,40],attrs={'class':'form-control','autocomplete':'off'}),
        'ContainerNo': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
        'From': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
		'To1': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
		'To2': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
		'VehicleNo': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
        'TransporterName': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
		'InvoiceAmount': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
		'TripSheetNo': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
		'TripSheetAmount': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
		'TripSheetDate': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
		'CashAdvance': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
		'ChequeAdvance': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
		'Diesel': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
	    'Diesel_Advance': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
	    'Status': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}), 
        'Driver_Name': floppyforms.TextInput(attrs={'class':'form-control','autocomplete':'off'}) }