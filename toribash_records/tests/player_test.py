import unittest
from toribash_records.objects.player import Player
from toribash_records.objects.toribash_match import ToribashMatch
from toribash_records.util.path_finding import from_relative


class PlayerTest(unittest.TestCase):
    def test_get_stats(self):
        test_player = Player("bladerunnr")
        test_match = ToribashMatch(from_relative("../Data/Stats/TFC/TFC_1/Bladerunnr_vs_Danewninja.json"))
        test_player.add_match(test_match)
        for stat in test_match.stats[test_player.player_name]:
            self.assertIn(stat, test_player.get_stats(),
                          f"{stat} from match stats is not in player stats")

if __name__ == '__main__':
    unittest.main()
