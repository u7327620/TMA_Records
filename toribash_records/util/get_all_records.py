import os
from json import JSONDecodeError
from trueskill import Rating, rate_1vs1, expose

from toribash_records.player import Player
from toribash_records.toribash_match import ToribashMatch
from toribash_records.util.path_finding import from_relative


def get_tfc_history(elo=False, elo_events: list[str]=None) -> dict[str, Player] | tuple[dict[str, Player], dict[str, Rating]]:
    """
    elo: Performs elo calculations
    elo_events: list of events to calculate elo ratings with, default=All

    typical usage: players, ratings = get_tfc_history(elo=True, elo_events=["TFC_22", "TFC_21"])
    """
    all_matches: list[ToribashMatch] = get_all_matches()
    all_players: dict[str, Player] = {}
    ratings = {}

    for match in sorted(all_matches, key=lambda x: int(x.event_name.split("_")[1])):
        p1 = match.player1_name
        p2 = match.player2_name

        if p1 not in all_players.keys():
            all_players[p1] = Player(p1)
        if p2 not in all_players.keys():
            all_players[p2] = Player(p2)
        all_players[p1].add_match(match)
        all_players[p2].add_match(match)

        if not elo:
            continue

        if elo_events:
            if match.event_name not in elo_events:
                continue

        if p1 not in ratings.keys():
            ratings[p1] = Rating()
        if p2 not in ratings.keys():
            ratings[p2] = Rating()

        if match.winner:
            if match.winner.lower() == match.player1_name.lower():
                ratings[p1], ratings[p2] = rate_1vs1(ratings[p1], ratings[p2])
            else:
                ratings[p2], ratings[p1] = rate_1vs1(ratings[p2], ratings[p1])
        elif match.result[-1] == "DRAW":
            ratings[p1], ratings[p2] = rate_1vs1(ratings[p1], ratings[p2], drawn=True)

    if elo:
        return all_players, ratings
    return all_players

def get_tfc_player_records(recent_tfc: list[str]=None, elo_events: list[str]=None, streak=False):
    """
    recent_tfc: List of events to count streak and consider a player active if they've played in.
    elo_events: List of events to calculate elo ratings with, default=All
    """
    players, ratings = get_tfc_history(True, elo_events)

    # runs trueskill expose() to sort ratings
    ratings = dict(sorted(ratings.items(), key=lambda x: x[1].mu - 3 * x[1].sigma, reverse=True))
    # dictionary as a mapping function of player_name to index in ratings (place on leaderboard)
    ratings_map = {key: z for z, key in enumerate(ratings)}

    output = []
    if not recent_tfc:
        for player in sorted(players.values(), key=lambda x: ratings_map.get(x.player_name)):
            wins, losses, draws = player.get_win_loss()
            pname = player.player_name
            rating = ratings[pname]

            x = f"{pname}: <{wins}-{losses}-{draws}> "
            x += f"{rating.mu - 3 * rating.sigma:.1f}, " # Trueskill rating
            output.append(x + f"({rating.mu:.1f}±{rating.sigma:.1f})")
        return output

    active_lines = []
    rated_active_lines = []
    inactive_lines = []
    rated_inactive_lines = []
    for player in players.values():
        wins, losses, draws = player.get_win_loss()
        streak = []
        active = False
        # Determines streak and if they were active
        for tfc in sorted(recent_tfc, key=lambda x: int(x.split("_")[1])):
            match = player.get_matches(tfc)
            if len(match) > 0:
                active = True

            if active and streak:
                match = match[0] # No handling for multiple fights in one event
                if match.winner:
                    if match.winner.lower() == player.player_name.lower():
                        streak.append("w")
                    else:
                        streak.append("l")
                elif match.result[-1] == "DRAW":
                    streak.append("d")
                else:
                    streak.append("?")
            elif streak and not active:
                streak.append("x")

        rated = False
        pname = player.player_name
        x = f"{pname}: <{wins}-{losses}-{draws}> "
        if active and streak:
            x += f"[{"-".join(streak)}] "
        if pname in ratings.keys():
            rated = True
            x += f"{ratings[pname].mu - 3 * ratings[pname].sigma:.1f}, "
            x += f"({ratings[pname].mu:.1f}±{ratings[pname].sigma:.1f})"
        if active:
            if rated:
                rated_active_lines.append(x)
            else:
                active_lines.append(x)
        else:
            if rated:
                rated_inactive_lines.append(x)
            else:
                inactive_lines.append(x)

    rated_active_lines = sorted(rated_active_lines, key=lambda x: ratings_map.get(x.split(":")[0]))
    rated_inactive_lines = sorted(rated_inactive_lines, key=lambda x: ratings_map.get(x.split(":")[0]))
    output.append("# Active rankings (last 3 TFC)")
    output.append(f"<Name>: <W>-<L>-<D> <{", ".join(recent_tfc)}> <elo>\n")
    output.append("\n".join(rated_active_lines))
    output.append("\n".join(active_lines))
    output.append("\n# Inactive rankings")
    output.append(f"<Name>: <W>-<L>-<D> <elo>\n")
    output.append("\n".join(rated_inactive_lines))
    output.append("\n".join(inactive_lines))
    return output

def get_all_matches() -> list[ToribashMatch]:
    all_matches: list[ToribashMatch] = []
    tfc_dir = from_relative("../Data/Stats/TFC")
    for folder in os.listdir(tfc_dir):
        current_tfc_dir = os.path.join(tfc_dir, folder)
        for filename in os.listdir(current_tfc_dir):
            if filename.endswith(".json"):
                try:
                    all_matches.append(ToribashMatch(os.path.join(current_tfc_dir, filename)))
                except JSONDecodeError as e:
                    print(f"Error in JSON code for: {os.path.join(current_tfc_dir, filename)}. {e}")
    return all_matches

if __name__ == "__main__":
    recent_tfcs = ["TFC_22", "TFC_21", "TFC_20"]
    calculate_elo_using = []#"TFC_22", "TFC_21", "TFC_20", "TFC_19", "TFC_18", "TFC_17", "TFC_16"]
    print("\n".join(get_tfc_player_records(recent_tfcs, calculate_elo_using)))