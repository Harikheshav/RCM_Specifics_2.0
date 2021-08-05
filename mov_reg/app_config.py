from django.apps import AppConfig
import os
import pandas as pd
rcm_drivers=[]
rcm_place_adv=[]
rcm_veh_nos=[]
rcm_drivers_mob_no={}
class MovementConfig(AppConfig):
    name = 'mov_reg'
    def ready(self):
            googleSheetId = os.environ['googleSheetId']
            rcm_place_adv = pd.read_csv('https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
                googleSheetId,
                'Place_Advance'
            )).dropna(how='all', axis=1).values.tolist()
            rcm_veh_nos = pd.read_csv('https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
                googleSheetId,
                'Vehicle_Numbers'
            )).dropna(how='all', axis=1).values.tolist()
            rcm_veh_nos = [item for sublist in rcm_veh_nos for item in sublist]
            rcm_drivers_mob_no = pd.read_csv('https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
                googleSheetId,
                'Driver_Mobile'
            )).dropna(how='all', axis=1).to_dict()
            rcm_drivers=list(rcm_drivers_mob_no['Driver Name'].values())