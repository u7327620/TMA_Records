import os
import unittest

from records.toribash_match import ToribashMatch
from records.util.path_finding import from_relative


class JsonVerification(unittest.TestCase):
    def test_verify_result(self):
        json_matches = []
        tfc_dir = from_relative("../Data/Events_Stats/TFC")
        for folder in os.listdir(tfc_dir):
            current_tfc_dir = os.path.join(tfc_dir, folder)
            for filename in os.listdir(current_tfc_dir):
                if filename.endswith(".json"):
                    json_matches.append(ToribashMatch(os.path.join(current_tfc_dir, filename)))

        for match in json_matches:
            if match.winner:
                # There is a winner, and it is one of the players
                self.assertTrue(match.player1_name == match.winner or match.player2_name == match.winner,
                                f"{match.winner} is not either {match.player1_name} or {match.player2_name}"
                                f"\nin match: {match.file_path}")
            else:
                res = match.result[-1]
                self.assertTrue(res == "DRAW" or res == "UNDOCUMENTED")

if __name__ == '__main__':
    unittest.main()
