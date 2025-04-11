import requests,json,os, uuid
from apscheduler.schedulers.background import BackgroundScheduler as scheduler
from dotenv import load_dotenv
from datetime import datetime
from generateSafetyStatus import generateSafetyStatus
from clinicianStatus import updateSafetyStatus
from alerting import unsafeClinicianAlert, serverDownAlert


load_dotenv(dotenv_path = '.env')
CLINICIAN_STATUS_API_URL = os.getenv('CLINICIAN_STATUS_API_URL')
MAX_QPS = int(os.getenv('MAX_QPS'))
SAFETY = int(os.getenv('SAFETY'))
START_ID = int(os.getenv('START_ID'))
END_ID = int(os.getenv('END_ID'))
INTERVAL = int(os.getenv('INTERVAL'))

server = {
    "status": True,
    "alerted": False
}

def pollClinicianData():
    """
    Queries for Clinician Data, kicks off safety computations calls alerting
    To be periodically called by the scheduler.

    """
    print(datetime.now(), '------------------------------------------')
    for id in range(START_ID,END_ID):
        query_id = uuid.uuid4()
        try:
            response = requests.get(f"{CLINICIAN_STATUS_API_URL}{id}").json()        
            if 'error' in response:
                processServerError(response)
                raise Exception(f"{response['error']}")
            resetServerStatus()
            clinician_status = generateSafetyStatus(response)
            if not clinician_status: 
                updateSafetyStatus(id, clinician_status)
                unsafeClinicianAlert(id,query_id, response )
            else:
                updateSafetyStatus(id, clinician_status)
            printQueryResults(id, clinician_status)
            
        except Exception as e:
            print(e)

def printQueryResults(id, response):
        print(f"{id}: {response} | QueryID: {uuid.uuid4()}")


def initializeStatusJSON():
    """
    Initializes a Clinician Status JSON to read/write statuses 
    Note: (Used to avoid sending multiple emails for the clinician trigger)
    """
    statuses = {
        str(i): {
            "safetyStatus": True,
            "alerted": False
        } for i in range(START_ID, END_ID)
    }

    with open("clinicianStatuses.json", "w") as f:
        json.dump(statuses, f, indent=2)

def processServerError(error):
    """
    Checks if trigger has already been alerted for, and sends alerts if not.
    Note: (Used to avoid sending multiple emails for the same server error)
    """
    if not server['alerted']:
        server['alerted'] =  serverDownAlert(error)
    else:
        print('server error already alerted')
    return server

def resetServerStatus():
    """
    On receiving correct server responses, update global server status
    Note: (Used to avoid sending multiple emails for the same server error)
    """
    global server
    server = {
        "status": True,
        "alerted": False
    }
    return server


if __name__ == "__main__" : 
    """
    Initializes Clinician Status Tracker, and periodically runs 
    pollClinicianData 

    Notes:
    Run via 'python3 pollGeo
    Type 'exit' to shutdown scheduler
    """
    initializeStatusJSON()
    scheduler = scheduler({'apscheduler.job_defaults.max_instances': 2})
    scheduler.add_job(pollClinicianData, 'interval', seconds = INTERVAL)
    scheduler.start()

    while True: 
        user_input = input('Type \'exit\' to quit polling\n')
        if user_input == 'exit':
            print('exiting...')
            break
    scheduler.shutdown()
