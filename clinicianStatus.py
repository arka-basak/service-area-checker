import os,json
from dotenv import load_dotenv

load_dotenv(dotenv_path = '.env')
CLINICIAN_STATUS_FILEPATH = os.getenv('CLINICIAN_STATUS_FILEPATH')


def alreadyAlerted(clinician_id):
    """
    Checks if 'unsafe' clinician has already triggered an alert

    Parameters:
    clinician_id (int)
    """
    with open(CLINICIAN_STATUS_FILEPATH, "r") as f:
        data = json.load(f)
        clinician = data[str(clinician_id)]
        return clinician['alerted']


def updateAlertStatus(clinician_id):
    """
    Updates alerted status to True from parent function (unsafeClinicianAlert)

    Parameters:
    clinician_id (int)
    """
    with open(CLINICIAN_STATUS_FILEPATH, "r+") as f:
        data = json.load(f)
        clinician = data[str(clinician_id)]
        clinician['alerted'] = True
        dumpJSON(f,data)

def updateSafetyStatus(clinician_id, status_val):
    """
    Updates safety attribute when server status changes

    Parameters:
    clinician_id (int)
    status_val (bool)
    """
    with open(CLINICIAN_STATUS_FILEPATH, "r+") as f:
        data = json.load(f)
        clinician = data[str(clinician_id)]
        clinician['safetyStatus'] = status_val
        if status_val == True:
            clinician['alerted'] = False
        dumpJSON(f,data)

        

def dumpJSON(f, data):
    """
    dump JSON helper to read/write into local files
    """
    f.seek(0)
    json.dump(data,f,indent = 2)
    f.truncate()