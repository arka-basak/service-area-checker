import unittest
import json
from unittest.mock import patch
from pollGeometryServiceDriver import pollClinicianData, generateSafetyStatus

class TestComputedSafetyStatus(unittest.TestCase):

    test_cases = [
        ("test_case_1", "testcases/testdata/test_in1.json", True),
        ("test_case_2", "testcases/testdata/test_in2.json", True),
        ("test_case_3", "testcases/testdata/test_in3.json", True),
        ("test_case_4", "testcases/testdata/test_line5.json", True),
        ("test_case_5", "testcases/testdata/test_in6.json", True),
        ("test_case_5", "testcases/testdata/test_tight_out4.json", False),
        ("test_case_5", "testcases/testdata/test_out7.json", False),
    ]

    def test_generate_safety_status_outputs(self):
        for name, filepath, expected in self.test_cases:
            with self.subTest(name=name):
                with open(filepath) as f:
                    feature_response = json.load(f)
                    result = generateSafetyStatus(feature_response)
                    self.assertEqual(result, expected)

    @patch('pollGeometryServiceDriver.generateSafetyStatus', side_effect=generateSafetyStatus)
    @patch('pollGeometryServiceDriver.requests.get')
    @patch('pollGeometryServiceDriver.unsafeClinicianAlert')
    def test_poll_clinician_data_flow(self, mock_unsafe_alert, mock_requests_get, mock_safety_status):
        for name, filepath, expected in self.test_cases:
            with self.subTest(name=name):
                with open(filepath) as f:
                    feature_response = json.load(f)
                    mock_requests_get.return_value.json.return_value = feature_response

                    pollClinicianData()

                    if expected is False:
                        mock_unsafe_alert.assert_called()
                    else:
                        mock_unsafe_alert.assert_not_called()
                        self.assertTrue(mock_safety_status.return_value)

                    mock_unsafe_alert.reset_mock()


if __name__ == '__main__':
    unittest.main()
