from unittest import TestCase

from main import YDCLIENT, TOKEN_YD, name_file


class TestSomething(TestCase):
    def test_ok(self):
        yd_client = YDCLIENT(TOKEN_YD)
        result = yd_client.new_folder(name_file)
        self.assertTrue(199 < result < 300)
