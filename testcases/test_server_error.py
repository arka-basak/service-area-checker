import unittest
from unittest.mock import patch, MagicMock
from pollGeometryServiceDriver import pollClinicianData,processServerError

class TestServerError(unittest.TestCase):

    @patch('pollGeometryServiceDriver.serverDownAlert')
    @patch('pollGeometryServiceDriver.requests.get')
    def test_internal_server_err(self, mock_get, mock_server_alert):
        error_response = {'error': 'Internal Server Error'}
        mock_get.return_value.json.return_value = error_response
        mock_server_alert.return_value = True

        pollClinicianData()

        mock_get.assert_called()
        mock_server_alert.assert_called()
        #test that it only runs once, even if querying for all id's 
        self.assertEqual(mock_server_alert.call_count, 1) 

    @patch('pollGeometryServiceDriver.serverDownAlert')
    def test_process_server_error(self, mock_server_alert):
        error_response = {'error': 'Internal Server Error'}
        result = processServerError(error_response)
        mock_server_alert.return_value = True
        self.assertEqual(result, {"status": False, "alerted": True})



if __name__ == '__main__':
    unittest.main()