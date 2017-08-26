import time
import unittest

from cantoolz.engine import CANSploit


class EcuControl(unittest.TestCase):

    def tearDown(self):
        self.CANEngine.stop_loop()
        self.CANEngine = None
        print("stopped")

    def test_ecu_commands_and_firewall(self):
        self.CANEngine = CANSploit()
        self.CANEngine.load_config("tests/configurations/test_9.py")
        self.CANEngine.start_loop()
        time.sleep(1)
        ret = self.CANEngine.call_module(1, "x")
        ret2 = self.CANEngine.call_module(1, "b")
        self.assertTrue(ret.find("Unknown") > 0, "Nothing yet")
        self.assertTrue(ret2.find("Unknown") > 0, "Nothing yet")

        self.CANEngine.call_module(0, "t t13320000")
        time.sleep(1)
        ret = self.CANEngine.call_module(1, "x")
        ret2 = self.CANEngine.call_module(1, "b")
        print(ret)
        self.assertFalse(ret.find("Unknown") >= 0, "Should be status")
        self.assertFalse(ret2.find("Unknown") >= 0, "Should be status")
        self.assertTrue(ret.find("Closed") >= 0, "Should be status")
        self.assertTrue(ret2.find("Closed") >= 0, "Should be statu")

        self.CANEngine.call_module(0, "t t1332ff22")
        time.sleep(1)
        ret = self.CANEngine.call_module(1, "x")
        ret2 = self.CANEngine.call_module(1, "b")
        self.assertTrue(ret.find("Closed") >= 0, "Should be status")
        self.assertTrue(ret2.find("Open") >= 0, "Should be status")

        self.CANEngine.call_module(1, "z")
        self.CANEngine.call_module(1, "a")
        time.sleep(1)
        ret = self.CANEngine.call_module(2, "p")
        ret2 = self.CANEngine.call_module(4, "p")
        print(ret)
        print(ret2)
        self.assertTrue(ret.find("0x122") >= 0, "0x122 should be there")
        self.assertTrue(ret.find("fff0") >= 0, "fff0 as body should be there")
        self.assertTrue(ret.find("ffff") >= 0, "ffff as body should be there")
        self.assertTrue(ret.find("ff22") >= 0, "ff22 as body should be there")
        self.assertTrue(ret.find("0x133") >= 0, "0x133 should be there")
        self.assertFalse(ret2.find("0x133") >= 0, "0x133 should NOT be there")
        self.assertFalse(ret2.find("ff22") >= 0, "0x133 should NOT be there")
        self.assertTrue(ret2.find("0x122") >= 0, "0x122 should be there")
