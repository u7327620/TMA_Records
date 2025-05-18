import unittest
from records.player import Player
from records.toribash_match import ToribashMatch


class PlayerTest(unittest.TestCase):
    def test_get_stats(self):
        test_player = Player("bladerunnr")
        ToribashMatch("Data/Events_Stats/TFC/TFC_1/Bladerunnr_vs_Danewninja.json")


if __name__ == '__main__':
    unittest.main()
