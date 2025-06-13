import unittest
from toribash_records.player import Player
from toribash_records.toribash_match import ToribashMatch
from toribash_records.util.path_finding import from_relative


class PlayerTest(unittest.TestCase):
    def test_get_stats(self):
        test_player = Player("Bladerunnr")
        test_match = ToribashMatch(from_relative("../Data/Stats/TFC/TFC_1/Bladerunnr_vs_Danewninja.json"))
        test_player.add_match(test_match)
        self.assertEqual(test_match.stats[test_player.player_name], test_player.get_stats(),
                         f"{test_match.stats[test_player.player_name]} \nis not equal to the player data:\n"
                         f"{test_player.get_stats()}")


if __name__ == '__main__':
    unittest.main()
