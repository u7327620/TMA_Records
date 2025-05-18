import os
from trueskill import Rating, quality_1vs1, rate_1vs1
from records import Fight
from result import MatchResult
from util import get_all_records

def generate_elo():
    path = os.path.join(os.getcwd(), "..", "../", "Data", "Events_Stats", "TFC")
    ratings: [str, Rating] = {}
    for folder in sorted(os.listdir(path), key=lambda x: int(x.split("_")[1])):
        folder_path = os.path.join(path, folder)
        for file in sorted(os.listdir(folder_path)):
            match_path = os.path.join(folder_path, file)
            fight = Fight(match_path)
            p1 = fight.player1.name
            p2 = fight.player2.name
            if p1 not in ratings:
                ratings[p1] = Rating()
            if p2 not in ratings:
                ratings[p2] = Rating()
            if fight.result is not MatchResult.UNDOCUMENTED:
                if fight.result in [MatchResult.DRAW, MatchResult.SPLIT_DRAW, MatchResult.MAJORITY_DRAW, MatchResult.UNANIMOUS_DRAW]:
                    ratings[p1], ratings[p2] = rate_1vs1(ratings[p1], ratings[p2], drawn=True)
                elif fight.winner.name == p1:
                    ratings[p1], ratings[p2] = rate_1vs1(ratings[p1], ratings[p2])
                else:
                    ratings[p2], ratings[p1] = rate_1vs1(ratings[p2], ratings[p1])
    return ratings

def _print_elo():
    elo = generate_elo()
    records = get_all_records()
    output = "<name> <W>-<L>-<D> <played> <rating> <confidence>\n\n"
    for name, rating in sorted(elo.items(), key=lambda x: x[1].mu, reverse=True):
        if 2 * rating.sigma < 10:
            output += records[name].to_txt() + f" {rating.mu:.2f} ± {2 * rating.sigma:.2f}\n"
    path = os.path.join(os.getcwd(), "ratings.txt")
    with open(path, "w") as f:
        f.write(output)

def player_record(name: str) -> list[str]:
    out = []
    out.append("<current_rating> <opponent> <opponent_rating> <outcome>\n")
    bruh = ""
    path = os.path.join(os.getcwd(), "..", "../", "Data", "Events_Stats", "TFC")
    ratings: [str, Rating] = {}
    for folder in sorted(os.listdir(path), key=lambda x: int(x.split("_")[1])):
        folder_path = os.path.join(path, folder)
        for file in sorted(os.listdir(folder_path)):
            match_path = os.path.join(folder_path, file)
            fight = Fight(match_path)
            p1 = fight.player1.name
            p2 = fight.player2.name
            if p1 not in ratings.keys():
                ratings[p1] = Rating()
            if p2 not in ratings.keys():
                ratings[p2] = Rating()
            if p1 == name or p2 == name:
                bruh = f"[{ratings[name].mu:.2f}, {ratings[name].sigma:.2f}] "
                if p1 == name:
                    bruh += f"{p2} ({ratings[p2].mu:.2f}, {ratings[p2].sigma:.2f}) "
                elif p2 == name:
                    bruh += f"{p1} ({ratings[p1].mu:.2f}, {ratings[p1].sigma:.2f}) "
                if fight.result is not MatchResult.UNDOCUMENTED:
                    if name != fight.winner.name:
                        bruh += f"lost {fight.result.value}"
                    else:
                        bruh += f"{fight.result.value}"
                out.append(bruh)
            if fight.result is not MatchResult.UNDOCUMENTED:
                if fight.result in [MatchResult.DRAW, MatchResult.SPLIT_DRAW, MatchResult.MAJORITY_DRAW,
                                    MatchResult.UNANIMOUS_DRAW]:
                    ratings[p1], ratings[p2] = rate_1vs1(ratings[p1], ratings[p2], drawn=True)
                elif fight.winner.name == p1:
                    ratings[p1], ratings[p2] = rate_1vs1(ratings[p1], ratings[p2])
                else:
                    ratings[p2], ratings[p1] = rate_1vs1(ratings[p2], ratings[p1])

    out.append(f"Final rating: {ratings[name].mu:.2f}, {ratings[name].sigma:.2f}")
    return out

if __name__ == "__main__":
    print("\n".join(player_record("danewninja")))