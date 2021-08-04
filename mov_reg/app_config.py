from django.apps import AppConfig
import os
import pandas as pd
rcm_drivers=[]
rcm_place_adv=[]
rcm_veh_nos=[]
rcm_drivers_mob_no={}
path = 'Template.xlsx'
class MovementConfig(AppConfig):
    name = 'mov_reg'
    def ready(self):
        path_exists=os.path.exists('Template.xlsx')
        global rcm_veh_nos,rcm_drivers,rcm_drivers_mob_no,rcm_place_adv
        if path_exists:
            rcm_veh_nos=pd.read_excel(path,na_filter=False,sheet_name='Vehicle Numbers').values.tolist()
            rcm_veh_nos=[item for sublist in rcm_veh_nos for item in sublist]
            rcm_place_adv=pd.read_excel(path,na_filter=False,sheet_name='Place_Advance').values.tolist()
            rcm_drivers_mob_no=pd.read_excel(path,na_filter=False,sheet_name='Driver_Mobile').to_dict()
            rcm_drivers=list(rcm_drivers_mob_no['Driver Name'].values())