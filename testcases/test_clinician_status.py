import unittest,json,os
from dotenv import load_dotenv
from pollGeometryServiceDriver import updateSafetyStatus, initializeStatusJSON
load_dotenv(dotenv_path = '.env')
CLINICIAN_STATUS_FILEPATH = os.getenv('CLINICIAN_STATUS_FILEPATH')

class TestClinicianStatus(unittest.TestCase):
    def setUp(self):
        initializeStatusJSON()

    def test_update_safety_status_false(self):
        updateSafetyStatus(1, False)
        with open(CLINICIAN_STATUS_FILEPATH, 'r') as f:
            data = json.load(f)
        self.assertFalse(data["1"]["safetyStatus"])
        self.assertFalse(data["1"]["alerted"])

if __name__ == '__main__':
    unittest.main()