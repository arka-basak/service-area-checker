import os,json
from dotenv import load_dotenv

load_dotenv(dotenv_path = '.env')
CLINICIAN_STATUS_FILEPATH = os.getenv('CLINICIAN_STATUS_FILEPATH')


def alreadyAlerted(clinician_id):
    with open(CLINICIAN_STATUS_FILEPATH, "r") as f:
        data = json.load(f)
        clinician = data[str(clinician_id)]
        #clinician['safetyStatus'] = False
        return clinician['alerted']


def updateAlertStatus(clinician_id):
    with open(CLINICIAN_STATUS_FILEPATH, "r+") as f:
        data = json.load(f)
        clinician = data[str(clinician_id)]
        clinician['alerted'] = True
        dumpJSON(f,data)

def updateSafetyStatus(clinician_id, status_val):
    #if status_val == False: 
        #print(status_val)
    with open(CLINICIAN_STATUS_FILEPATH, "r+") as f:
        data = json.load(f)
        clinician = data[str(clinician_id)]
        clinician['safetyStatus'] = status_val
        if status_val == True:
            clinician['alerted'] = False
        dumpJSON(f,data)

        

def dumpJSON(f, data):
    f.seek(0)
    json.dump(data,f,indent = 2)
    f.truncate()