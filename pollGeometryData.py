import requests,json
from apscheduler.schedulers.background import BackgroundScheduler as scheduler


def pollPhlebotomistData():
    print('hello')



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