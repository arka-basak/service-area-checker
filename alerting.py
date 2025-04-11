


import os, json
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from clinicianStatus import alreadyAlerted,updateAlertStatus

load_dotenv(dotenv_path = '.env')
CLINICIAN_STATUS_API_URL = os.getenv('CLINICIAN_STATUS_API_URL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
ALERTS_INBOX = os.getenv('ALERTS_INBOX')




def unsafeClinicianAlert(clinician_id, query_id, location_data):
    if not alreadyAlerted(clinician_id):
        try:
            message = Mail(
                from_email=SENDER_EMAIL,
                to_emails=ALERTS_INBOX,
                subject=f"Clinician {clinician_id} has exited the service zone!",
                plain_text_content=f'{json.dumps(location_data, indent =2 )}',
            # html_content=f'<strong> Query ID: {query_id}</strong>'
            )
            print(f'would send alert email for {clinician_id}')
            updateAlertStatus(clinician_id)

            response = sendMessage(message)
            if response == '202':
               updateAlertStatus(clinician_id)


        except Exception as e:
            print(e)
    else:
        print('alerted already')

def serverDownAlert(error_message):
    try:
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=ALERTS_INBOX,
            subject=f"{error_message}!",
            plain_text_content=f'{error_message}',
        # html_content=f'<strong> Query ID: {query_id}</strong>'
        )

        response = sendMessage(message)
        if response == '202':
            return True
        return False

    except Exception as e:
        print(e)


def sendMessage(message):
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        return response.status_code
    except Exception as e:
        print(e)



#unsafeClinicianAlert(1234, 12345)
