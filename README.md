# Clinician Location Tracking and Alerting Service

## Description
The Clinician Location Tracking and Alerting service periodically polls a `ClinicianStatusAPI`, checks whether a clinician's server location is inside or outside designated service areas, and sends an email alert if the clinician is located outside these areas. The service uses the raycast algorithm to determine if the location is outside the boundary by counting the number of intersections a horizontal ray from the location makes with the service area's boundary. An odd count guarantees the clinician is outside the boundary. It also sends alerts if the server is having issues.

## Installation

1. Set up a virtual environment
2. Install requirements.txt
3. Update .env file with credentials and configurable settings.

## Usage
Run the service with the following command:

```bash
python3 pollGeometryServiceDriver.py
type exit to stop the scheduler
```

This will start polling the ClinicianStatusAPI and send alerts when the clinician is outside the designated service area.

## Configuration
Update the `.env` file with the following environment variables:

- **CLINICIAN_STATUS_API_URL**: URL for the ClinicianStatus API.
- **SENDER_EMAIL**: Email address used to send alerts.
- **ALERTS_INBOX**: Email address to receive alerts.
- **SENDGRID_API_KEY**: (Unused) SendGrid API key for sending emails.
- **SENDER_PW**: Password for the sender email account.
- **CLINICIAN_STATUS_FILEPATH**: Path to store clinician status data.
- **MAX_QPS**: Maximum queries per second allowed for the API.
- **SAFETY**: (Unused) Percent of Max_QPS to hit API with 
- **SUSPICION_TIMEOUT**: (Unused) Timeout for suspicion state.
- **START_ID / END_ID**: IDs for the range of clinicians to monitor.
- **INTERVAL**: Time interval in seconds between polling.
- **PORT**: Port used for email sending (typically 465 for SMTP).

## Testing
Run the following unit tests to verify the service's functionality:

```bash
python3 -m unittest testcases.test_server_error
python3 -m unittest testcases.test_clinician_status
python3 -m unittest testcases.test_generateSafetyStatus
```
