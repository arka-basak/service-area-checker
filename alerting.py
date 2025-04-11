import os, json, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from clinicianStatus import alreadyAlerted,updateAlertStatus

load_dotenv(dotenv_path = '.env')
CLINICIAN_STATUS_API_URL = os.getenv('CLINICIAN_STATUS_API_URL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
ALERTS_INBOX = os.getenv('ALERTS_INBOX')
SENDER_PW = os.getenv('SENDER_PW')
PORT = os.getenv('PORT')




def unsafeClinicianAlert(clinician_id, query_id, location_data):
    """
    Checks if this trigger has been alerted for, and sends alert if not

    Parameters:
    clinician_id (int): id of OOB clinician
    query_id (string): (unused) to reference for logged queries
    location_data (JSON): Feature object of query response

    """
    if not alreadyAlerted(clinician_id):
        try:
            print(f'send alert email for {clinician_id}')
            msg = EmailMessage()
            msg.set_content(json.dumps(location_data, indent=2))
            msg['Subject'] = f"Clinician {clinician_id} has exited the service zone!"
            msg['From'] = SENDER_EMAIL
            msg['To'] = ALERTS_INBOX
            updateAlertStatus(clinician_id)
            sendMessage(msg)


        except Exception as e:
            print(e)
    else:
        print('alerted already')




def serverDownAlert(error_msg):
    """
    Sends Alert messages for Internal Server Errors

    Parameters:
    error_msg -- Error Message to sen

    """
    try:
        subject = error_msg['error']
        msg = EmailMessage()
        msg.set_content(json.dumps(error_msg, indent=2))
        msg['Subject'] = f'{subject}'
        msg['From'] = SENDER_EMAIL
        msg['To'] = ALERTS_INBOX
        sendMessage(msg)
        return True
    except Exception as e:
         print(e)



def sendMessage(msg):
    """
    Sends an email alert message via SMTP over SSL.

    Parameters:
    msg (EmailMessage): The email message object to be sent.
    """
    try: 
        with smtplib.SMTP_SSL('smtp.gmail.com', PORT) as smtp_server:
            smtp_server.login(SENDER_EMAIL, SENDER_PW)
            response = smtp_server.sendmail(SENDER_EMAIL, ALERTS_INBOX, msg.as_string())    
            print('alert sent')
    except Exception as e:
         print(e)

