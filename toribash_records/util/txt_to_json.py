import json
import os
import re

from toribash_records.util.path_finding import from_relative
from toribash_records.util.possible_results import MatchResult

# Converts Lull's match txt files to JSON format
def convert_match_to_json(p: str) ->  dict[str, dict]:
    with open(p, 'r') as f:
        raw_lines = f.readlines()

    lines = [line.strip() for line in raw_lines if line.strip()]
    stats = {"Meta": {}, "Records": [], "Result": []}
    stats["Meta"]["Name"] = p.split("/")[-1].split(".")[0]
    stats["Meta"]["Event"] = p.split("/")[-2]

    meta_lines = []
    record_lines = []
    result_lines = []

    stat_line_pattern = re.compile(r'(.+?)\s+([-\d]+%?)$')
    result_marker = re.compile(r'-{2,}\s*RESULT\s*-{2,}', re.IGNORECASE)
    record_marker = re.compile(r'-{2,}\s*RECORDS\s*-{2,}', re.IGNORECASE)
    divider_pattern = re.compile(r'-{3,}')

    current_player = None
    mode = 'meta'
    i = 0

    while i < len(lines):
        line = lines[i]

        # Switch to result parsing
        if result_marker.match(line):
            i += 1
            while i < len(lines):
                result_lines.append(lines[i])
                i += 1
            break

        # Switch to record parsing
        elif record_marker.match(line):
            mode = 'record'
            i += 1
            continue

        # Match stat lines
        match = stat_line_pattern.match(line)
        if match:
            stat_name, value = match.groups()
            stat_name = stat_name.strip()
            if value.endswith('%'):
                value = float(value.strip('%'))
            elif '.' in value:
                value = float(value)
            else:
                value = int(value)
            if current_player:
                stats[current_player][stat_name] = value
        elif not divider_pattern.match(line):
            # Non-stat line: could be a player name or metadata or record line
            if mode == 'meta':
                # If it's the first player, switch to player mode
                if not stat_line_pattern.match(lines[i + 1]):  # look ahead
                    meta_lines.append(line)
                else:
                    current_player = line
                    stats[current_player] = {}
                    mode = 'players'
            elif mode == 'record':
                record_lines.append(line)
            else:  # mode == 'players'
                current_player = line
                stats[current_player] = {}
        i += 1

    # Attach optional sections
    if meta_lines:
        stats["Meta"]["random"] = meta_lines
    if record_lines:
        stats["Records"] = record_lines
    if result_lines:
        stats["Result"] = result_lines
    else:
        stats["Result"] = ["Unknown"]

    res = stats["Result"][-1].lower().split(" ")
    if len(res) < 3:
        # Should only be draws or undocumented
        res = MatchResult.from_text(stats["Result"][-1].lower())
    else:
        # Should be <Name> via <win type>
        winner = res[0]
        stats["Winner"] = winner
        res = MatchResult.from_text(" ".join(res[1:]))

    if res == MatchResult.DRAW:
        stats["Result"].append("DRAW")
    elif res == MatchResult.UNDOCUMENTED:
        stats["Result"].append("UNDOCUMENTED")
    elif res:
        stats["Result"].append(res.name)

    return stats


if __name__ == '__main__':
    root_path = from_relative("../Data/Stats/TFC/")
    for directory in sorted(os.listdir(root_path), key=lambda x: int(x.split("_")[1])):
        directory_path = os.path.join(root_path, directory)
        for file in sorted(os.listdir(directory_path)):
            if file.endswith(".txt"):
                file_path = os.path.join(directory_path, file)
                print(file_path)
                data = convert_match_to_json(file_path)
                with open(file_path[:-3]+'json', 'w') as json_file:
                    json.dump(data, json_file, indent=4)