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

server = {
    "status": True,
    "alerted": False
}

def pollClinicianData():
    print(datetime.now(), '------------------------------------------')
    for id in range(START_ID,END_ID):
        query_id = uuid.uuid4()
        try:
            response = requests.get(f"{CLINICIAN_STATUS_API_URL}{id}").json()
            if 'error' in response:
                processServerError(response['error'])
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
             #print(f"Query:{id} {query_id} did not return ")

def printQueryResults(id, response):
        print(f"{id}: {response} | QueryID: {uuid.uuid4()}")


def initializeStatusJSON():
    statuses = {
        str(i): {
            "safetyStatus": True,
            "alerted": False
        } for i in range(1, 8)
    }

    with open("clinicianStatuses.json", "w") as f:
        json.dump(statuses, f, indent=2)

def processServerError(error):
    if not server['alerted']:
        server['alerted'] =  serverDownAlert(error)
    else:
        print('server error already alerted')

def resetServerStatus():
    server = {
        "status": True,
        "alerted": False
}



if __name__ == "__main__" : 
    initializeStatusJSON()
    scheduler = scheduler({'apscheduler.job_defaults.max_instances': 2})
    scheduler.add_job(pollClinicianData, 'interval', seconds =5)
    scheduler.start()

    while True: 
        user_input = input('Type \'exit\' to quit polling\n')
        if user_input == 'exit':
            print('exiting...')
            break
    scheduler.shutdown()


    #https://chriskiehl.com/article/parallelism-in-one-line