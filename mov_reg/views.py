from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Movement,Vehicle_Detail
from .forms import MovementForm,Vehicle_Detail_Form
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import os
import pandas as pd
import io
import xlsxwriter
import random
from django.utils.html import format_html
from django.db.models import Q
from datetime import date,timedelta,datetime
rcm_drivers = [] 
rcm_place_adv = []
rcm_veh_nos = []
rcm_drivers_mob_no = {}
cols=['Party','ACofParty','Movement','Size','PartyRef','ContainerNo','From','To1','To2','VehicleNo','TransporterName','InvoiceNo','InvoiceDate','InvoiceAmount','TripSheetNo','TripSheetAmount','TripSheetDate','CashAdvance','ChequeAdvance','Fixed_Advance','Diesel','Alloted_Diesel','Diesel_Advance','Status','Driver_Name']
not_varied=['Party','ACofParty','Movement','PartyRef','From','To1','To2','InvoiceNo']
sug_mov=['Party','ACofParty','From','To1','To2','VehicleNo','Driver_Name','TransporterName']
calc_data=['Alloted_Diesel','Fixed_Advance']
googleSheetId = os.environ['googleSheetId']
today=date.today().strftime("%d-%m-%Y")
def ready():
     global rcm_veh_nos,rcm_drivers,rcm_drivers_mob_no,rcm_place_adv
     rcm_place_adv = pd.read_csv('https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
     googleSheetId,
     'Place_Advance')).dropna(how='all', axis=1).values.tolist()
     rcm_veh_nos = pd.read_csv('https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
     googleSheetId,'Vehicle_Numbers')).dropna(how='all', axis=1).values.tolist()
     rcm_veh_nos = [item for sublist in rcm_veh_nos for item in sublist]
     rcm_drivers_mob_no = dict(pd.read_csv('https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
     googleSheetId,'Driver_Mobile')).dropna(how='all', axis=1).values)
     rcm_drivers_mob_no = {k.upper():v for k,v in rcm_drivers_mob_no.items()}
     rcm_drivers=list(rcm_drivers_mob_no.keys())
     delete_query = Q(Party__isnull = True) | Q(Party__exact = '') | Q(Party__exact = None)
     Movement.objects.filter(delete_query).delete()
def suggest(col_name):
    try:
        df=pd.DataFrame(list(Movement.objects.all().values()))
    except:
        df=pd.DataFrame(columns=cols)
    if df.empty:
        return []
    elif col_name=='Driver_Name':
        return rcm_drivers + ["Other Company"]
    else:
        return list(filter(None,set(df[col_name].values.tolist())))
def calc_fixed(From=None,To_1=None,To_2=None):
    for data in rcm_place_adv:
        if data[0].upper()==From.upper() and data[1].upper()==To_1.upper() and data[2].upper()==To_2.upper():
            return data[3],data[4]
    return 0,0
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('/login')
def install(request):
    return render(request,'install_app.html')
class HomeView(ListView):
    model=Movement
    template_name='home.html'
    def __init__(self):
        ready()
    def get_queryset(self):
        return Movement.objects.exclude(Party__isnull = True).exclude(Party__exact = '').exclude(Party__exact = None).order_by('-id')
class MovDetailView(DetailView):
    model=Movement
    template_name='mov_details.html'
class AddMovView_Initial(CreateView):
    model=Movement
    form_class= MovementForm
    template_name='add_mov.html'
    def __init__(self):
        ready()
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
        instances.Alloted_Diesel,instances.Fixed_Advance= calc_fixed(str(instances.From),str(instances.To1),str(instances.To2))
        instances.save()
        return HttpResponseRedirect('/add_mov_init')
class AddMovView_Empty(CreateView):
    model=Movement
    form_class= MovementForm
    template_name='add_mov.html'
    def __init__(self):
        ready()
    def get_context_data(self, **kwargs):
        context = super(AddMovView_Empty, self).get_context_data(**kwargs)
        context['form'] = MovementForm()
        for field in sug_mov:
            context['form'].fields[field].widget.datalist=suggest(field)
        context['form'].fields['Size'].widget.datalist=[20,40]
        context['form'].fields['Movement'].widget.datalist=['Import','Export','Offload','Empty']
        context['form'].fields['TripSheetDate'].initial = today
        return context
    def post(self, request, *args, **kwargs):
        form = MovementForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
    def form_valid(self, form):
        instances = form.save(commit=False)
        instances.Alloted_Diesel,instances.Fixed_Advance = calc_fixed(str(instances.From),str(instances.To1),str(instances.To2))
        instances.save()
        return HttpResponseRedirect('/add_mov_init')
class UpdateMovView(UpdateView):
    model=Movement
    form_class= MovementForm
    template_name='update_mov.html'
    def __init__(self):
        ready()
    def get_context_data(self, **kwargs):
        context = super(UpdateMovView, self).get_context_data(**kwargs)
        context['form'] = MovementForm()
        return context
    def form_valid(self, form):
        form.instance.Alloted_Diesel,form.instance.Fixed_Advance = calc_fixed(str(form.instance.From),str(form.instance.To1),str(form.instance.To2)) 
        return super().form_valid(form)
class DeleteMovView(UpdateView):
    model=Movement
    template_name='delete_mov.html'
    fields='__all__'
    success_url=reverse_lazy('home')
def FileUpload(request):
    ready()
    try:
        note='Sample Data:'+random.choice(rcm_veh_nos)+random.choice(rcm_place_adv[0])+random.choice(rcm_drivers)
    except:
        note='No Data'
    return render(request,'upload.html',{'note':note,'sheet_id':googleSheetId})
def FilterView(request):
    ready()
    def range_days(rangestr):
                [start,end] = rangestr.split(':')
                start = datetime.strptime(start,"%d-%m-%Y")
                end = datetime.strptime(end,"%d-%m-%Y")
                daterange = [start + timedelta(days = x) for x in range(0, (end-start).days)]
                daterange.append(end)
                daterange = [dat.strftime("%d-%m-%Y") for dat in daterange]
                return daterange
    
    def printColName(n):
         
        arr = [0] * 10000
        i = 0
     
        # Step 1: Converting to number
        # assuming 0 in number system
        while (n > 0):
            arr[i] = n % 26
            n = int(n // 26)
            i += 1
             
        #Step 2: Getting rid of 0, as 0 is
        # not part of number system
        for j in range(0, i - 1):
            if (arr[j] <= 0):
                arr[j] += 26
                arr[j + 1] = arr[j + 1] - 1
        val = '' 
        for j in range(i, -1, -1):
            if (arr[j] > 0):
                val = val + (chr(ord('A') + (arr[j] - 1)))   
        return  val
    if request.POST:
        val=dict(request.POST.lists())
        if val['search_in'][0] == '':
            objs=Movement.objects.all().exclude(Party__isnull = True).exclude(Party__exact = '').exclude(Party__exact = None).values(*(val['display_col']+['id']))
        else:
            search_for=val['search_for'][0].upper()
            ranges = search_for.split(',')
            try:
                ranges = [range_days(Range) for Range in ranges]
                ranges=[item for sublist in ranges for item in sublist]
            except:
                pass
            objs=Movement.objects.filter(**{val['search_in'][0]+'__in':ranges}).exclude(Party__isnull = True).exclude(Party__exact = '').exclude(Party__exact = None).values(*(val['display_col']+['id']))
        if 'Update' in request.POST:
             objs.update(**{val['search_in'][0]:val['update'][0].upper()})
             message='Updated Successfully'
             return render(request,'filter.html',{'cols':cols,'today':today,'message':message})
        elif 'Export' in request.POST:
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()
            i=2
            disp_cols = val['display_col']
            #Column Naming (A1=cols[0]:Z1=cols[Z-1])
            for col in disp_cols:
                worksheet.write(printColName(i)+'1', col)
                i+=1
            #Column Naming (A2=1:AZ=Z-1)
            for i in range(len(list(objs))+2):
                if i == 1:
                    worksheet.write('A'+str(i), 'S.No')
                else:
                    worksheet.write('A'+str(i), str(i-1))
            i = j = 2
            for obj in objs:
                j=2 #(Back to X2)
                for col in disp_cols:
                    worksheet.write(printColName(j)+str(i), obj[col])
                    j+=1
                i+=1
            # Close the workbook before sending the data.
            workbook.close()
            # Rewind the buffer.
            output.seek(0)
            # Set up the Http response.
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
            return response
        elif 'veh_stat' in request.POST:
            df = pd.DataFrame(Movement.objects.all().exclude(Party__isnull = True).exclude(Party__exact = '').exclude(Party__exact = None).values(),columns=['VehicleNo','Driver_Name','From','To1','To2','Party','Status','TripSheetDate','TransporterName'])
            pd.set_option('max_colwidth', None)
            df=df[(df['TripSheetDate'].str.contains(val['date'][0])) & (df['TransporterName'].str.contains('RCM'))]
            df=df.drop(['TransporterName','TripSheetDate'],axis=1)
            try:
                df['Mobile No']=df['Driver_Name'].apply(lambda x: rcm_drivers_mob_no.get(x)).astype(int)#Getting Mobile Name based on Driver_Name
            except:
                df['Mobile No']='Not Stored'
            table=df.to_html(escape=False)
            return render(request,'table.html',{'table':table,'veh_stat':True})
        else:
             pd.set_option('max_colwidth', None)
             df = pd.DataFrame(objs,columns=val['display_col']+['id'])
             df['View']=""
             df['Edit']=""
             df['Delete']=""
             for i in range(len(df.index)):
                df['View'][i]=format_html('<a href=movement/'+str(df['id'][i])+'>(View)</a>')
                df['Edit'][i]=format_html('<a href=movement/'+'edit/'+str(df['id'][i])+'>(Edit)</a>')
                df['Delete'][i]=format_html('<a href=movement/'+str(df['id'][i])+'/delete/>(Delete)</a>')
             df.index+=1
             df.drop('id',axis=1,inplace=True)
             table=df.to_html(escape=False)
        return render(request,'table.html',{'table':table,'veh_stat':False})
    return render(request,'filter.html',{'cols':cols,'today':today})
def VehicleView(request):
        ready()
        fields=['id','VehicleNo','CashAdvance','ChequeAdvance','Diesel_Advance','TripSheetAmount','InvoiceAmount','TripSheetDate']
        amounts=['CashAdvance','ChequeAdvance','Diesel_Advance','TripSheetAmount','InvoiceAmount']
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
    ready()
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
    ready()
    if request.method == 'POST':
        form = Vehicle_Detail_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/veh_list')
    else:
        form = Vehicle_Detail_Form()
        form.fields['VehicleNo'].widget.datalist=rcm_veh_nos
        form.fields['Date'].initial = today

    return render(request,'vehicle.html',{'form':form})