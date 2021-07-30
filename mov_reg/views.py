from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Movement,Vehicle_Detail
from .forms import MovementForm,FileForm,Vehicle_Detail_Form
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import os
import pandas as pd
from excel_response import ExcelResponse
from django.utils.html import format_html
from datetime import date,timedelta,datetime
path='Template.xlsx'
sug_sales=['Party','ACofParty',]
not_varied=['Party','ACofParty','Movement','PartyRef','From','To1','To2','InvoiceNo']
sug_mov=['Party','ACofParty','From','To1','To2','VehicleNo','Driver_Name','TransporterName']
calc_data=['Alloted_Diesel','Fixed_Diesel_Advance','Fixed_Advance']
cols=['id','Party','ACofParty','Movement','Size','PartyRef','ContainerNo','From','To1','To2','VehicleNo','TransporterName','InvoiceNo','InvoiceDate','InvoiceAmount','TripSheetNo','TripSheetAmount','TripSheetDate','CashAdvance','ChequeAdvance','Fixed_Advance','Diesel','Alloted_Diesel','Diesel_Advance','Fixed_Diesel_Advance','Status','Driver_Name']
today=date.today().strftime("%d-%m-%Y")
def get_key(val,my_dict):
    for key, value in my_dict.items():
         if val in value:
             return key
    return 0              
def suggest(col_name):
    try:
        df=pd.DataFrame(list(Movement.objects.all().values()))
    except:
        df=pd.DataFrame(columns=cols)
    try:
        rcm_drivers_mob_no=pd.read_excel(path,na_filter=False,sheet_name='Driver_Mobile').to_dict()
        rcm_drivers=list(rcm_drivers_mob_no['Driver Name'].values())
    except:
        rcm_drivers_mob_no={}
        rcm_drivers=[]      
    if df.empty:
        return []
    elif col_name=='Driver_Name':
        return rcm_drivers + ["Other Company"]
    else:
        return list(filter(None,set(df[col_name].values.tolist())))
def validate_file(value):
    if not value.name.startswith('Template.xlsx'):
            if not value.name.endswith('Template.xlsx'):
                raise forms.ValidationError("Not the same file")
def calc_fixed(From=None,To_1=None,To_2=None):
    try:
        rcm_place_adv=pd.read_excel(path,na_filter=False,sheet_name='Place_Advance').values.tolist()
    except:
        rcm_place_adv=[]   
    for data in rcm_place_adv:
        if data[0]==From and data[1]==To_1 and data[2]==To_2:
            return data[3],data[4],data[5]
    return 0,0,0
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('/login')
class HomeView(ListView):
    model=Movement
    template_name='home.html'
    def get_queryset(self):
        return Movement.objects.exclude(Party__isnull = True).exclude(Party__exact = '').exclude(Party__exact = None).order_by('-id')
class MovDetailView(DetailView):
    model=Movement
    template_name='mov_details.html'
class AddMovView_Initial(CreateView):
    model=Movement
    form_class= MovementForm
    template_name='add_mov.html'
    def get_context_data(self, **kwargs):
        context = super(AddMovView_Initial, self).get_context_data(**kwargs)
        Id = int(str(Movement.objects.last()).split('(')[1].split(')')[0])
        initial_dict=Movement.objects.filter(id=Id).values()[0]
        initial_dict = {key: initial_dict[key] for key  in not_varied}
        context['form'] = MovementForm(initial=initial_dict)
        for field in sug_mov:
            context['form'].fields[field].widget.datalist=suggest(field)
        context['form_message']='The form has been saved!!!!!'
        return context
    def post(self, request, *args, **kwargs):
        form = MovementForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
    def form_valid(self, form):
        instances = form.save(commit=False)
        instances.Alloted_Diesel,instances.Fixed_Advance,instances.Fixed_Diesel_Advance= calc_fixed(instances.From,instances.To1,instances.To2)
        instances.save()
        return HttpResponseRedirect('/add_mov_init')
class AddMovView_Empty(CreateView):
    model=Movement
    form_class= MovementForm
    template_name='add_mov.html'
    def get_context_data(self, **kwargs):
        context = super(AddMovView_Empty, self).get_context_data(**kwargs)
        context['form'] = MovementForm()
        for field in sug_mov:
            context['form'].fields[field].widget.datalist=suggest(field)
        context['form'].fields['Size'].widget.datalist=[20,40]
        context['form'].fields['Movement'].widget.datalist=['Import','Export','Offload','Empty']
        return context
    def post(self, request, *args, **kwargs):
        form = MovementForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
    def form_valid(self, form):
        instances = form.save(commit=False)
        instances.Alloted_Diesel,instances.Fixed_Advance,instances.Fixed_Diesel_Advance= calc_fixed(str(instances.From),str(instances.To1),str(instances.To2))
        instances.save()
        return HttpResponseRedirect('/add_mov_init')
class UpdateMovView(UpdateView):
    model=Movement
    form_class= MovementForm
    template_name='update_mov.html'
    def form_valid(self, form):
        form.instance.Alloted_Diesel,form.instance.Fixed_Advance,form.instance.Fixed_Diesel_Advance= calc_fixed(str(form.instance.From),str(form.instance.To1),str(form.instance.To2)) 
        return super().form_valid(form)
class DeleteMovView(UpdateView):
    model=Movement
    template_name='delete_mov.html'
    fields='__all__'
    success_url=reverse_lazy('home')
def VehicleView(request):
        fields=['id','VehicleNo','CashAdvance','ChequeAdvance','Diesel_Advance','TripSheetAmount','InvoiceAmount','TripSheetDate']
        amounts=['CashAdvance','ChequeAdvance','Diesel_Advance','TripSheetAmount','InvoiceAmount']
        try:
            rcm_veh_nos=pd.read_excel(path,na_filter=False,sheet_name='Vehicle Numbers').values.tolist()
            rcm_veh_nos=[item for sublist in rcm_veh_nos for item in sublist]
        except:
            rcm_veh_nos=[]
        objs=list(Movement.objects.filter(VehicleNo__in = rcm_veh_nos).values(*fields))
        for obj in objs:
            for amount in amounts:
                veh_obj = Vehicle_Detail(VehicleNo=obj['VehicleNo'],Amount=obj[amount],Reason=amount,Reason_Id=obj['id'],Date=obj['TripSheetDate'])
                if obj[amount] is None: # If the field for the respective Id is None ignore
                    continue
                elif (Vehicle_Detail.objects.filter(Reason_Id=obj['id']).exists() and Vehicle_Detail.objects.filter(Reason=amount).exists()) : # If the field for the respective Id exists update amount(If no change its the same) 
                    Vehicle_Detail.objects.filter(Reason_Id=obj['id']).filter(Reason=amount).update(Amount=obj[amount])
                else: # If the field for the respective Id is new please save the respective object
                    veh_obj.save()
        objs2=Vehicle_Detail.objects.values('Amount')
        vals=list(objs2.values())
        total_inc = sum(val['Amount'] for val in vals if val['Amount']> 0 )
        total_exp = sum(val['Amount'] for val in vals if val['Amount']< 0 )
        total=total_inc+total_exp
        return render(request,'veh_list.html',{'veh_nos':rcm_veh_nos,'total_inc':total_inc,'total_exp':total_exp,'total':total})
def VehicleDetailView(request,veh_no):
    objs=Vehicle_Detail.objects.filter(VehicleNo=veh_no).values()
    vals=list(objs.values())
    total_inc = sum(val['Amount'] for val in vals if val['Amount']> 0 )
    total_exp = sum(val['Amount'] for val in vals if val['Amount']< 0 )
    total=total_inc+total_exp
    if request.POST:
        val=dict(request.POST.lists())
        start = datetime.strptime(val['start_date'][0],"%d-%m-%Y")
        end = datetime.strptime(val['end_date'][0],"%d-%m-%Y")
        daterange = [start + timedelta(days = x) for x in range(0, (end-start).days)]
        daterange.append(end)
        daterange = [dat.strftime("%d-%m-%Y") for dat in daterange]
        objs=Vehicle_Detail.objects.filter(VehicleNo=veh_no).filter(Date__in=daterange).values()
        vals=list(objs.values())
        total_inc = sum(val['Amount'] for val in vals if val['Amount']> 0 )
        total_exp = sum(val['Amount'] for val in vals if val['Amount']< 0 )
        total=total_inc+total_exp
        return render(request,'veh_details.html',{'objs':objs,'veh_no':veh_no,'daterange':daterange,'total_inc':total_inc,'total_exp':total_exp,'total':total})
    return render(request,'veh_details.html',{'objs':objs,'veh_no':veh_no,'total_inc':total_inc,'total_exp':total_exp,'total':total})
def Vehicle(request):
    try:
        rcm_veh_nos=pd.read_excel(path,na_filter=False,sheet_name='Vehicle Numbers').values.tolist()
        rcm_veh_nos=[item for sublist in rcm_veh_nos for item in sublist]
    except:
          rcm_veh_nos=[]
    if request.method == 'POST':
        form = Vehicle_Detail_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/veh_list')
    else:
        form = Vehicle_Detail_Form()
        form.fields['VehicleNo'].widget.datalist=rcm_veh_nos
    return render(request,'vehicle.html',{'form':form})
def FilterView(request):
    def range_days(rangestr):
                [start,end] = rangestr.split(':')
                start = datetime.strptime(start,"%d-%m-%Y")
                end = datetime.strptime(end,"%d-%m-%Y")
                daterange = [start + timedelta(days = x) for x in range(0, (end-start).days)]
                daterange.append(end)
                daterange = [dat.strftime("%d-%m-%Y") for dat in daterange]
                return daterange
    try:
        rcm_drivers_mob_no=pd.read_excel(path,na_filter=False,sheet_name='Driver_Mobile').to_dict()
        rcm_drivers=list(rcm_drivers_mob_no['Driver Name'].values())
    except:
        rcm_drivers_mob_no={}
        rcm_drivers=[]  
    if request.POST:
        val=dict(request.POST.lists())
        if val['search_in'][0] == '':
            objs=Movement.objects.all().exclude(Party__isnull = True).exclude(Party__exact = '').exclude(Party__exact = None).values(*val['display_col'])
        else:
            search_for=val['search_for'][0].upper()
            ranges = search_for.split(',')
            try:
                ranges = [range_days(Range) for Range in ranges]
                ranges=[item for sublist in ranges for item in sublist]
            except:
                pass
            objs=Movement.objects.filter(**{val['search_in'][0]+'__in':ranges}).exclude(Party__isnull = True).exclude(Party__exact = '').exclude(Party__exact = None).values(*val['display_col'])
        if 'Update' in request.POST:
             objs.update(**{val['search_in'][0]:val['update'][0].upper()})
             message='Updated Successfully for checking press Display'
             return render(request,'filter.html',{'cols':cols,'today':today,'message':message,'search_for':val['update'][0].upper()})
        elif 'Export' in request.POST:
            return ExcelResponse(objs)
        elif 'veh_stat' in request.POST:
            df = pd.DataFrame(Movement.objects.all().exclude(Party__isnull = True).exclude(Party__exact = '').exclude(Party__exact = None).values(),columns=['VehicleNo','Driver_Name','From','To1','To2','Party','Status','TripSheetDate','TransporterName'])
            df=df[(df['TripSheetDate'].str.contains(val['date'][0])) & (df['TransporterName'].str.contains('RCM'))]
            df=df.drop(['TransporterName','TripSheetDate'],axis=1)
            try:
                c_keys=[get_key(item,rcm_drivers_mob_no['Driver Name']) for item in df['Driver_Name'].to_string(index=False).split()] #Both Mob no and Dri_name has common key
                df['Mobile No']=[rcm_drivers_mob_no['Mobile Number'][c_key] for c_key in c_keys ] #Reading mobile number based on common key
            except:
                df['Mobile No']='Not Stored'
            table=df.to_html(escape=False)
            return render(request,'table.html',{'table':table})
        else:
             df = pd.DataFrame(objs,columns=val['display_col'])
             df['View']=""
             df['Edit']=""
             df['Delete']=""
             for i in range(len(df.index)):
                df['View'][i]=format_html('<a href=movement/'+str(df['id'][i])+'>(View)</a>')
                df['Edit'][i]=format_html('<a href=movement/'+'edit/'+str(df['id'][i])+'>(Edit)</a>')
                df['Delete'][i]=format_html('<a href=movement/'+str(df['id'][i])+'/delete/>(Delete)</a>')
             df.index+=1
             table=df.to_html(escape=False)
             return render(request,'table.html',{'table':table})
    return render(request,'filter.html',{'cols':cols,'today':today})
def delete_file(request):
    os.remove('Template.xlsx')
    return redirect('upload')
def FileUpload(request):
    path_exists=os.path.exists('Template.xlsx')
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FileForm()
    return render(request, 'upload.html', {'form': form,'path_exists':path_exists})    