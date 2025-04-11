import requests,json
from apscheduler.schedulers.background import BackgroundScheduler as scheduler
import os
from dotenv import load_dotenv
from generateSafetyStatus import generateSafetyStatus
# from multiprocessing import Pool
# from multiprocessing.dummy import Pool as ThreadPool


load_dotenv(dotenv_path = '.env')
clinician_status_url = os.getenv('CLINICIAN_STATUS_API_URL')

def pollPhlebotomistData():
    #pool = ThreadPool(7)
    for i in range(1,8):
        res = requests.get(f"{clinician_status_url}{i}").json()
        print(i, ' ',generateSafetyStatus(res))

    
if __name__ == "__main__" : 
    scheduler = scheduler({'apscheduler.job_defaults.max_instances': 2})
    scheduler.add_job(pollPhlebotomistData, 'interval', seconds =5)
    scheduler.start()

    while True: 
        user_input = input('Type \'exit\' to quit polling\n')
        if user_input == 'exit':
            print('exiting...')
            break
    scheduler.shutdown()


    #https://chriskiehl.com/article/parallelism-in-one-line