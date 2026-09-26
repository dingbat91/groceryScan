import unittest
from unittest.mock import patch
from barcode import outputCode

class TestNetworkClient(unittest.TestCase):

    @patch('barcode.socket.socket')
    def testOutputMessage(self, mockSocketClass):
        socketInstance:unittest = mockSocketClass.return_value
        socketInstance.__enter__.return_value = socketInstance
        test_host="192.168.0.48"
        test_port=4454
        test_code=123456
        outputCode(test_host,test_port,test_code)

        socketInstance.connect.assert_called_once_with((test_host,test_port))
        socketInstance.send.assert_called_once_with(123456)

if __name__ == "__main__":
    unittest.main(verbosity=2)