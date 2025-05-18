import unittest
from records.toribash_match import ToribashMatch
from importlib import resources
from records.util.path_finding import from_relative


class ToribashMatchTest(unittest.TestCase):
    def test_init(self):
        with resources.as_file(resources.files('records').joinpath(
                '../Data/Events_Stats/TFC/TFC_1/Bladerunnr_vs_Danewninja.json')) as f:
            ToribashMatch(f)
            self.assertTrue(True, msg="ToribashMatch should initiate successfully")

    def test_extract(self):
        f = from_relative("../Data/Events_Stats/TFC/TFC_1/Bladerunnr_vs_Danewninja.json")
        tb_match = ToribashMatch(f)
        self.assertEqual(tb_match.event_name, "TFC_1")
        self.assertEqual(tb_match.meta["Name"], "Bladerunnr_vs_Danewninja")


if __name__ == '__main__':
    unittest.main()
